from master import *
from color_bump import bump
"""clean sine waves based on discrete array 360 elements long """


### edge2 symmetry ###
##function start##
bump_steps = bump.shape[0]
skip_size = 12 # how many elements to skip in color bump
steps = bump_steps // skip_size
p_paths = CreatePixelPaths(steps, num_lights=ray_size)

for j in range(0, bump_steps, skip_size):
    r_index = (j + 120) % 360
    g_index = j
    b_index = (j + 240) % 360
    p_paths[0][j // skip_size][0] = bump[r_index]
    p_paths[0][j // skip_size][1] = bump[g_index]
    p_paths[0][j // skip_size][2] = bump[b_index]
##function end##

for i in range(ray_size):
    for j in range(steps):
        for k in range(3):
            p_paths[i][j - (5*i)][k] = p_paths[0][j][k]
### edge2 symmetry end###
f_paths = FlattenEdge2(p_paths)
while True:
    ShowPaths(f_paths, delay=.001)

