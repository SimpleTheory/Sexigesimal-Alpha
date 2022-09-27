import base_60_math


def reverse(x): return x[::-1]

###################


def test_euclidean_division():
    assert base_60_math.euclidean_division(60, 37) == (1, 60 - 37,)
    assert base_60_math.euclidean_division(40, 50) == (0, 40,)


def test_base60_unit_addition():
    assert base_60_math.base60_unit_addition(3, 59) == (2, 1,)
    assert base_60_math.base60_unit_addition(5, 4) == (9, 0,)


def test_base60_unit_subtraction():
    assert base_60_math.base60_unit_subtraction(3, 59) == (4, -1,)
    assert base_60_math.base60_unit_subtraction(5, 4) == (1, 0,)

#####################


def test_add_items_in_list_number():
    a = base_60_math.Base60.from_commas('1,2,3,4,5')
    b = base_60_math.Base60.from_commas('59,59,3,5')
    c = base_60_math.add_items_in_list_number(a.number, b.number)
    # [0, 59, 59, 3, 5]
    #  [1, 2, 3, 4, 5]
    #  [2, 2, 2, 7,10]
    assert c == [2, 2, 2, 7, 10]
    assert base_60_math.add_items_in_list_number([59, 59, 59, 59], [59, 59, 59, 59]) == [1, 59, 59, 119 - 60, 118 - 60]


def test_add_items_in_list_fraction():
    assert base_60_math.add_items_in_list_fraction([30, 40, 20], [5, 5, 40]) == ([35, 46, 0], 0,)

    a = base_60_math.Base60.from_commas('1,2,3,4,5')
    b = base_60_math.Base60.from_commas('59,59,3,5')
    c = base_60_math.add_items_in_list_fraction(a.number, b.number)
    #  [59,59,3, 5, 0]
    #  [1, 2, 3, 4, 5]
    # 1[1, 1, 6, 9, 5]
    assert c == ([1, 1, 6, 9, 5], 1,)


def test_subtraction_number():
    a = base_60_math.Base60.from_commas('1,2,3,4,5')
    b = base_60_math.Base60.from_commas('59,59,3,5')
    c = base_60_math.subtract_number(a.number, b.number)
    # [0, 59, 59, 3, 5]
    #  [1, 2, 3, 4, 5]
    #  [2, 2, 2, 7,10]
    assert c == [2, 4, 1, 0]
    assert base_60_math.subtract_number([59, 59, 59, 59], [59, 59, 59, 59]) == [0]


def test_subtraction_fraction():
    assert base_60_math.add_items_in_list_fraction([30, 40, 20], [5, 5, 40]) == ([35, 46, 0], 0,)

    a = base_60_math.Base60.from_commas('1,2,3,4,5')
    b = base_60_math.Base60.from_commas('59,59,3,5')
    c = base_60_math.add_items_in_list_fraction(a.number, b.number)
    #  [59,59,3, 5, 0]
    #  [1, 2, 3, 4, 5]
    # 1[1, 1, 6, 9, 5]
    assert c == ([1, 1, 6, 9, 5], 1,)

###############


def test_comparator_truthy():
    assert base_60_math.comparator([30, 27], [59]) == (True, False,)
    assert base_60_math.comparator([30, 27], [19, 39]) == (True, False,)
    assert base_60_math.comparator([30, 27], [30, 26]) == (True, False,)
    assert base_60_math.comparator([30, 27], [30, 27]) == (False, True,)


def test_comparator_falsey():
    assert base_60_math.comparator([59], [30, 27]) == (False, False,)
    assert base_60_math.comparator([1, 59], [30, 27]) == (False, False,)
    assert base_60_math.comparator([30, 26], [30, 27]) == (False, False,)


def test_prep_compare():
    a = base_60_math.prep_compare([1, 2, 1, 1], [1, 1], True)
    b = base_60_math.prep_compare([1, 2, 1, 1], [1, 1], False)
    assert b == ([1, 2, 1, 1], [1, 1, 0, 0],)
    assert a == ([1, 2, 1, 1], [0, 0, 1, 1],)

    assert base_60_math.prep_compare([1, 2, 1, 1], [1, 1], True, True) == tuple([reverse(i) for i in a])
    assert base_60_math.prep_compare([1, 2, 1, 1], [1, 1], False, True) == tuple([reverse(i) for i in b])