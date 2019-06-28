from master import *

strip = Patterns()

cycle_size = 400

path1 = strip.ColorPulse(steps=cycle_size)
path2 = strip.ColorWhip(steps=cycle_size)
path3 = strip.Raindrops(white, steps=cycle_size)
path4 = strip.Raindrops(oranges, steps=cycle_size)
path5 = strip.Raindrops(pinks, steps=cycle_size)
path6 = strip.Raindrops(greens, steps=cycle_size)
path7 = strip.Raindrops(blues, steps=cycle_size, intensity=.8)
path8 = strip.Raindrops(rainbow, steps=cycle_size, intensity=.8)
path9 = strip.MeteorShower(pastels, intensity=.8, steps=cycle_size)
path10 = strip.MeteorShower(neons, intensity=.8, steps=cycle_size)
path11 = strip.MeteorShower(rainbow, intensity=.8, steps=cycle_size)
path12 = strip.MeteorShower(greens, intensity=.8, steps=cycle_size)
path13 = strip.MeteorShower(blues, intensity=.8, steps=cycle_size)
path14 = strip.MeteorShower(pinks, intensity=.8, steps=cycle_size)
path15 = strip.MeteorShower(oranges, intensity=.8, steps=cycle_size)

# Change when new paths are added
total_paths = 15
wait_list = [.01, .02, .04, .05, .08]

while True:
    index = np.random.randint(1, total_paths + 1)
    wait = np.random.choice(wait_list)
    path = locals()["path" + str(index)]
    ShowPaths(path)
    time.sleep(wait)