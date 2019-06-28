from master import *

strip = Patterns()

cycle_size = 1000

path = strip.MeteorShower(rainbow, intensity=.8, steps=cycle_size)
back_path = np.flip(path, axis=1)

wait = .005

while True:
    f_path = path
    
    if Decision(.2):
        f_path += back_path

    ShowPaths(f_path)
    time.sleep(wait)