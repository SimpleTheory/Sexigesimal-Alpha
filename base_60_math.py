import copy
import functools
import pysnooper


# Wrappers -------------------------------------------------------------------------------------------------------------
def absolute(func):
    def wrapper(self, other):
        if isinstance(other, Base60):
            other = abs(Base60)
        elif isinstance(other, int):
            other = AbsBase60.from_integer(other)

        val = func(self, other)
        return val

    return wrapper


def copy_args(func):
    def wrapper(*args, **kwargs):
        new_args = [copy.copy(i) for i in args]
        new_kwargs = {k: copy.copy(v) for k, v in kwargs.items()}
        val = func(*new_args, **new_kwargs)
        return val

    return wrapper


# Classes --------------------------------------------------------------------------------------------------------------
class AbsBase60:
    def __init__(self, number, fraction=None):
        self.number: list = number
        self.fraction: list = fraction if fraction else []

    def __repr__(self):
        return f'{(int(self))} | {str(self)}'

    @classmethod
    def from_commas(cls, commas: str):
        commas = commas.strip()
        if ';' in commas:
            number, fractions = commas.split(';', 1)
            if number == '':
                return cls([], [abs(int(i)) for i in fractions.split(',')])
            return cls([abs(int(i)) for i in number.split(',')], [abs(int(i)) for i in fractions.split(',')])
        else:
            return cls([abs(int(i)) for i in commas.split(',')])

    @classmethod
    def zero(cls):
        return cls([0], [])

    @classmethod
    def from_code(cls):
        pass

    @classmethod
    def from_integer(cls, integer: int):
        return cls(int_to_base(integer, 60), [])

    @staticmethod
    def from_float(decimal: float):
        # round decimal to ten places
        # decimal = round(decimal, 10)
        # the float * 60**i until is int
        for i in range(101):
            current_answer = float(decimal * (60 ** i))
            if current_answer.is_integer():
                return WholeBase60Number(AbsBase60.from_integer(int(current_answer)).number, i, True).to_Abs60()
                # then that from_int(int).numberize(i).to_Abs60()

        # if is not int after 100 digits
        # round the int at that place and convert
        # run the round scheme on the number and return

    # TODO: Make a rounding scheme such that if a number is 60 it is 0 and adds to the next number
    @copy_args
    @pysnooper.snoop()
    def round(self, place=None):
        if place:
            self.fraction = self.fraction[:place]
        elif place == 0:
            self.fraction = []
        whole_number = self.wholenumberize(True)
        whole_number.number[0] = 60
        whole_number.number = carry_over_reformat_base(whole_number.number)
        return whole_number.to_Abs60()

    def copy(self):
        return copy.copy(self)

    def is_int(self):
        if not self.fraction:
            return True
        elif not remove_0s_from_end(self.fraction):
            return True
        return False

    def is_float(self):
        return not self.is_int()

    def wholenumberize(self, reverse_=False):
        new_frac = remove_0s_from_end(self.fraction)
        return WholeBase60Number(self.number + new_frac, len(new_frac), reverse_)

    def __str__(self):
        n = ','.join(stringify(self.number))
        if self.fraction:
            f = ','.join(stringify(self.fraction))
            return f'{n};{f}'
        return n

    def __int__(self):
        return sum([v * (60 ** i) for i, v in enumerate(self.number.__reversed__())])

    def __float__(self):
        whole_number = self.wholenumberize()
        return int(whole_number) / (60 ** whole_number.seximals)

    @absolute
    def __gt__(self, other):
        return abs_base60_comparator(self, other)[0]

    @absolute
    def __ge__(self, other):
        return (abs_base60_comparator(self, other)[0]) or (abs_base60_comparator(self, other)[1])

    @absolute
    def __lt__(self, other):
        return not abs_base60_comparator(self, other)[0] and (not abs_base60_comparator(self, other)[1])

    @absolute
    def __le__(self, other):
        return (not abs_base60_comparator(self, other)[0]) or abs_base60_comparator(self, other)[1]

    @absolute
    def __eq__(self, other):
        return abs_base60_comparator(self, other)[1]

    @absolute
    def __add__(self, other):
        return abs(lazy_addition(self, other))

    @absolute
    def __sub__(self, other):
        return abs(lazy_subtraction(self, other))

    def __abs__(self):
        return self

    def __copy__(self):
        return AbsBase60(copy.copy(self.number), copy.copy(self.fraction))


