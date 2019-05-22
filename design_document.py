import time
from typing import Any, Tuple

from main import Motherboard, Unit, Number

map_ = Motherboard(1500, 1000)


class CustomUnit(Unit):
    @property
    def position(self) -> Tuple[Number, Number]:
        return 745, 495

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        return 5, 5

    @property
    def color(self) -> Any:
        return 255, 255, 255


unit1 = CustomUnit()
map_.add_unit(unit1)

map_.display()

# unit1.move_toward((800, 55), 42)

# map_.refresh()

while True:
    try:
        time.sleep(0.01)
    except KeyboardInterrupt:
        break
