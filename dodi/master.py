#import board
#import neopixel
import time
import numpy as np
from colorschemes import *

edge_size = 9 #LEDS per edge
total_edges = 30
total_lights = edge_size * total_edges
ray_size = edge_size // 2 + 1  #edge_size must be odd
#p_order = neopixel.GRBW #neopixel.GRBW is actually RGBW

"""the global pixel_state is updated by ShowState() and ShowPaths()"""
#pixel_state = neopixel.NeoPixel(board.D18, total_lights,
#                            brightness=.4, auto_write=False, pixel_order=p_order)

### TOOLBOX ###
def CreatePixelPaths(steps, num_lights=total_lights):
    p_paths = np.zeros([num_lights, steps, 4])
    return(p_paths)

def RandomColor():
    rgbw_val = np.zeros(4)
    rgbw_val[0] = np.random.randint(0, 255)
    g_range = 255 - rgbw_val[0]
    rgbw_val[1] = np.random.randint(0, g_range)
    rgbw_val[2] = 255 - rgbw_val[0] - rgbw_val[1]
    return (rgbw_val)

def RandomNeon():
    value_1 = np.random.randint(0, 255)
    value_2 = 255 - value_1
    index = np.arange(3)
    np.random.shuffle(index)
    rgbw_val = np.zeros(4)
    rgbw_val[index[0]] = value_1
    rgbw_val[index[1]] = value_2
    return (rgbw_val)

def RandomElement(arr):
    total_elements = arr.shape[0]
    random_index = np.random.randint(0, total_elements)
    return(arr[random_index])

def Decision(probability):
    return (np.random.rand() < probability)

""" input: a step in pixel_paths, target pixel index, and an optional color to replace
 output: next step in pixel_paths with target pixel copied to left or right"""
def RadiateLeft(path_instance, target, new_color):
    l_neighbor = target - 1
    if (l_neighbor < 0):
        l_neighbor = total_lights - l_neighbor
    next_instance = np.copy(path_instance)
    next_instance[l_neighbor][:] = path_instance[target][:]
    if new_color:
        next_instance[target][:] = new_color[:]
    else:
        next_instance[target][:] = np.array([0,0,0,0])
    return(next_instance)

def RadiateRight(path_instance, target, new_color):
    r_neighbor = target - 1
    if (r_neighbor >= total_lights):
        r_neighbor = r_neighbor - total_lights
    next_instance = np.copy(path_instance)
    next_instance[r_neighbor][:] = path_instance[target][:]
    if new_color:
        next_instance[target][:] = new_color[:]
    else:
        next_instance[target][:] = np.array([0,0,0,0])
    return(next_instance)

def ShiftLeft(path_instance):
    next_instance = np.copy(path_instance)
    for i in range(total_lights-1):
        next_instance[i][:] = path_instance[i+1][:]
    next_instance[total_lights][:] = path_instance[0][:]
    return(next_instance)

# input steps wanted, starting path instance, skips(optional) 
# output p_paths of size steps
def Roll(path_instance, steps, skips=0):
    lights = path_instance.shape[0]
    total_steps = steps * (skips + 1)
    p_paths = CreatePixelPaths(total_steps, num_lights=lights)
    for i in range(0, total_steps, skips+1):
        p_state = np.roll(path_instance, i, axis=0)
        for j in range(lights):
            p_paths[j][i] = p_state[j]
    return(p_paths)

def ShiftRight(path_instance):
    next_instance = np.copy(path_instance)
    next_instance[0][:] = path_instance[total_lights][:]
    for i in range(total_lights-1):
        next_instance[i+1][:] = path_instance[i][:]
    return(next_instance)

def GetDiff(a, b):
    if(a>=b):
        return (a-b)
    else:
        return (b-a)

""" Trims the path for one pixel in random places to get to target_size"""
def NormalizePath(p_path, target_size):
    path_size = p_path.shape[0]
    if (path_size > target_size):
        diff = path_size - target_size
        choices = np.arange(path_size)
        choices = np.random.shuffle(choices)
        drop_index = choices[:diff]
        new_path = np.delete(p_path, drop_index)
        return(new_path)
    else:
        return(p_path)