class Base60(AbsBase60):
    def __init__(self, number, negative, fraction=None):
        super(Base60, self).__init__(number, fraction)
        self.negative: bool = negative

    @classmethod
    def zero(cls):
        return cls([0], False, [])

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
        return copy.copy(self)

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


class WholeBase60Number:

    def __init__(self, number, fractional_length, reverse_=False):
        self.number: list = number
        self.seximals: int = fractional_length
        self.reversed: bool = reverse_
        if reverse_:
            self.number.reverse()

    @classmethod
    def from_base60_number(cls, b60num: AbsBase60, reverse_=False):
        frac_len = len(remove_0s_from_end(b60num.fraction))
        return cls(b60num.number + b60num.fraction, frac_len, reverse_)

    def toggle_reverse(self):
        self.number.reverse()
        self.reversed = not self.reversed

    def reverse(self):
        if self.reversed is True:
            return
        else:
            self.toggle_reverse()

    def un_reverse(self):
        if self.reversed is False:
            return
        else:
            self.toggle_reverse()

    @copy_args
    def to_Abs60(self):
        self.un_reverse()
        fraction = self.number[:self.seximals]
        fraction.reverse()
        fraction = remove_0s_from_end(fraction)
        number = self.number[self.seximals:]
        number.reverse()
        return AbsBase60(number, fraction)

    def __int__(self):
        if not self.reversed:
            iter_ls = self.copy(reversed_=True).number
        else:
            iter_ls = self.number
        return sum([v * (60 ** i) for i, v in enumerate(iter_ls)])

    def copy(self, reversed_=False):
        if not reversed_:
            return copy.copy(self)
        else:
            a = copy.copy(self)
            a.toggle_reverse()
            return a

    def __copy__(self):
        return WholeBase60Number(copy.copy(self.number), copy.copy(self.seximals), copy.copy(self.reversed))

    base = 60


# Misc -----------------------------------------------------------------------------------------------------------------
def swap(x, y): return y, x,


def stringify(x): return [str(i) for i in x]


def absolutify(x):
    if isinstance(x, list):
        return [abs(i) for i in x]
    else:
        return abs(x)


def reverse(x): return x[::-1]


# Unit Mathematics -----------------------------------------------------------------------------------------------------
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


def base_unit_round(unit: int):
    if unit < 30:
        return 0
    else:
        return 60


# Formatting -----------------------------------------------------------------------------------------------------------
def prep_compare(l1, l2, number=True, reversed_=False):
    rl1 = l1[:]
    rl2 = l2[:]
    len_diff = len(rl1) - len(rl2)
    if number:
        if len_diff > 0:
            rl2 = [0 for _ in range(abs(len_diff))] + rl2
        elif len_diff < 0:
            rl1 = [0 for _ in range(abs(len_diff))] + rl1
    else:
        if len_diff > 0:
            rl2.extend([0 for _ in range(len_diff)])
        elif len_diff < 0:
            rl1.extend([0 for _ in range(len_diff)])

    if reversed_:
        rl1.reverse()
        rl2.reverse()

    return rl1, rl2

@pysnooper.snoop()
def carry_over_reformat_base(ls: list):
    """
    List argument must be SMALLEST -> BIGGEST!

    :param ls: List to perform this on MUST BE REVERSED
    :return:
    """
    if [i for i in ls if i >= 60]:
        carry_over = 0
        temp_ls = []

        for v in ls:
            v += carry_over
            carry_over = 0
            while v >= 60:
                carry_over += 1
                v -= 60
            temp_ls.append(v)

        if carry_over:
            temp_ls.append(carry_over)

        return temp_ls

    return ls


# Comparison -----------------------------------------------------------------------------------------------------------
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


# Conversions & Misc Basemath ------------------------------------------------------------------------------------------
def int_to_base(integer, base):
    # find how many times it goes to 60
    # if the quotient is less than 60 return it
    # otherwise rerun the function with the quotient and append modulus to list
    if integer == 0:
        return Base60.zero()

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


def reflect60(n: list): return [60 - i for i in n]


# Arithmetic Functions -------------------------------------------------------------------------------------------------
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


