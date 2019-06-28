from master import *

strip = Patterns()

Path1 = strip.Sparkles(white)
Path2 = strip.Sparkles(oranges)
Path3 = strip.Sparkles(pinks)
Path4 = strip.Sparkles(greens)
Path5 = strip.Sparkles(blues)

Paths = np.array([Path1, Path2, Path3, Path4, Path5])
BlendedPath = BlendPaths(Paths)

while True:
    ShowPaths(BlendedPath)