""" Input: dictionary set of pixel_paths
    Output: key (pixel number) of shortest path"""
def ShortestPath(p_paths):
    min_pathsize = p_paths[0].shape[0]
    num_lights = p_paths.shape[0]
    for i in range(num_lights):
        pixel_pathsize = p_paths[i].shape[0]
        if (pixel_pathsize < min_pathsize):
            min_pathsize = pixel_pathsize
    return (min_pathsize)

""" normalizes all pixel_paths to the size of the shortest one
    Input: dictionary pixel_paths
    Output: normalized dictionary pixel_paths"""
def NormalizeAll(p_paths):
    short_path = ShortestPath(p_paths)
    for i in range(total_lights):
        p_paths[i] = NormalizePath(p_paths[i], short_path)
    p_paths = p_paths.astype(int)
    p_paths = np.clip(p_paths, 0, 255)
    return(p_paths)

""" Input: intensity of fade (0.0-1.0) with 1.0 turning pixel off completely
    Output: individual rgbw value"""
def ColorFade(c1, intensity):
    faded_color = (1 - intensity) * c1
    faded_color = faded_color.astype(int)
    faded_color = np.clip(faded_color, 0, 255)
    return(faded_color)

""" Input: pixel_paths, target pixel, when, and how many steps of dimming
    Output: edited p_paths with target getting dimmed to zero"""
def Dimmer(p_paths, target, step, total_dims):
    color = p_paths[target][step]
    if (p_paths.shape[1] - step < total_dims):
        return(p_paths)
    else:
        for i in range(step, step+total_dims):
            intensity = ((i-step)/total_dims) * ((1 - ((i-step)/total_dims)) + 1)
            faded_color = ColorFade(color, intensity)
            p_paths[target][i] = faded_color
    return(p_paths)

""" Input: pixel_paths, desired color, target pixel, when,
        and how many steps of antidimming
    Output: edited p_paths with target getting approached from zero"""
def AntiDimmer(p_paths, color, target, step, total_dims):
    if (p_paths.shape[1] - step < total_dims):
        return(p_paths)
    else:
        for i in range(step, step+total_dims):
            intensity = (i-step)/total_dims
            faded_color = ColorFade(color, intensity)
            p_paths[target][step+total_dims - i] = faded_color
    return(p_paths)



""" Input: starting rgbw value, ending rgbw value
    Output: individual pixel path p_path"""
def Fade2Color(c1, c2):
    fade_size = 25
    p_path = np.zeros([10, 4])
    for i in range(10):
        p_path[i][:] = c1[:]
    first_downstep = first_upstep = np.zeros(4)
    downsteps = upsteps = np.zeros(4)
    for i in range(4):
        first_downstep[i] = c1[i] % fade_size
        first_upstep[i] = c2[i] % fade_size
        downsteps[i] = c1[i] // fade_size
        upsteps[i] = c2[i] // fade_size
    np.append(p_path, [c1 - first_downstep], axis=0)
    for i in range(fade_size):
        faded_color = c1 - first_downstep - (i * downsteps)
        np.append(p_path, [faded_color], axis=0)
    np.append(p_path, [first_upstep], axis=0)
    for i in range(fade_size):
        brighter_color = first_downstep + (i * upsteps)
        np.append(p_path, [brighter_color], axis=0)
    np.append(p_path, [c2], axis=0)
    return(p_path)


""" Input: pixel number, rgbw value target_color
    Output: a single pixel_path of length max_diff"""
