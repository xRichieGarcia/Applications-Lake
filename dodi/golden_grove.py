from master import *

strip = Patterns()

cycle_size = 400

path1 = strip.Raindrops(gold, steps=cycle_size)
path2 = strip.MeteorShower(gold, intensity=.8, steps=cycle_size)
path3 = strip.Blinker(colors=gold)


wait = .005
while True:
    ShowPaths(path1)
    time.sleep(wait)
    ShowPaths(path2)
    time.sleep(wait)
    ShowPaths(path3)
    time.sleep(wait)