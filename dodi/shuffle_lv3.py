from master import *

strip = Patterns()

cycle_size = 80

path1 = strip.ColorPulse(steps=cycle_size)
path2 = strip.ColorWhip(steps=cycle_size)
path3 = strip.Sparkles(white, steps=cycle_size)
path4 = strip.Sparkles(oranges, steps=cycle_size)
path5 = strip.Sparkles(pinks, steps=cycle_size)
path6 = strip.Sparkles(greens, steps=cycle_size)
path7 = strip.Sparkles(blues, steps=cycle_size)
path8 = strip.Sparkles(rainbow, steps=cycle_size)
path9 = strip.MeteorShower(pastels, intensity=.8, steps=cycle_size)
path10 = strip.MeteorShower(neons, intensity=.8, steps=cycle_size)
path11 = strip.MeteorShower(rainbow, intensity=.8, steps=cycle_size)
path12 = strip.MeteorShower(greens, intensity=.8, steps=cycle_size)
path13 = strip.MeteorShower(blues, intensity=.8, steps=cycle_size)
path14 = strip.MeteorShower(pinks, intensity=.8, steps=cycle_size)
path15 = strip.MeteorShower(oranges, intensity=.8, steps=cycle_size)

Path1 = path4 + path7
Path2 = path5 + path6
Path3 = path8
Path4 = path9 + path11[::-1]
Path5 = path12 + path14[::-1]
Path6 = path13 = path15[::-1]
Path7 = path9 + path3 + path3[::-1]

# Change when new paths are added
total_paths = 7
wait_list = [.001, .005, .008]

while True:
    bot_index = np.random.randint(9, high=16)
    top_index = np.random.randint(1, total_paths + 1)
    wait = np.random.choice(wait_list)
    
    bot_Path = locals()["path" + str(bot_index)]
    top_Path = locals()["Path" + str(top_index)]

    Path = top_Path + bot_Path
    ShowPaths(Path)
    time.sleep(wait)