def Walk2Color(pixel, target_color):
    rgbw_is = rgbw_target = rgbw_diff = np.zeros(4)

    for i in range(4):
        rgbw_is[i] = pixel_state[pixel][i]
        rgbw_target[i] = target_color[i]
        rgbw_diff[i] = GetDiff(rgbw_is[i], rgbw_target[i])

    max_diff = np.amax(rgbw_diff)
    pixel_path = np.zeros([max_diff, 4])

    for i in range(max_diff):
        for j in range(4):
            if (rgbw_is[j] < rgbw_target[j]):
                rgbw_is[j] += 1
                pixel_path[i][j] = rgbw_is[j]

            if (rgbw_is[j] < rgbw_target[j]):
                rgbw_is[j] += 1
                pixel_path[i][j] = rgbw_is[j]

            if (rgbw_is[j] == rgbw_target[j]):
                pixel_path[i][j] = rgbw_is[j]

    return(pixel_path)

""" Edits normalized pixel_paths to include random sparkles
    Input: pixel_paths, sparkle color, intensity from (0.0-1.0)
    Output: edited pixel_paths"""
def MoreSparkles(p_paths, target_color, intensity):
    path_size = p_paths[0].shape[0]
    for step in range(path_size):
        if Decision(intensity):
            random_pixel = np.random.randint(total_lights)
            p_paths[random_pixel][step] = target_color
    return (p_paths)

""" Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r."""
def Wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b, 0)

""" using a 3 out-of-sync sine waves to create a rgb rainbow with only one color as input
    use for each pixel of a color state
    Input: single rgb value c, number of steps t, amplitude of sine waves a
    Output: rgb array of size t"""
def WaveCycle(color, steps, a):
    steps_list = np.linspace(0, 8*np.pi, steps)
    max_index = np.argsort(color)[-1]
    mid_index = np.argsort(color)[-2]
    phi_list = np.array([np.pi/2, np.pi/2, np.pi/2])
    phi_list[max_index] = -np.pi/4
    phi_list[mid_index] = np.pi/4
    waves = np.zeros([steps, 4])
    p_path = np.zeros([steps, 4])
    for i in range(steps):
        for j in range(3):
            waves[i][j] = a * np.sin(steps_list[i] + phi_list[j])
            p_path[i][j] = color[j] + waves[i][j]
        second_largest = np.argsort(p_path[i])[-2]
        p_path[i][second_largest] = 0
    return(p_path)

""" Wave walks one pixel towards a target color c2
    Output: set of rgb values for one pixel c_list of length t"""
def Blender(self, c1, c2, t, a):
    steps = np.arange(0, 1, 1/t)
    phi_list = np.array([np.pi/4, 0, np.pi/2])
    waves = c_list = np.empty([3, steps.size])

    for i in range(3):
        waves[i] = a * np.sin(2*np.pi*steps + phi_list[i])
        c_list[i] = c1[i] + waves[i]

        if (np.abs(c_list[i] - c2) < 4):
            c_list[i:] = c2
    return (c_list)

def ShowState(p_state, delay=.005):
    global pixel_state
    p_state.show()
    time.sleep(delay)

def FlattenEdge(p_paths):
    total_steps = p_paths.shape[1]
    final_paths = CreatePixelPaths(total_steps)
    for i in range(total_edges):
        for j in range(edge_size):
            pixel_index = (i * edge_size) + j
            for k in range(total_steps):
                final_paths[pixel_index][k] = p_paths[j][k]
    return(final_paths)

# only works for odd numbered edge_size
def FlattenEdge2(p_paths):
    total_steps = p_paths.shape[1]
    final_paths = CreatePixelPaths(total_steps)
    for i in range(total_edges):
        for j in range(ray_size):
            center_index = i*edge_size + (ray_size - 1)
            for k in range(total_steps):
                final_paths[center_index][k] = p_paths[0][k]
                final_paths[center_index - j][k] \
                    = p_paths[j][k]
                final_paths[center_index + j][k] \
                    = p_paths[j][k]
    return(final_paths)

