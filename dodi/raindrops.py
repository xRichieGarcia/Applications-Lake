from master import *

strip = Patterns()

path = strip.Raindrops(sunset)
wait = .005

while True:
    ShowPaths(path)
    time.sleep(wait)