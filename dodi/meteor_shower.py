from master import *

strip = Patterns()

cycle_size = 1000

path1 = strip.MeteorShower(pastels, intensity=.8, steps = cycle_size)
path2 = strip.MeteorShower(neons, intensity=.8, steps=cycle_size)
path3 = strip.MeteorShower(rainbow, intensity=.8, steps=cycle_size)
path4 = strip.MeteorShower(greens, intensity=.8, steps=cycle_size)
path5 = strip.MeteorShower(blues, intensity=.8, steps=cycle_size)
path6 = strip.MeteorShower(pinks, intensity=.8, steps=cycle_size)
path7 = strip.MeteorShower(oranges, intensity=.8, steps=cycle_size)

# Change when new paths are added
total_paths = 7
wait_list = [.001, .005, .008]

while True:
    index = np.random.randint(1, total_paths, 2)
    wait = np.random.choice(wait_list)
    
    bot_path = locals()["path" + str(index[0])]
    top_path = locals()["path" + str(index[1])]

    f_path = top_path + bot_path
    ShowPaths(f_path, delay=wait)
    time.sleep(wait)