# overlap should be between(0,1)
# p_paths_arr is a list of p_paths that can vary in step sizes
def BlendPaths(p_paths_arr, overlap=.2):
    total_paths = p_paths_arr.shape[0]
    total_steps = 1
    final_paths = CreatePixelPaths(total_steps)
    for i in range(total_paths - 1):
        path_steps = p_paths_arr[i].shape[1]
        nextpath_steps = p_paths_arr[i+1].shape[1]
        overlapped_steps = int(path_steps * overlap)
        if (overlapped_steps > nextpath_steps):
            overlapped_steps = nextpath_steps
        for j in range(total_lights):
            p_paths_arr[i][j][path_steps:path_steps-overlapped_steps:-1] \
                += p_paths_arr[i+1][j][:overlapped_steps]
        del p_paths_arr[i+1][:][:overlapped_steps]
        np.append(final_paths, p_paths_arr[i], axis=1)
    np.append(final_paths, p_paths_arr[total_paths-1], axis=1)
    return(final_paths)

def ShowPaths(p_paths, delay=.005):
    global pixel_state
    p_paths = NormalizeAll(p_paths)
    total_steps = p_paths.shape[1]
    for i in range(total_steps):
        for j in range(total_lights):
            pixel_state[j] = p_paths[j][i]
        pixel_state.show()
        time.sleep(delay)

### END OF TOOLBOX ###


