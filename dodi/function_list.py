##function start##
## 3 humps with a base secondary color
t = np.linspace(0, 30, steps//3)
r0 = -((t - 15)**2) + 225 
g0 = 50
b0 = 0
for j in range(steps//3):
    p_paths[0][j][0] = r0[j]
    p_paths[0][j][1] = g0
    p_paths[0][j][2] = b0

t = np.linspace(30, 60, steps//3)
g1 = -((t - 45)**2) + 225 
b1 = 50
r1 = 0
for j in range(steps//3, 2*steps//3):
    p_paths[0][j][0] = r1
    p_paths[0][j][1] = g1[j - (steps//3)]
    p_paths[0][j][2] = b1

t = np.linspace(60, 90, steps - (2*steps//3))
b2 = -((t - 75)**2) + 225 
r2 = 50
g2 = 0
for j in range(2*steps//3, steps):
    p_paths[0][j][0] = r2
    p_paths[0][j][1] = g2
    p_paths[0][j][2] = b2[j - (2*steps//3)]

##function end##


##function start##
##super mario hills sine waves
t = np.linspace(0, 4*np.pi, steps)
for j in range(steps - edge_size):
    for k in range(3):
        theta = t[j]
        p_paths[0][j][k] = ((14 * np.sin(theta + k*(2*np.pi/3))) + 14) \
            - (7 * np.sin(.5*theta + k*(np.pi/3)))**2 \
            + (((6 * np.sin(2*theta + k*(4*np.pi/3)))**2) + 2)
##function end##


##function start##
##higher color freq is higher wave freq
steps = 1000
p_paths = CreatePixelPaths(steps)
t = np.linspace(0, 8*np.pi, steps)
for i in range(total_lights):
    for j in range(steps):
        for k in range(3):
            theta = ((k+1) * 1.3)*t[j]
            p_paths[i][j][k] = ((42 * np.sin(theta + k*(2* np.pi/3))) + 38)
            if (j <= (steps // 3)):
                p_paths[i][j][2] = 0
            if ((j > (steps // 3)) and (j <= (2 * steps // 3))):
                p_paths[i][j][1] = 0
            if (j > (2* steps // 3)):
                p_paths[i][j][0] = 0
            
##function end##


##function start##
##random walk in color space
color_index = np.arange(3)
np.random.shuffle(color_index)
c_min = 8
c_max = 210

initial_state = np.random.randint(40, 180, 2)
p_paths[0][0][color_index[0]] = initial_state[0]
p_paths[0][0][color_index[1]] = initial_state[1]
switch = np.random.randint(0, 2) ##if equal to one go down
for j in range(1, steps//3):
    for k in range(2):
        seed = np.random.randint(-9, 18)
        if (p_paths[0][j-1][color_index[k]] < c_min):
            switch = 0
        if (p_paths[0][j-1][color_index[k]] > c_max):
            switch = 1
        # add/subtracting from prev step    
        if (switch==0):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] + seed
        if (switch==1):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] - seed
    if ((steps//3) - j < 50):
        p_paths[0][j][color_index[0]] *= .8

initial_state = np.random.randint(40, 180, 2)
p_paths[0][steps//3][color_index[1]] = initial_state[0]
p_paths[0][steps//3][color_index[2]] = initial_state[1]
for j in range((steps//3) + 1, 2*steps//3):
    for k in range(1, 3):
        seed = np.random.randint(-9, 18)
        if (p_paths[0][j-1][color_index[k]] < c_min):
            switch = 0
        if (p_paths[0][j-1][color_index[k]] > c_max):
            switch = 1
        # add/subtracting from prev step    
        if (switch==0):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] + seed
        if (switch==1):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] - seed
    if ((2*steps//3) - j < 50):
        p_paths[0][j][color_index[1]] *= .8


initial_state = np.random.randint(40, 180, 2)
p_paths[0][2*steps//3][color_index[2]] = initial_state[0]
p_paths[0][2*steps//3][color_index[0]] = initial_state[1]
for j in range((2*steps//3) + 1, steps):
    for k in [2, 0]:
        seed = np.random.randint(-9, 18)
        if (p_paths[0][j-1][color_index[k]] < c_min):
            switch = 0
        if (p_paths[0][j-1][color_index[k]] > c_max):
            switch = 1
        # add/subtracting from prev step    
        if (switch==0):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] + seed
        if (switch==1):
            p_paths[0][j][color_index[k]] = p_paths[0][j-1][color_index[k]] - seed
    if ((steps) - j < 50):
        p_paths[0][j][color_index[2]] *= .8
##function end##