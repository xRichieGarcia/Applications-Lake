from master import *

strip = Patterns()

path1 = strip.Sparkles(white, steps=100)
path2 = strip.Sparkles(oranges, steps=100)
path3 = strip.Sparkles(pinks, steps=100)
path4 = strip.Sparkles(greens, steps=100)
path5 = strip.Sparkles(blues, steps=100)

# Change when new paths are added
total_paths = 5
wait= .001

while True:
    index = np.random.randint(1, total_paths + 1)
    path = locals()["path" + str(index)]
    ShowPaths(path)
    time.sleep(wait)
