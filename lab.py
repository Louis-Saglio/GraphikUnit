from math import sqrt


def divide(a, b):
    if b == 0:
        if a == 0:
            return 1
        return float("inf")
    return a / b


def compute(origin, direction, distance):
    return (
        (
            origin[0]
            + (direction[0] - origin[0])
            * distance
            / (sqrt((origin[0] - direction[0]) ** 2 + (origin[1] - direction[1]) ** 2))
        ),
        (
            origin[1]
            + (direction[1] - origin[1])
            * distance
            / (sqrt((origin[0] - direction[0]) ** 2 + (origin[1] - direction[1]) ** 2))
        ),
    )
