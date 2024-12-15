import numpy as np
import struct
import os


class Bi4File:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.data = self.read_file()

        self.int_key = 'i'
        self.double_key = 'd'
        self.long_long_key = 'q'
        self.int_size = struct.calcsize(self.int_key)
        self.double_size = struct.calcsize(self.double_key)
        self.long_long_size = struct.calcsize(self.long_long_key)

    def read_file(self) -> bytes:
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(
                f"File not found: {self.filepath}")

        if not os.access(self.filepath, os.R_OK):
            raise PermissionError(
                f"No permission to read the file: {self.filepath}")

        with open(self.filepath, 'rb') as file:
            return file.read()

    def search_value(self, str_needle, seek_counter, output_type, n_outputs=1):
        possible_control_characters = [
            "\f", "\v", "\b", "\x02", "\x16", "\x17"]

        hit_index = -1
        for pcc in possible_control_characters:
            str_needle_cc = f"\0{str_needle}{pcc}"
            hit_index = self.data.find(str_needle_cc.encode(), seek_counter)
            if hit_index != -1:
                break

        if hit_index == -1:
            print(f"StringNeedle: {str_needle}, was not found in file.")
            return None

        loc_a = hit_index + len(str_needle_cc) + 3
        loc_b = loc_a + struct.calcsize(output_type) * n_outputs

        val_r = struct.unpack(
            f'{n_outputs}{output_type}', self.data[loc_a:loc_b])

        if n_outputs == 1:
            return val_r[0]
        else:
            return val_r

    def read_array(self, key: bytes,
                   offset: int,
                   dtype: np.dtype,
                   ncol: int) -> tuple[np.ndarray, int]:
        start_pos = self.data.find(key)
        if start_pos == -1:
            raise ValueError(
                f"Key '{key}' not found in data.")
        start_pos += offset

        nid_s = start_pos + 1 + self.long_long_size
        nid_e = nid_s + self.int_size - 1
        if nid_e >= len(self.data):
            raise IndexError("Not enough data to read the array size.")
        nid_data = self.data[nid_s:nid_e + 1]

        size = self.get_value(self.int_key, nid_data)
        if size < 0:
            raise ValueError("Array size cannot be negative.")

        did_s = nid_e + 1 + self.int_size
        did_e = did_s + self.calc_size(dtype) * size * ncol - 1
        if did_e >= len(self.data):
            raise IndexError("Not enough data to read the array.")
        did_data = self.data[did_s:did_e + 1]

        return self.get_array(dtype, did_data)

    def get_time(self):
        time_key = "TimeStep"

        position = self.data.find(time_key.encode())
        if position == -1:
            raise ValueError(
                f"String '{time_key}' not found in data.")
        position += len(time_key)

        first_pos = position + self.int_size
        last_pos = first_pos + self.double_size
        if last_pos > len(self.data):
            raise IndexError("Not enough data to read the time.")

        time_data = self.data[first_pos:last_pos]
        return self.get_value(self.double_key, time_data)

    def get_number_of_particles(self, key):
        position = self.data.find(key.encode())
        position += len(key)

        first_pos = position + self.int_size
        last_pos = first_pos + self.int_size

        particle_data = self.data[first_pos:last_pos]
        return self.get_value(self.int_key, particle_data)

    def get_property(self, key):
        sV, sT = list(key.items())[0]
        n, t = sT
        if n == 1:
            a = self.search_value(sV, 1, t)
        elif n == 3:
            a = self.search_value(sV, 1, t, n)
        return a

    def search_type(self, str2_search):
        possible_types = ["Fixed", "Floating", "Fluid"]
        for pt in possible_types:
            if pt.encode() in str2_search:
                return pt

    def get_value(self, key, hex):
        return struct.unpack(key, hex)[0]

    def get_array(self, dtype, data):
        return np.frombuffer(data, dtype=dtype)

    def calc_size(self, dtype):
        return struct.calcsize(np.dtype(dtype).char)
