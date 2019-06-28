import numpy as np
from scipy.stats import skewnorm
from master import *

##start##
a = 2
steps = 1000
color_max = 1 / 255
t_max = 300*skewnorm.ppf(0.5, a, scale=color_max)

p_paths = CreatePixelPaths(steps)

t = np.linspace(skewnorm.ppf(0.01, a, scale=color_max),
        t_max, steps)
count = 0
while (count < 100):
    color_index = np.random.randint(0, 3)
    offset = np.random.uniform(low=0, high=t_max)
    pulse = skewnorm.pdf(t, a, loc=offset, scale=color_max)
    for i in range(total_lights):
        for j in range(steps):
            p_paths[0][j][color_index] += pulse[j]
            p_paths[i][j][color_index] = p_paths[0][j][color_index]
    count+=1

##end of random_rbg_pulses part##
ShowPaths(p_paths)