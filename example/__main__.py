from os.path import dirname, realpath
from sys import path

path.append(dirname(dirname(realpath(__file__))))


from random import randint, random
from typing import List, Callable

from graphical_engine import GraphicalParticle, Universe
from laws import Gravity, Merge
from particles import Atom
from physics import Number, Law


def main(
    particle_nbr: Number,
    special_particles: Callable[..., List[GraphicalParticle]],
    particles_init_mass: Callable[..., Number],
    particles_init_position_range: Callable[[Universe], List[Number]],
    particles_init_velocity: Callable[..., List[Number]],
    laws: List[Law],
    draw_trajectory: bool,
    sync_time: bool,
    zoom_level: Number,
):
    universe = Universe(zoom_level=zoom_level, draw_trajectory=draw_trajectory, sync_time=sync_time)
    for _ in range(particle_nbr):
        universe.add_unit(
            Atom(universe, particles_init_mass(), particles_init_position_range(universe), particles_init_velocity())
        )
    for particle in special_particles(universe):
        universe.add_unit(particle)
    for law in laws:
        universe.laws.append(law)
    universe.loop()


options = {
    "mass": {"1": lambda: 1, "1to10": lambda: randint(1, 10)},
    "position": {
        "in_screen": lambda u: [randint(-u.width / 2, u.width / 2), randint(-u.height / 2, u.height / 2)],
        "in_twice_screen": lambda u: [randint(-u.width, u.width), randint(-u.height, u.height)],
        "in_half_screen": lambda u: [randint(-u.width / 4, u.width / 4), randint(-u.height / 4, u.height / 4)],
        "in_2_3rd_of_screen": lambda u: [randint(-u.width / 3, u.width / 3), randint(-u.height / 3, u.height / 3)],
    },
    "velocity": {
        "0": lambda: [0, 0],
        "-0.01": lambda: [-0.01, -0.01],
        "rand_0.5": lambda: [(random() - 0.5), (random() - 0.5)],
        "rand_0.002": lambda: [randint(-1, 1) / 500, randint(-1, 1) / 500],
    },
    "special_particles": {
        "centered_big_star": lambda u: [Atom(u, 4000, [0, 0], [0, 0])],
        "none": lambda u: [],
        "centered_small_star": lambda u: [Atom(u, 4000, [0, 0], [0, 0])],
        "four_star": lambda u: [
            Atom(u, 500, [100, 100], [0, 0]),
            Atom(u, 500, [-100, 100], [0, 0]),
            Atom(u, 500, [100, -100], [0, 0]),
            Atom(u, 500, [-100, -100], [0, 0]),
        ],
    },
    "laws": {"realistic": [Gravity(), Merge()], "pure_gravity": [Gravity()]},
}


if __name__ == "__main__":
    main(
        200,
        options["special_particles"]["none"],
        options["mass"]["1"],
        options["position"]["in_half_screen"],
        options["velocity"]["0"],
        # options["velocity"]["rand_0.5"],
        options["laws"]["realistic"],
        draw_trajectory=True,
        sync_time=False,
        zoom_level=1,
    )
