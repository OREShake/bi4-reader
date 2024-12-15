import numpy as np


class Bi4DataType:
    class DataType:
        def __init__(self, key, offset, dtype, ncol):
            self.key = key
            self.offset = offset
            self.dtype = dtype
            self.ncol = ncol

    Points = DataType(b"ARRAY\x03\x00\x00\x00Pos", 11, np.float32, 3)
    Points_F64 = DataType(b"ARRAY\x04\x00\x00\x00Posd", 12, np.float64, 3)
    Idp = DataType(b"ARRAY\x03\x00\x00\x00Idp", 11, np.int32, 1)
    Vel = DataType(b"ARRAY\x03\x00\x00\x00Vel", 11, np.float32, 3)
    Rhop = DataType(b"ARRAY\x04\x00\x00\x00Rhop", 12, np.float32, 1)


class Bi4DataProperties:
    def __init__(self):
        self.visco_type = {"ViscoType": (1, 'I')}
        self.visco_value = {"ViscoValue": (1, 'f')}
        self.visco_bound_factor = {"ViscoBoundFactor": (1, 'f')}
        self.splitting = {"Splitting": (1, 'B')}
        self.dp = {"Dp": (1, 'd')}
        self.h = {"H": (1, 'd')}
        self.b = {"B": (1, 'd')}
        self.rhop_zero = {"RhopZero": (1, 'd')}
        self.mass_bound = {"MassBound": (1, 'd')}
        self.mass_fluid = {"MassFluid": (1, 'd')}
        self.gamma = {"Gamma": (1, 'd')}
        self.gravity = {"Gravity": (3, 'f')}
        self.case_pos_min = {"CasePosMin": (3, 'd')}
        self.case_pos_max = {"CasePosMax": (3, 'd')}
        self.peri_xinc = {"PeriXinc": (3, 'd')}
        self.peri_yinc = {"PeriYinc": (3, 'd')}
        self.peri_zinc = {"PeriZinc": (3, 'd')}
        self.data_2d = {"Data2d": (1, 'B')}
        self.data_2d_pos_y = {"Data2dPosY": (1, 'd')}
        self.npiece = {"Npiece": (1, 'I')}
        self.first_part = {"FirstPart": (1, 'I')}


class Bi4DataParticles:
    def __init__(self):
        self.all_points_key = 'CaseNp'
        self.fixed_points_key = 'CaseNfixed'
        self.moving_point_key = 'CaseNmoving'
        self.float_point_key = 'CaseNfloat'
        self.fluid_point_key = 'CaseNfluid'