class Patterns():
    def __init__(self):
        pass

    def TestCycle(self):
        steps = 4
        self.pixel_paths = CreatePixelPaths(4)
        colors = np.zeros([steps,4])
        for j in range(steps):
            colors[j][j] = 255
            for i in range(total_lights):
                self.pixel_paths[i][j] = colors[j]
        ShowPaths(self.pixel_paths, 1)

    def CycleColors(self, colors):
        steps = colors.shape[0]
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(steps):
            for j in range(total_lights):
                self.pixel_paths[j][i] = colors[i]
        return(self.pixel_paths)

    def RainbowCycle(self, wait=.005):
        global pixel_state
        for j in range(255):
            for i in range(total_lights):
                pixel_index = (i * 256 // total_lights) + j
                pixel_state[i] = Wheel(pixel_index & 255)
            pixel_state.show()
            time.sleep(wait)
    
# compatible with all 3 symmetries just change edge value
    def RainbowCycle2(self, wait=.005, edge=0):
        if (edge==1):
            lights = edge_size
        elif (edge==2):
            lights = ray_size
        self.pixel_paths = CreatePixelPaths(255, num_lights=lights)
        for j in range(255):
            for i in range(lights):
                pixel_index = (i * 256 // lights) + j
                self.pixel_paths[i][j] = Wheel(pixel_index & 255)
        return(self.pixel_paths)

    def Raindrops(self, colors, steps=1000, intensity=.3):
        dim_steps = 24
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(steps - dim_steps):
            for j in range(10):
                if Decision(intensity):
                    pixel_index = np.random.randint(0, total_lights)
                    self.pixel_paths[pixel_index][i] = RandomElement(colors)
                    self.pixel_paths = Dimmer(self.pixel_paths,
                                            pixel_index, i, dim_steps)
        return(self.pixel_paths)
        
    def Droplets_edge2(self, steps=2000, intensity=.08, fast=False):
        self.pixel_paths = CreatePixelPaths(steps, num_lights=ray_size)
        bright_path = brighten
        if fast:
            bright_path = brighten_small
        dim_steps = bright_path.shape[0]
        for i in range(steps - 2 * dim_steps):
            if Decision(intensity):
                pixel_index = np.random.randint(0, ray_size)
                count = 0
                while (count < dim_steps):
                    self.pixel_paths[pixel_index][i+count][3] = bright_path[count]
                    self.pixel_paths[pixel_index][i+count+dim_steps][3] = \
                        bright_path[-count - 1]
                    count += 1
        return(self.pixel_paths)

    def Sparkles(self, colors, steps=1000, intensity=.8):
        total_colors = colors.shape[0]
        total_cycles = 20
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(total_cycles):
            self.pixel_paths = \
                MoreSparkles(self.pixel_paths, colors[i % total_colors], intensity)
        return(self.pixel_paths)
        

    def MeteorShower(self, colors, steps=1000, intensity=.4):
        dim_steps = 14
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(steps - 2*dim_steps):
            if Decision(intensity):
                color = RandomElement(colors)
                pixel_index = np.random.randint(0, total_lights)
                self.pixel_paths[pixel_index][i] = color
                self.pixel_paths = Dimmer(self.pixel_paths,
                                        pixel_index, i, dim_steps)
                for j in range(dim_steps):
                    self.pixel_paths[pixel_index-j][i+j] = color
                    self.pixel_paths = Dimmer(self.pixel_paths,
                                            pixel_index-j, i+j, dim_steps)
        return(self.pixel_paths)

    def Snake(self, colors):
        total_colors = colors.shape[0]
        steps = total_lights * total_colors
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(0, steps, total_lights):
            color = RandomElement(colors)
            for j in range(total_lights):
                self.pixel_paths[j][j+i] = color
                self.pixel_paths = Dimmer(self.pixel_paths, j, j+i, 6)
        return(self.pixel_paths)

# Arath's snake game
    def Snake2(self, colors=rainbow):
        total_colors = colors.shape[0]
        steps = (total_colors - 1) * total_lights 
        palette = np.copy(colors)
        np.random.shuffle(palette)
        self.pixel_paths = CreatePixelPaths(steps + total_colors)
        first_color = palette[0]
        for i in range(1, total_colors):
            color = palette[i]
            dot_index = np.random.randint(10, total_lights)
            for head_index in range(total_lights):
                step = (i-1)*(total_lights) + head_index
                if(head_index-i > dot_index):
                    self.pixel_paths[head_index-i][step] = color
                else:
                    self.pixel_paths[dot_index][step] = color
                self.pixel_paths[head_index][step] = first_color
                for j in range(1, i):
                    self.pixel_paths[head_index-j][step] = palette[j]
        for k in range(total_colors):
            for l in range(total_colors):
                if(l<=k):
                    self.pixel_paths[total_lights-k-1+l][steps-1+l] = \
                        self.pixel_paths[total_lights-k-1][steps-1]
        return(self.pixel_paths)

    def Blinker(self, colors=rainbow):
        total_colors = colors.shape[0]
        bright_path = brighten_small
        dim_step = bright_path.shape[0]
        steps = 2*dim_step*total_colors
        self.pixel_paths = CreatePixelPaths(steps)
        for i in range(total_colors):
            color = colors[i]
            first_upstep = i * (2* dim_step)
            first_downstep = first_upstep + dim_step
            for j in range(dim_step):
                up_multiplier = brighten_small[j] / 255
                down_multiplier = brighten_small[-j - 1] / 255
                for k in range(total_lights):
                    self.pixel_paths[k][first_upstep + j] = up_multiplier * color
                    self.pixel_paths[k][first_downstep + j] = down_multiplier * color
        return(self.pixel_paths)

# symmetric for edge_size = 9    
# output: every other light lit then spun
    def CandyCane(self, color_0=rainbow[0], color_1=rainbow[3], \
                    color_2=rainbow[4], total_steps=270):
        path_instance = CreatePixelPaths(1, num_lights=edge_size)
        for i in range(0, edge_size, 3):
            switch = int(i % 9 / 3)
            color = locals()["color_" + str(switch)]
            path_instance[i] = color
        self.pixel_paths = Roll(path_instance, steps=total_steps)
        return(self.pixel_paths)
        
    def FadeTest(self):
        steps = 56
        color_1 = np.array([28, 114, 200, 0])
        color_2 = np.array([200, 114, 28, 0])
        self.pixel_paths = CreatePixelPaths(steps)
        p_path = Fade2Color(color_1, color_2)
        for i in range(total_lights):
            np.append(self.pixel_paths[i], p_path, axis=0)
        print(self.pixel_paths)
        return(self.pixel_paths)

    def RainbowOut(self, repeat=1):
        steps = 7 + ray_size
        total_steps = steps * repeat
        self.pixel_paths = CreatePixelPaths(total_steps, num_lights=ray_size)
        for j in range(steps):
            for k in range(repeat):
                self.pixel_paths[0][(j*k)+k] = rainbow[j % 7]
        for i in range(edge_size):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j - (30*i)][k] = self.pixel_paths[0][j][k]
        return(self.pixel_paths)

    def ColorPulse(self, steps=500):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps)
        steps_list = np.linspace(0, 8*np.pi, steps).astype('f8')
        for i in range(total_lights):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j][k] = \
                        a * (np.sin(steps_list[j] + ((np.pi/3) * float(k))))**2
        return(self.pixel_paths)

