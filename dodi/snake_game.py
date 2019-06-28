from master import *

strip = Patterns()

path = strip.Snake2()
path2 = strip.Snake2(colors=pastels)
wait=.005

while True:
    ShowPaths(path, delay=wait)
    time.sleep(wait)
    ShowPaths(path2, delay=wait)
    time.sleep(wait)