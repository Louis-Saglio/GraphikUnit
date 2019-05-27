from lab import compute, Force, sum_forces


def test1():
    assert compute(Force((0, 0), (8, 6), 5)) == (4.0, 3.0)
    assert compute(Force((8, 6), (0, 0), 5)) == (4.0, 3.0)


def test2():
    assert compute(Force((0, 0), (-8, -6), 5)) == (-4.0, -3.0)
    assert compute(Force((-8, -6), (0, 0), 5)) == (-4.0, -3.0)


def test3():
    assert compute(Force((0, 0), (-8, 6), 5)) == (-4.0, 3.0)
    assert compute(Force((-8, 6), (0, 0), 5)) == (-4.0, 3.0)


def test4():
    assert compute(Force((0, 0), (8, -6), 5)) == (4.0, -3.0)
    assert compute(Force((8, -6), (0, 0), 5)) == (4.0, -3.0)


def test5():
    assert compute(Force((0, 0), (16, 12), 5)) == (4.0, 3.0)
    assert compute(Force((16, 12), (0, 0), 5)) == (12.0, 9.0)


def test6():
    assert compute(Force((0, 0), (-16, -12), 5)) == (-4.0, -3.0)
    assert compute(Force((-16, -12), (0, 0), 5)) == (-12.0, -9.0)


def test7():
    assert compute(Force((0, 0), (-16, 12), 5)) == (-4.0, 3.0)
    assert compute(Force((-16, 12), (0, 0), 5)) == (-12.0, 9.0)


def test8():
    assert compute(Force((0, 0), (16, -12), 5)) == (4.0, -3.0)
    assert compute(Force((16, -12), (0, 0), 5)) == (12.0, -9.0)


def test9():
    assert compute(Force((3, 4), (6, 8), -5)) == (0, 0)
    assert compute(Force((6, 8), (3, 4), -5)) == (9, 12)


def test_sum_forces1():
    assert sum_forces([Force((0, 0), (3, 4), 2), Force((0, 0), (3, 4), 2)]) == Force((0, 0), (0, 0), 0)


def test_sum_forces2():
    assert sum_forces([Force((0, 0), (3, 4), 2), Force((0, 0), (-3, -4), 2)]) == Force((0, 0), (0, 0), 0)


def test_sum_forces3():
    assert sum_forces([Force((0, 0), (3, 4), 5), Force((3, 4), (0, -4), 4)]) == Force((0, 0), (0, 0), 4)
