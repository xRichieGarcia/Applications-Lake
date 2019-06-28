from master import *

strip = Patterns()

path = strip.Droplets_edge2(fast=True)
wait = .005

final_path = FlattenEdge2(path)

while True:
    ShowPaths(final_path, delay=wait)
    time.sleep(wait)