from master import *

strip = Patterns()

path1 = strip.Snake(sunset)
path2 = strip.Snake2(rainbow)
wait = .005

while True:
    ShowPaths(path1)
    time.sleep(wait)
    ShowPaths(path2)
    time.sleep(wait)