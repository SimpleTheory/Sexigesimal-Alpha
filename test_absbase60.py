import base_60_math

a = base_60_math.AbsBase60.from_integer(346)
b = base_60_math.AbsBase60.from_integer(643)
c = base_60_math.AbsBase60.from_integer(346)


def test_abs_ge():
    assert b >= a
    assert a >= c

    assert not (a >= b)


def test_abs_le():
    assert a <= b
    assert a <= c

    assert (b <= a) is False


def test_abs_eq():
    assert not (b == a)
    assert a == c


def test_abs_gt():
    assert b > a

    assert not (a > c)
    assert not (a > b)


def test_abs_lt():
    assert a < b

    assert (a < c) is False
    assert not (b < a)
