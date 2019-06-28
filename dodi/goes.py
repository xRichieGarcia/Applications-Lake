from master import *

strip = Patterns()

path1 = strip.Raindrops(white, steps=40)
path2 = strip.Sparkles(white, steps=40, intensity=.8)
sum_path12 = path1 + path2
path3 = strip.Snake(white)
path4 = strip.MeteorShower(white, steps=200)
path5 = strip.MeteorShower(white, steps=200, intensity=.8)
sum_path45 = path4 + path5


ShowPaths(path1, delay=.02)
ShowPaths(path1, delay=.01)
ShowPaths(path1, delay=.009)
ShowPaths(path1, delay=.008)
ShowPaths(path1, delay=.007)
ShowPaths(path2, delay=.005)
ShowPaths(sum_path12, delay=.001)

ShowPaths(path3, delay=.001)

ShowPaths(path4, delay=.005)
ShowPaths(path5, delay=.001)
ShowPaths(path5, delay=.001)
ShowPaths(sum_path45, delay=.001)
ShowPaths(sum_path12, delay=.001)
ShowPaths(path1, delay=.001)
ShowPaths(path1, delay=.009)
ShowPaths(path1[:][:12], delay=.05)