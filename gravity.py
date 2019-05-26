from math import sqrt
from random import randint
from typing import Tuple, Iterable

from lab import divide
from lib import MovableUnitMixin, Motherboard, Number, Law


class Particle(MovableUnitMixin):
    def __init__(self, position: Tuple[Number, Number], mass: Number):
        self._position = position
        self.mass = mass
        self.velocity = 0
        self._color = [randint(0, 255) for _ in range(3)]

    @property
    def position(self) -> Tuple[Number, Number]:
        return self._position

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        return sqrt(self.mass * 3), sqrt(self.mass * 3)

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        # print(self.velocity)
        velocity = abs(self.velocity)
        return 255, min(255, 0 + sqrt(velocity * 20000)), min(255, 0 + sqrt(velocity * 20000))

    def run(self, total_time: int, **kwargs):
        pass

    def apply_force(self, force: Number, direction: Tuple[Number, Number]):
        self.velocity += force / self.mass
        self.move_toward(direction, self.velocity)

    @position.setter
    def position(self, value):
        self._position = value


class Gravity(Law):
    g = 7 * 10 ** -3

    def apply(self, units: Iterable[Particle]):
        for unit in units:
            for other_unit in units:
                if unit != other_unit:
                    distance = unit.distance_with(other_unit)
                    force = divide((self.g * unit.mass * other_unit.mass), distance ** 2)
                    if distance > 30:
                        unit.apply_force(
                            force, other_unit.position
                        )
                    else:
                        unit.apply_force(-force, other_unit.position)


class Reaction(Law):
    anti_g = -7e0

    def apply(self, units: Iterable[Particle]):
        for unit in units:
            for other_unit in units:
                if unit != other_unit:
                    distance = unit.distance_with(other_unit)
                    unit.apply_force(
                        self.anti_g * divide(unit.mass * other_unit.mass, distance * distance), unit.position
                    )


universe = Motherboard()
universe.laws.append(Gravity())
# universe.laws.append(Reaction())

for _ in range(100):
    universe.add_unit(
        Particle(
            (randint(-universe.width / 2, universe.width / 2), randint(-universe.height / 2, universe.height / 2)), 1
        )
    )

universe.loop()
