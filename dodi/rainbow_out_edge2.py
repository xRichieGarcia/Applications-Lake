## Testing RainbowOut
from master import *

strip = Patterns()

Path1 = strip.RainbowOut()
Path2 = strip.RainbowOut(repeat=8)

Path1 = FlattenEdge2(Path1)
Path2 = FlattenEdge2(Path2)

while True:
    ShowPaths(Path1)
    time.sleep(2)
    ShowPaths(Path2)
    time.sleep(2)