import argparse
from bi4.bi4_data_type import Bi4DataType
from bi4.bi4_file import Bi4File
from bi4.bi4_reader import Bi4Reader

reader = Bi4Reader('./data')

def get_file_name(part_number):
    return f'Part_{part_number:04d}.bi4'

def read_time(file_name):
    times = reader.read_bi4_time()
    print(f'{file_name} time: {times[file_name]}')

def read_number_of_all_particles(file_name):
    count = reader.read_bi4_number_of_all_particles()
    print(f'{file_name} number of all particles: {count[file_name]}')

def read_number_of_fixed_particles(file_name):
    count = reader.read_bi4_number_of_fixed_particles()
    print(f'{file_name} number of fixed particles: {count[file_name]}')

def read_number_of_moving_particles(file_name):
    count = reader.read_bi4_number_of_moving_particles()
    print(f'{file_name} number of moving particles: {count[file_name]}')

def read_number_of_float_particles(file_name):
    count = reader.read_bi4_number_of_float_particles()
    print(f'{file_name} number of float particles: {count[file_name]}')

def read_number_of_fluid_particles(file_name):
    count = reader.read_bi4_number_of_fluid_particles()
    print(f'{file_name} number of fluid particles: {count[file_name]}')

def read_number_of_particles(file_name):
    read_number_of_all_particles(file_name)
    read_number_of_fixed_particles(file_name)
    read_number_of_moving_particles(file_name)
    read_number_of_float_particles(file_name)
    read_number_of_fluid_particles(file_name)

def read_visco_type():
    value = reader.read_bi4_viscosity_formulation()
    print(f"Visco type: {value}")

def read_visco_value():
    value = reader.read_bi4_viscosity_value()
    print(f"Visco value: {value}")

def read_visco_bound_factor():
    value = reader.read_bi4_visco_bound_factor()
    print(f"Visco bound factor: {value}")

def read_case_range():
    value = reader.read_bi4_case_range()
    print(f"Case range: {value}")

def read_simulation_dimension():
    value = reader.read_bi4_simulation_dimension()
    print(f"Simulation dimension {value}")

def read_simulation_position():
    value = reader.read_bi4_simulation_position()
    print(f"Simulation position: {value}")

def read_properties():
    read_visco_type()
    read_visco_value()
    read_visco_bound_factor()
    read_case_range()
    read_simulation_dimension()
    read_simulation_position()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a BI4 file.')
    parser.add_argument('--file', type=int, required=True, help='Part number of the BI4 file')
    args = parser.parse_args()

    part_number = args.file
    file_name = get_file_name(part_number)
    
    read_time(file_name)
    read_number_of_particles(file_name)
    read_properties()
