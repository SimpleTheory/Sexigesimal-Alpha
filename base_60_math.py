import copy
import functools
import random
import pysnooper


class Base60:
    def __init__(self, number, negative, fraction=None):
        self.number: list = number
        self.fraction: list = fraction
        self.negative: bool = negative

    @classmethod
    def from_commas(cls, commas: str):
        commas = commas.strip()
        negative = commas.startswith('-')
        if ';' in commas:
            number, fractions = commas.split(';', 1)
            return cls([int(i) for i in number.split(',')], negative, [int(i) for i in fractions.split(',')])
        else:
            return cls([int(i) for i in commas.split(',')], negative)

    @classmethod
    def from_code(cls):
        pass

    @classmethod
    def from_integer(cls, integer: int):
        return cls(int_to_base(integer, 60), integer < 0)

    def copy(self):
        return Base60(self.number, self.negative, self.fraction)

    def __str__(self):
        n = ','.join(stringify(self.number))
        if self.fraction:
            f = ','.join(stringify(self.fraction))
            return f'{n};{f}'
        return n

    def __int__(self):
        return sum([v * (60 ** i) for i, v in enumerate(self.number.__reversed__())])

    def __abs__(self):
        return AbsBase60(self.number, self.fraction)

    def __copy__(self):
        return Base60(copy.copy(self.number), copy.copy(self.negative), copy.copy(self.fraction))


class AbsBase60:
    def __init__(self, number, fraction=None):
        self.number: list = number
        self.fraction: list = fraction

    def __repr__(self):
        return f'{(int(self))} | {str(self)}'

    @classmethod
    def from_commas(cls, commas: str):
        commas = commas.strip()
        if ';' in commas:
            number, fractions = commas.split(';', 1)
            return cls([abs(int(i)) for i in number.split(',')], [abs(int(i)) for i in fractions.split(',')])
        else:
            return cls([abs(int(i)) for i in commas.split(',')])

    @classmethod
    def from_code(cls):
        pass

    @classmethod
    def from_integer(cls, integer: int):
        return cls(int_to_base(integer, 60), integer < 0)

    def copy(self):
        return copy.copy(self)

    def is_int(self):
        if not self.fraction:
            return True
        elif False not in [i == 0 for i in self.fraction]:
            return True
        return False

    def is_float(self):
        return not self.is_int()

    def __str__(self):
        n = ','.join(stringify(self.number))
        if self.fraction:
            f = ','.join(stringify(self.fraction))
            return f'{n};{f}'
        return n

    def __int__(self):
        return sum([v * (60 ** i) for i, v in enumerate(self.number.__reversed__())])

    def __gt__(self, other):
        return abs_base60_comparator(self, other)[0]

    def __ge__(self, other):
        return (abs_base60_comparator(self, other)[0]) or (abs_base60_comparator(self, other)[1])

    @pysnooper.snoop()
    def __lt__(self, other):
        print(not abs_base60_comparator(self, other)[0])
        return not abs_base60_comparator(self, other)[0] and (not abs_base60_comparator(self, other)[1])

    def __le__(self, other):
        return (not abs_base60_comparator(self, other)[0]) or abs_base60_comparator(self, other)[1]

    def __eq__(self, other):
        return abs_base60_comparator(self, other)[1]

    def __abs__(self):
        return self

    def __copy__(self):
        return AbsBase60(copy.copy(self.number), copy.copy(self.fraction))


###################
def swap(x, y): return y, x,


def stringify(x): return [str(i) for i in x]


def absolutify(x): return [abs(i) for i in x]


# ----
def base60_unit_addition(num1, num2):
    temp = num1 + num2
    q, m = euclidean_division(temp, 60)
    return m, q


def base60_unit_subtraction(subtractee, subtractor):
    holdover = 0
    while subtractee < subtractor:
        subtractee += 60
        holdover -= 1
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
        if (not self) and (not other):
            return False, True
        elif not self:
            return False, False
        elif not other:
            return True, False
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


def int_to_base(integer, base):
    # find how many times it goes to 60
    # if the quotient is less than 60 return it
    # otherwise rerun the function with the quotient and append modulus to list
    if integer == 0:
        return [0]

    answer = []

    def recurse(num):
        quotient, mod = euclidean_division(num, base)
        answer.insert(0, mod)
        if quotient < base:
            if quotient > 0:
                answer.insert(0, quotient)
            return
        recurse(quotient)

    recurse(integer)
    return answer


@pysnooper.snoop()
def abs_base60_comparator(n1, n2):
    gr, eq = comparator(n1.number, n2.number)
    if gr:
        return True, False
    elif eq:
        grf, eqf = comparator(n1.fraction, n2.fraction, True)
        if eqf:
            return False, True
        elif grf:
            return True, False
        else:
            return False, False
    else:
        return False, False


