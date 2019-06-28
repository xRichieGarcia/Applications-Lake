from master import *

strip = Patterns()

path = strip.CandyCane()
reverse_path = np.copy(path[::-1])
wait = .005

final_path = FlattenEdge(path)
final_r_path = FlattenEdge(reverse_path)

while True:
    ShowPaths(final_path, delay=wait)
    time.sleep(wait)
    ShowPaths(final_r_path)
    time.sleep(wait, delay=wait)