def lazy_addition(number1: Base60 | AbsBase60, number2: Base60 | AbsBase60):
    n1 = number1.copy()
    n2 = number2.copy()

    if n1.fraction and n2.fraction:
        fraction, holdover = add_items_in_list_fraction(n1.fraction, n2.fraction)
        n1.number[-1] += holdover
    elif n1.fraction:
        fraction = n1.fraction
    elif n2.fraction:
        fraction = n2.fraction
    else:
        fraction = []

    sum_ = add_items_in_list_number(n1.number, n2.number)

    return AbsBase60(sum_, fraction=fraction)


# Subtraction ----------------------------------------------------------------------------------------------------------
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
    holdover = 0
    rl1, rl2 = prep_compare(l1, l2, False, True)
    gr, eq = comparator(reverse(rl1), reverse(rl2), True)
    if eq:
        return []
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


def lazy_subtraction(subtractee: Base60 | AbsBase60, subtractor: Base60 | AbsBase60) -> Base60:
    if abs(subtractee) == abs(subtractor):
        return Base60.zero()
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
    return Base60(sum_, negative, fraction=fraction)


# Multiplicative -------------------------------------------------------------------------------------------------------

@copy_args
def int_multiplication(n1, n2):
    n1 = absolutify(n1)
    n2 = absolutify(n2)
    print(type(n2))
    sum_ = AbsBase60.zero()
    r = range(len(n2)) if isinstance(n2, list) else range(int(n2))
    for _ in r:
        sum_ += n1
    return sum_


def remove_0s_from_end(x, end=True):
    if not x:
        return []
    elif len(x) == 0:
        return []
    new_ls = x.copy()
    if end:
        while new_ls[-1] == 0:
            new_ls = new_ls[:-1]
            if not new_ls:
                return []
    else:
        while new_ls[0] == 0:
            new_ls = new_ls[1:]
            if not new_ls:
                return []
    return new_ls


@copy_args
def multiply(n1: Base60 | AbsBase60, n2: AbsBase60 | Base60):
    n1.fraction = remove_0s_from_end(n1.fraction)
    n2.fraction = remove_0s_from_end(n2.fraction)
    n1_whole = {'number': n1.number + n1.fraction, 'seximals': len(n1.fraction)}
    n2_whole = {'number': n2.number + n2.fraction, 'seximals': len(n2.fraction)}
    total_seximals = n1_whole['seximals'] + n2_whole['seximals']
    total_whole_num = int_multiplication(AbsBase60(n1_whole['number']), AbsBase60(n2_whole['number']))
    r_twn = reverse(total_whole_num.number)
    fraction = r_twn[:total_seximals]
    numbers = r_twn[total_seximals:]
    fraction.reverse()
    numbers.reverse()
    return AbsBase60(numbers, fraction)


# Division -------------------------------------------------------------------------------------------------------------
def inverse(number: AbsBase60):
    whole_number = number.wholenumberize()
    for i in range(10000):
        current_answer: float = (60 ** (whole_number.seximals + i)) / int(whole_number)
        # Base case
        if current_answer.is_integer():
            # i is the fractionality
            r_twn = WholeBase60Number(AbsBase60.from_integer(int(current_answer)).number, i, True)
            return r_twn.to_Abs60()

    current_answer: float = (60 ** (whole_number.seximals + 10002)) / int(whole_number)
    r_twn = WholeBase60Number(AbsBase60.from_integer(round(current_answer)).number, 10002, True)
    return r_twn.to_Abs60()


def lazy_division(dividend, divisor):
    return multiply(dividend, inverse(divisor))


# Base 60 Sorting ------------------------------------------------------------------------------------------------------


def partition(first_index, last_index, nums_):
    pivot_value, index_swap_iterative = nums_[last_index], first_index
    for i in range(first_index, last_index):
        if nums_[i] <= pivot_value:
            nums_[i], nums_[index_swap_iterative] = nums_[index_swap_iterative], nums_[i]
            index_swap_iterative += 1
    nums_[index_swap_iterative], nums_[last_index] = nums_[last_index], nums_[index_swap_iterative]
    return index_swap_iterative


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
    a2 = Base60.from_integer(43)
    a1 = Base60.from_integer(437)
    print([int_multiplication(a1, a2)])
    print(a1, a2)
    print(f'expected {43 * 437}')

    # print(b >= a)
    # print(a >= c)
    #
    # print(a >= b)
