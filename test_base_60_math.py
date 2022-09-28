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

def test_add_items_in_list_number2():
    a = [7,17]
    b = [6]
    assert base_60_math.add_items_in_list_number(a, b) == [7,23]
    assert base_60_math.add_items_in_list_number(b, a) == [7,23]

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
    # 30 40 20
    # 5   5 40
    # 25 34 40
    assert base_60_math.subtract_fraction([30, 40, 20], [5, 5, 40]) == ([25, 34, 40], 0,)
    assert base_60_math.subtract_fraction([5, 5, 40], [30, 40, 20]) == ([25, 34, 40], -1,)

    a = base_60_math.Base60.from_commas('1,2,3,4,5')
    b = base_60_math.Base60.from_commas('59,59,3,5')
    c = base_60_math.subtract_fraction(a.number, b.number)
    #  [59,59,3, 5, 0]e
    #  [1, 2, 3, 4, 5]
    # 1[1, 1, 6, 9, 5]
    assert c == ([58, 57, 0, 0, 55], -1,)


def test_lazy_sub():
    a = base_60_math.lazy_subtraction(base_60_math.Base60.from_commas('4,16;18'),
                                      base_60_math.Base60.from_commas('1,12;6'))
    b = base_60_math.lazy_subtraction(base_60_math.Base60.from_commas('1,12;6'),
                                      base_60_math.Base60.from_commas('4,16;18'))
    expected = base_60_math.Base60.from_commas('3,4;12')
    assert str(a[0]) == str(expected)
    assert str(b[0]) == str(expected)
    assert a[1] is False
    assert b[1] is True


def test_lazy_add():
    a = base_60_math.AbsBase60.from_commas('4,16;54')
    b = base_60_math.AbsBase60.from_commas('4,0;7')
    c = base_60_math.lazy_addition(a, b)
    assert str(c) == str('8,17;1')
    assert str(c) == str(base_60_math.lazy_addition(b, a))

def test_lazy_add_int():
    int_ = 6+437
    a = base_60_math.AbsBase60.from_integer(6)
    b = base_60_math.AbsBase60.from_integer(437)
    expected = base_60_math.AbsBase60.from_integer(int_)
    assert base_60_math.lazy_addition(a, b) == base_60_math.lazy_addition(b, a)
    assert base_60_math.lazy_addition(a, b) == expected

###############
def test_base60_str():
    a = base_60_math.Base60.from_commas('3,4;12')
    assert str(a) == '3,4;12'


def test_comparator_truthy():
    assert base_60_math.comparator([30, 27], [59]) == (True, False,)
    assert base_60_math.comparator([30, 27], [19, 39]) == (True, False,)
    assert base_60_math.comparator([30, 27], [30, 26]) == (True, False,)
    assert base_60_math.comparator(reverse([20, 40, 30]), reverse([40, 5, 5]), True) == (True, False,)
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


def test_int_to_base():
    a = base_60_math.int_to_base(478, 60)
    assert a == [7, 58]


def test_sort():
    init_ = [base_60_math.AbsBase60.from_integer(i) for i in [661, 409, 7236, 1976, 2764]]
    final = [base_60_math.AbsBase60.from_integer(i) for i in sorted([661, 409, 7236, 1976, 2764])]
    assert base_60_math.sort(init_) == final
