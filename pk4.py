from ctypes import LittleEndianStructure, Union, c_uint8 as u8, c_uint16 as u16, c_uint32 as u32

# shift -> block order l where ABCD is 0 1 2 3
blocks = {0: [0, 1, 2, 3], 1: [0, 1, 3, 2], 2: [0, 2, 1, 3], 3: [0, 2, 3, 1], 4: [0, 3, 1, 2], 5: [0, 3, 2, 1],
          }
