#color schemes for Dodi
import numpy as np

white = np.array([0, 0, 0, 255])

gold = np.array([[255 ,215 ,0, 0], [255, 223, 0, 0], [207, 181, 39, 0], \
                [120, 99, 0, 0], [48, 33, 0, 0], [12, 12, 0, 0]])

blues = np.array([[73, 61, 139, 0], [123, 104, 238, 0], [132, 112, 255, 0], \
                [0, 0, 128, 0], [25, 25, 112, 0], [0, 0, 250, 0], \
                [30, 144, 255, 0], [0, 191, 255, 0], [0, 206, 209, 0], \
                [64, 224, 208, 0], [0, 255, 255, 0], [0, 255, 180, 0], \
                [11, 66, 222, 0], [2, 33, 250, 0], [0, 89, 231, 0], \
                [0, 0, 255, 33]])

oranges = np.array([[255, 203, 30, 0], [255, 180, 0, 0], [250, 125, 0, 4], \
                    [250, 10, 10, 0], [252, 42, 160, 0], [255, 0, 0, 0], \
                    [255, 0, 0, 20], [212, 144, 40, 0], [255, 151, 105, 0], \
                    [255, 31, 88, 0], [255, 20, 180, 0], [255, 0, 5, 15], \
                    [254, 160, 11, 0], [255, 8, 64, 0], [150, 4, 1, 0], \
                    [80, 0, 0, 0], [144, 31, 0, 0], [142, 0, 63, 0]])

pinks = np.array([[255, 105, 180, 0], [255, 20, 147, 0], [255, 192, 203, 0], \
                    [176, 48, 96, 0], [199, 21, 133, 0], [208, 32, 144, 0], \
                    [238, 130, 238, 0], [218, 112, 214, 0], [186, 85, 211, 0], \
                    [153, 50, 204, 0], [148, 0, 211, 0], [138, 43, 226, 0], \
                    [160, 32, 240, 0], [147, 112, 219, 0]])

greens = np.array([[203, 255, 30, 0], [180, 255, 0, 0], [125, 250, 0, 4], \
                    [10, 250, 10, 0], [42, 252, 160, 0], [0, 255, 0, 0], \
                    [0, 255, 0, 20], [144, 212, 40, 0], [151, 255, 105, 0], \
                    [31, 255, 88, 0], [20, 255, 180, 0], [0, 255, 5, 15], \
                    [160, 254, 11, 0], [8, 255, 64, 0], [4, 150, 1, 0], \
                    [0, 80, 0, 0], [31, 144, 0, 0], [0, 142, 63, 0]])
                    
sunset = np.array([[86, 34, 25, 0], [71, 35, 45, 0], [83, 33, 29, 0], \
                    [89, 34, 21, 0], [76, 37, 48, 0], [77, 63, 73, 0], \
                    [93, 56, 24, 0], [94, 63, 19, 0], [87, 36, 45, 0], \
                    [24, 31, 55, 0], [45, 39, 61, 0], [60, 45, 64, 0], \
                    [73, 57, 72, 0], [60, 67, 76, 0], [35, 16, 17, 0]])

neons = np.array([[250, 0, 0, 0],[250, 62, 0, 0],[250, 125, 0, 0], \
                    [250, 187, 0, 0],[250, 250, 0, 0], [187, 250, 0, 0], \
                    [125, 250, 0, 0],[62, 250, 0, 0],[0, 250, 0, 0], \
                    [0, 250, 62, 0],[0, 250, 187, 0],[0, 250, 250, 0], \
                    [0, 187, 250, 0],[0, 125, 250, 0],[0, 62, 250, 0], \
                    [0, 0, 250, 0],[62, 0, 250, 0],[125, 0, 250, 0], \
                    [187, 0, 250, 0],[249, 0, 249, 0],[250, 0, 249, 0], \
                    [250, 0, 187, 0],[250, 0, 125, 0],[250, 0, 62, 0], \
                    [250, 0, 0, 0]])

pastels = np.array([[67, 161, 158, 0], [78, 142, 159, 0], [89, 123, 159, 0], \
                [101, 105, 160, 0], [112, 86, 160, 0], [123, 67, 161, 0], \
                [147, 63, 153, 0], [171, 60, 145, 0], [194, 56, 138, 0], \
                [218, 53, 130, 0], [242, 49, 122, 0], [245, 70, 105, 0], \
                [247, 90, 88, 0], [250, 111, 70, 0], [252, 131, 53, 0], \
                [255, 152, 36, 0], [222, 163, 50, 0], [188, 174, 65, 0], \
                [155, 185, 79, 0], [121, 196, 94, 0], [88, 207, 108, 0]])

                    
rainbow = np.array([[255, 0, 0, 0], [255, 127, 0, 0], [255, 255, 0, 0], \
                    [0, 255, 0, 0], [0, 0, 255, 0], [75, 0, 130, 0], \
                    [148, 0, 211, 0]])


x_space  = np.linspace(0, 8, 100)
x_space_small = np.linspace(0, 8, 16)
brighten = 2**x_space - 1
brighten_small = 2**x_space_small - 1