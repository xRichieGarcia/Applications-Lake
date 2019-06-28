import numpy as np
from master import *

## define the RGBW path of one LED between fucntion start/end comments
## symmetry scripts copy single path to whole strip in different ways

### edge2 symmetry ###
steps = 1000
p_paths = CreatePixelPaths(steps, num_lights=ray_size)

##function start##
t = np.linspace(0, 4*np.pi, steps)
for j in range(steps - ray_size):
    for k in range(3):
        theta = t[j]
        p_paths[0][j][k] = ((14 * np.sin(theta + k*(2*np.pi/3))) + 14) \
            - (7 * np.sin(.5*theta + k*(np.pi/3)))**2 \
            + (((6 * np.sin(2*theta + k*(4*np.pi/3)))**2) + 2)
##function end##

for i in range(ray_size):
    for j in range(steps - ray_size):
        for k in range(3):
            p_paths[i][j - (40*i)][k] = p_paths[0][j][k]
f_paths = FlattenEdge2(p_paths)
