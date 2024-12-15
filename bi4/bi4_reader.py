import os
import re
from collections import OrderedDict
from .bi4_file import Bi4File
from .bi4_data_type import Bi4DataType, Bi4DataProperties, Bi4DataParticles


class Bi4Reader:
    def __init__(self, path: str = '.') -> None:
        self.path = path
        self.files = self._get_files()

        self.data_type = Bi4DataType()
        self.particle_keys = Bi4DataParticles()
        self.property_keys = Bi4DataProperties()

    def _get_files(self, rgx_pat="Part_\\d{4}.bi4"):
        bi4_files = {}
        file_names = os.listdir(self.path)
        for file_name in file_names:
            if re.search(rgx_pat, file_name):
                file_path = os.path.join(self.path, file_name)
                bi4_files[file_name] = Bi4File(file_path)
        return bi4_files

    def _get_head_config(self):
        return list(self._get_files("Part_Head").items())[0][1]

    def read_bi4_number_of_particles(self, key):
        number_of_particles = {}
        for file_name in self.files:
            count = self.files[file_name].get_number_of_particles(key)
            number_of_particles[file_name] = count
        return number_of_particles

    def read_bi4_property(self, key):
        config = self._get_head_config()
        return config.get_property(key)

    def read_bi4_data(self, data_type):
        data = {}
        for file_name in self.files:
            array = self.files[file_name].read_array(data_type.key,
                                                     data_type.offset,
                                                     data_type.dtype,
                                                     data_type.ncol)
            data[file_name] = array
        return data

    def read_bi4_points_type(self):
        pass

# ------------------------------------------------------------------------------
# Points
# ------------------------------------------------------------------------------

    def read_bi4_all_points(self):
        return self.read_bi4_data(self.data_type.Points)

    def read_bi4_fixed_points(self):
        # return self.read_bi4_all_points()[]
        pass

# ------------------------------------------------------------------------------
# Simulation times
# ------------------------------------------------------------------------------

    def read_bi4_time(self):
        times = {}
        for file_name in self.files:
            time = self.files[file_name].get_time()
            times[file_name] = time
        return times

# ------------------------------------------------------------------------------
# Number of particles
# ------------------------------------------------------------------------------

    def read_bi4_number_of_all_particles(self):
        return self.read_bi4_number_of_particles(
            self.particle_keys.all_points_key)

    def read_bi4_number_of_fixed_particles(self):
        return self.read_bi4_number_of_particles(
            self.particle_keys.fixed_points_key)

    def read_bi4_number_of_moving_particles(self):
        return self.read_bi4_number_of_particles(
            self.particle_keys.moving_point_key)

    def read_bi4_number_of_float_particles(self):
        return self.read_bi4_number_of_particles(
            self.particle_keys.float_point_key)

    def read_bi4_number_of_fluid_particles(self):
        return self.read_bi4_number_of_particles(
            self.particle_keys.fluid_point_key)

# ------------------------------------------------------------------------------
# Simulation properties
# ------------------------------------------------------------------------------

    def read_bi4_viscosity_formulation(self, show_comment=False):
        if show_comment:
            print('Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)')
        return self.read_bi4_property(
            self.property_keys.visco_type)

    def read_bi4_viscosity_value(self, show_comment=False):
        if show_comment:
            print('Viscosity value')
        return self.read_bi4_property(
            self.property_keys.visco_value)

    def read_bi4_visco_bound_factor(self, show_comment=False):
        if show_comment:
            print('Multiply viscosity value with boundary (default=1)')
        return self.read_bi4_property(
            self.property_keys.visco_bound_factor)

    def read_bi4_distance_between_particles(self, show_comment=False):
        if show_comment:
            print('Distance between particles (m)')
        return self.read_bi4_property(
            self.property_keys.dp)

    def read_bi4_interaction_radius(self, show_comment=False):
        if show_comment:
            print('Interaction radius (m)')
        return self.read_bi4_property(
            self.property_keys.h)

    def read_bi4_initial_density(self, show_comment=False):
        if show_comment:
            print('Reference density of the fluid (kg/m^3)')
        return self.read_bi4_property(
            self.property_keys.rhop_zero)

    def read_bi4_gamma(self, show_comment=False):
        if show_comment:
            print('Polytropic constant for water used in the state equation')
        return self.read_bi4_property(
            self.property_keys.gamma)

    def read_bi4_gravitational_acceleration(self, show_comment=False):
        if show_comment:
            print('Gravitational acceleration (m/s^2)')
        return self.read_bi4_property(
            self.property_keys.gravity)

    def read_bi4_case_range(self, show_comment=False):
        if show_comment:
            print('Simulation range [min : max] (m)')
        case_range = self.read_bi4_property(
            self.property_keys.case_pos_min)
        case_range += self.read_bi4_property(
            self.property_keys.case_pos_max)
        return case_range

    def read_bi4_simulation_dimension(self, show_comment=False):
        if show_comment:
            print('Simulation dimension 0:3D 1:2D')
        return self.read_bi4_property(
            self.property_keys.data_2d)

    def read_bi4_simulation_position(self, show_comment=False):
        if show_comment:
            print('Simulation plane position (m)')
        return self.read_bi4_property(
            self.property_keys.data_2d_pos_y)

    def read_bi4_splitting(self):
        return self.read_bi4_property(self.splitting)

    def read_bi4_head(self):
        bi4_head = self._get_head_config()
        rf = bi4_head.read_file()

        needle = "ITEM"
        item_locs = []
        ind = 0

        while True:
            ind = rf.find(needle.encode(), ind + 1)
            if ind == -1:
                break
            item_locs.append(ind)

        item_locs.pop(0)
        item_locs.pop(0)
        item_locs.append(len(rf))

        item_ranges = [range(item_locs[i], item_locs[i+1])
                       for i in range(len(item_locs)-1)]

        bi4_id_count = 0
        dct = []

        for val_range in item_ranges:
            rf_ = rf[val_range.start:val_range.stop]
            count = bi4_head.search_value("Count", 1, 'i')
            mk_type = bi4_head.search_value("MkType", 1, 'i')
            mk = bi4_head.search_value("Mk", 1, 'i')
            actual_type = bi4_head.search_type(rf_)

            print(f"Range: {val_range}, Count: {count}, MkType: {
                  mk_type}, Mk: {mk}, Type: {actual_type}")

            dct.append(OrderedDict(
                {"Type": actual_type, "MkType": mk_type, "Mk": mk, "Begin": bi4_id_count, "Count": count}))
            bi4_id_count += count

        return dct
