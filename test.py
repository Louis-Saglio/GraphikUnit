from lab import compute


def test1():
    assert compute((0, 0), (8, 6), 5) == (4.0, 3.0)
    assert compute((8, 6), (0, 0), 5) == (4.0, 3.0)


def test2():
    assert compute((0, 0), (-8, -6), 5) == (-4.0, -3.0)
    assert compute((-8, -6), (0, 0), 5) == (-4.0, -3.0)


def test3():
    assert compute((0, 0), (-8, 6), 5) == (-4.0, 3.0)
    assert compute((-8, 6), (0, 0), 5) == (-4.0, 3.0)


def test4():
    assert compute((0, 0), (8, -6), 5) == (4.0, -3.0)
    assert compute((8, -6), (0, 0), 5) == (4.0, -3.0)


def test5():
    assert compute((0, 0), (16, 12), 5) == (4.0, 3.0)
    assert compute((16, 12), (0, 0), 5) == (12.0, 9.0)


def test6():
    assert compute((0, 0), (-16, -12), 5) == (-4.0, -3.0)
    assert compute((-16, -12), (0, 0), 5) == (-12.0, -9.0)


def test7():
    assert compute((0, 0), (-16, 12), 5) == (-4.0, 3.0)
    assert compute((-16, 12), (0, 0), 5) == (-12.0, 9.0)


def test8():
    assert compute((0, 0), (16, -12), 5) == (4.0, -3.0)
    assert compute((16, -12), (0, 0), 5) == (12.0, -9.0)
