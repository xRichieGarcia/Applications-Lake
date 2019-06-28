import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skewnorm
"""currently testing random_rgb_pulses. Seems way to heavy for the pi
    t2.micro has taken 20+ minutes to fill p_paths """

total_lights = 270
edge_size = 9
total_edges = 30
ray_size = 9 //2 + 1

def CreatePixelPaths(steps, num_lights=total_lights):
    p_paths = np.zeros([num_lights, steps, 4])
    return(p_paths)
    
### edge symmetry ###
steps = 1000
p_paths = CreatePixelPaths(steps, num_lights=edge_size)

##function start##

from color_bump import bump
bump_steps = bump.shape[0]
steps = bump_steps // 3
p_paths = CreatePixelPaths(steps, num_lights=edge_size)

for j in range(0, bump_steps, 3):
    r_index = (j + 120) % 360
    g_index = j
    b_index = (j + 240) % 360
    p_paths[0][j // 3][0] = bump[r_index]
    p_paths[0][j // 3][1] = bump[g_index]
    p_paths[0][j // 3][2] = bump[b_index]

##function end##

t = np.linspace(0, steps, steps)

##plottting p_paths of pixel zero##
fig, ax = plt.subplots()
p_paths = p_paths.astype(int)
p_paths[p_paths<0] = 0
p_paths[p_paths>255] = 255

r_space = np.zeros(steps)
g_space = np.zeros(steps)
b_space = np.zeros(steps)

for j in range(steps):
    r_space[j] = p_paths[0][j][0]
    g_space[j] = p_paths[0][j][1]
    b_space[j] = p_paths[0][j][2]

ax.plot(t, r_space,
    'r-', lw=1, alpha=0.6, label='Red')
ax.plot(t, g_space,
    'g-', lw=1, alpha=0.6, label='Green')
ax.plot(t, b_space,
    'b-', lw=1, alpha=0.6, label='Blue')
    
plt.axvline(x=edge_size, color='k', linestyle='--', label='Edge size')
ax.set(xlabel='Frame', ylabel='Intensity',
       title='RGB path of one pixel')
ax.grid()
ax.legend(loc='best', frameon=False)
ax.set_ylim(0, 255)

fig.savefig("test.png")