def return_max(self: Base60, other: Base60) -> Base60:
    gr, eq = comparator(self.number, other.number)
    if gr:
        return self
    elif eq:
        grf, eqf = comparator(self.fraction, other.fraction, True)
        if eqf or grf:
            return self
        else:
            return other
    else:
        return other


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


@pysnooper.snoop()
def lazy_addition(number1: Base60, number2: Base60):
    n1 = number1.copy()
    n2 = number2.copy()
    print(f'{number1.number}')
    print(n1.number)
    print(f'{id(n1)} - {id(number1)}')
    print(f'{id(n1.number)} - {id(number1.number)}')
    if n1.fraction and n2.fraction:
        fraction, holdover = add_items_in_list_fraction(n1.fraction, n2.fraction)
        n1.number[-1] += holdover
    elif n1.fraction:
        fraction = n1.fraction
    elif n2.fraction:
        fraction = n2.fraction
    else:
        fraction = None
    sum_ = add_items_in_list_number(n1.number, n2.number)
    print(number1.number)
    print(n1.number)
    return Base60(sum_, None, fraction=fraction)


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


def reverse(x): return x[::-1]


def subtract_fraction(l1, l2):
    holdover = 0
    rl1, rl2 = prep_compare(l1, l2, False, True)
    gr, eq = comparator(reverse(rl1), reverse(rl2), True)
    if eq:
        return [0]
    if not gr:
        rl1, rl2 = swap(rl1, rl2)
        holdover = -1
    added_list = []
    mod = 0
    for i in zip(rl1, rl2):
        answer, temp = base60_unit_subtraction(*i)
        answer += mod
        mod = temp
        added_list.append(answer)
    added_list.reverse()

    return added_list, holdover


def reflect60(n: list): return [60 - i for i in n]


@pysnooper.snoop()
def lazy_subtraction(subtractee: Base60, subtractor: Base60):
    if abs(subtractee) == abs(subtractor):
        return Base60([0], False)
    elif abs(subtractee) > abs(subtractor):
        subtractee_copy = subtractee.copy()
        subtractor_copy = subtractor.copy()
        negative = False

    else:
        subtractor_copy = subtractee.copy()
        subtractee_copy = subtractor.copy()
        negative = True

    if subtractee_copy.fraction and subtractor_copy.fraction:
        fraction, holdover = subtract_fraction(subtractee_copy.fraction, subtractor_copy.fraction)
        subtractee_copy.number[-1] += holdover
    elif subtractee_copy.fraction:
        fraction = subtractee_copy.fraction
    elif subtractor_copy.fraction:
        fraction = reflect60(subtractor_copy.fraction)
        subtractee_copy.number[-1] -= 1
    else:
        fraction = None
    sum_ = subtract_number(subtractee_copy.number, subtractor_copy.number)
    return Base60(sum_, None, fraction=fraction), negative


########################


def partition(first_index, last_index, nums_):
    pivot_value, index_swap_iterative = nums_[last_index], first_index
    for i in range(first_index, last_index):
        if nums_[i] <= pivot_value:
            nums_[i], nums_[index_swap_iterative] = nums_[index_swap_iterative], nums_[i]
            index_swap_iterative += 1
    nums_[index_swap_iterative], nums_[last_index] = nums_[last_index], nums_[index_swap_iterative]
    return index_swap_iterative


@pysnooper.snoop()
def quicksort(first_i, last_i, nums):
    if last_i is None:
        last_i = len(nums) - 1

    if len(nums) == 1:  # Basecase
        return nums

    if first_i < last_i:
        pi = partition(first_i, last_i, nums)
        quicksort(first_i, pi - 1, nums)  # Recursively sorting the left values
        quicksort(pi + 1, last_i, nums)  # Recursively sorting the right values
    return nums


sort = functools.partial(quicksort, 0, None)

if __name__ == '__main__':
    # a = Base60.from_commas('1,2,3,4,5')
    # b = Base60.from_commas('59,59,3,5')
    # c = add_items_in_list_number(a.number, b.number)
    # a = add_items_in_list_number([59, 59, 59, 59], [59, 59, 59, 59])
    # a = subtract_fraction([30, 40, 20], [5, 5, 40])
    # a = lazy_subtraction(Base60.from_commas('4,16;18'), Base60.from_commas('1,12;6'))
    # print(a)
    # print(int_to_base(478, 60))
    # b60_list = [AbsBase60.from_integer(random.randint(0, 10000)) for _ in range(5)]
    # print('LIST')
    # for i in b60_list:
    #     print(i)
    # print()
    # for i in b60_list:
    #     print(int(i))
    # print('\n\nSORTED')
    # for i in sort(b60_list):
    #     print(i)
    # print()
    # for i in sort(b60_list):
    #     print(int(i))
    a = AbsBase60.from_commas('4,16;54')
    b = AbsBase60.from_commas('4,0;7')
    print(a)
    print(id(a))
    print(id(a.number))
    c = lazy_addition(a, b)
    print(a)
    print(c)

    # print(b >= a)
    # print(a >= c)
    #
    # print(a >= b)
