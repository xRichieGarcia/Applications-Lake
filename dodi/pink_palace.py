from master import *

strip = Patterns()

pink = np.array([255, 10, 203, 0])
steps = 1000

path = CreatePixelPaths(steps)
path = MoreSparkles(path, pink, .3)
path = MoreSparkles(path, pink, .8)
path = MoreSparkles(path, pink, .6)

while True:
    ShowPaths(path)
