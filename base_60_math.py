class Base60:
    def __init__(self, number, fraction=None):
        self.number: list = number
        self.fraction: list = fraction

    @classmethod
    def from_commas(cls, commas: str):
        if ';' in commas:
            number, fractions = commas.split(';', 1)
            return cls([int(i) for i in number.split(',')], [int(i) for i in number.split(',')])
        else:
            return cls([int(i) for i in commas.split(',')])

    @classmethod
    def from_code(cls):
        pass

    @classmethod
    def from_decimal(cls):
        pass

    @classmethod
    def from_binary(cls):
        pass


###################
def swap(x, y): return y, x,


# ----
def base60_unit_addition(num1, num2):
    temp = num1 + num2
    q, m = euclidean_division(temp, 60)
    return m, q


def base60_unit_subtraction(subtractee, subtractor):
    holdover = 0
    if subtractee < subtractor:
        subtractee += 60
        holdover = -1
    return (subtractee - subtractor), holdover


def euclidean_division(dividend, divisor):
    quotient = dividend // divisor
    mod = dividend % divisor
    return quotient, mod


#################
def prep_compare(l1, l2, number=True, reversed_=False):
    rl1 = l1[:]
    rl2 = l2[:]
    len_diff = len(rl1) - len(rl2)
    if number:
        if len_diff > 0:
            rl2 = [0 for _ in range(len_diff)] + rl2
        elif len_diff < 0:
            rl1 = [0 for _ in range(len_diff)] + rl1
    else:
        if len_diff > 0:
            rl2.extend([0 for _ in range(len_diff)])
        elif len_diff < 0:
            rl1.extend([0 for _ in range(len_diff)])

    if reversed_:
        rl1.reverse()
        rl2.reverse()

    return rl1, rl2


def comparator(self, other, fraction=False) -> tuple[bool, bool]:
    """
    Greater than operator with additional == value to be a base for all operators

    :param fraction: True if we are dealing with a fraction
    :param self: List which is supposed to be greater
    :param other: List which is supposed to be smaller
    :return: (l1 > l2, l1 == l2)
    """
    if fraction:
        self, other = prep_compare(self, other, False)
    else:
        if len(self) > len(other):
            return True, False
        elif len(other) > len(self):
            return False, False

    for i in zip(self, other):
        if i[0] > i[1]:
            return True, False
        elif i[1] > i[0]:
            return False, False

    return False, True


###################
def add_items_in_list_number(l1, l2):
    rl1, rl2 = prep_compare(l1, l2, True, True)

    added_list = []
    mod = 0
    for i in zip(rl1, rl2):
        answer, temp = base60_unit_addition(*i)
        answer += mod
        mod = temp
        added_list.append(answer)
    added_list.reverse()
    if mod:
        added_list.insert(0, mod)
    return added_list


def add_items_in_list_fraction(l1, l2):
    rl1, rl2 = prep_compare(l1, l2, False, True)

    added_list = []
    mod = 0
    for i in zip(rl1, rl2):
        answer, temp = base60_unit_addition(*i)
        answer += mod
        mod = temp
        added_list.append(answer)
    added_list.reverse()

    return added_list, mod


# ----
def subtract_number(l1, l2):
    gr, eq = comparator(l1, l2)
    if eq:
        return [0]

    rl1, rl2 = prep_compare(l1, l2, True, True)
    if not gr:
        rl1, rl2 = swap(rl1, rl2)

    added_list = []
    mod = 0
    for i in zip(rl1, rl2):
        answer, temp = base60_unit_subtraction(*i)
        answer += mod
        mod = temp
        added_list.append(answer)
    added_list.reverse()
    while added_list[0] == 0:
        added_list.pop(0)
    return added_list


def subtract_fraction(l1, l2):
    rl1, rl2 = prep_compare(l1, l2, False, True)
    gr, eq = comparator(rl1, rl2)
    if eq:
        return [0]
    if not gr:
        rl1, rl2 = swap(rl1, rl2)
    added_list = []
    mod = 0
    for i in zip(rl1, rl2):
        answer, temp = base60_unit_subtraction(*i)
        answer += mod
        mod = temp
        added_list.append(answer)
    added_list.reverse()

    return added_list, mod


if __name__ == '__main__':
    a = Base60.from_commas('1,2,3,4,5')
    b = Base60.from_commas('59,59,3,5')
    c = add_items_in_list_number(a.number, b.number)
    # a = add_items_in_list_number([59, 59, 59, 59], [59, 59, 59, 59])
    print(c)