# 3 offset sine waves
    def ColorWhip(self, steps=500):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps)
        steps_list = np.linspace(0, 4*np.pi, steps).astype('f8')
        phi_step = np.pi / total_lights
        for i in range(total_lights):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j][k] = \
                        a * (np.sin(steps_list[j] + (phi_step * float(i)) + ((np.pi/3) * float(k))))**2
        return(self.pixel_paths)

    def ColorWhipEdge(self, steps=500):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps, num_lights=edge_size)
        steps_list = np.linspace(0, 4*np.pi, steps).astype('f8')
        phi_step = np.pi / (4*(edge_size - 1))
        for i in range(edge_size):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j][k] = \
                        a * (np.sin(steps_list[j] + (phi_step * i) + ((np.pi/3) * k)))**2
        final_paths = FlattenEdge(self.pixel_paths)
        return(final_paths)

    def ColorWhipEdgeTest(self, steps=1000):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps, num_lights=edge_size)
        steps_list = np.linspace(0, 4*np.pi, steps).astype('f8')
        phi_step = np.pi / (4*(edge_size - 1))
        for i in range(edge_size):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j][k] = \
                        (a) * ( \
                        (2/np.pi)*np.sin((steps_list[j] + (phi_step * i) + ((np.pi/3) * k))) + \
                        (2/(3*np.pi))*np.sin(3* (steps_list[j] + (phi_step * i) + ((np.pi/3) * k))) + \
                        (2/(5*np.pi))*np.sin(5 * (steps_list[j] + (phi_step * i) + ((np.pi/3) * k))) + \
                        (2/(7*np.pi))*np.sin(7 * (steps_list[j] + (phi_step * i) + ((np.pi/3) * k))) \
                        )
        final_paths = FlattenEdge(self.pixel_paths)
        return(final_paths)

    def ColorWhipEdge2(self, steps=500):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps, num_lights=ray_size)
        steps_list = np.linspace(0, 4*np.pi, steps).astype('f8')
        phi_step = np.pi / total_lights
        for i in range(ray_size):
            for j in range(steps):
                for k in range(3):
                    self.pixel_paths[i][j][k] = \
                        a * (np.sin(steps_list[j] + (phi_step * i) + ((np.pi/3) * k)))**2
                second_largest = np.argsort(self.pixel_paths[i][j])[-2]
                self.pixel_paths[i][j][second_largest] = 0
        final_paths = FlattenEdge2(self.pixel_paths)

        return(final_paths)

    def ColorWhip3(self, steps=500):
        a = 254
        self.pixel_paths = CreatePixelPaths(steps)
        phi_step = np.pi / total_lights
        for i in range(total_lights):
            for k in range(3):
                self.pixel_paths[i][0][k] = \
                    a * (np.sin((phi_step * i) + ((np.pi/3) * k)))**2
            second_largest = np.argsort(self.pixel_paths[i][0])[-2]
            self.pixel_paths[i][0][second_largest] = 0
        for j in range(steps):
            self.pixel_paths[:][j] = \
                np.roll(self.pixel_paths[:][0], j % total_lights, axis=0)
        return(self.pixel_paths)

    """ Input: rgb array of colors to be initial state such as the globals neons and pastels"""
    def ChromaticDance(self, colors, steps=500):
        total_colors = colors.shape[0]
        self.path_instance = CreatePixelPaths(1)
        segment_size = total_lights // total_colors
        if (segment_size < 2):
            segment_size = 2
        color = colors[0]
        for i in range(total_lights):
            if (i % segment_size == 0):
                c_index = (i // segment_size) % total_colors
                color = colors[c_index]
            self.path_instance[i] = color
        self.pixel_paths = Roll(self.path_instance, steps=500)
        return(self.pixel_paths)
