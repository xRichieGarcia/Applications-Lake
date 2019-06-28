from master import *

strip = Patterns()

path1 = strip.Blinker()
wait = .005

while True:
    ShowPaths(path1)
    time.sleep(wait)
