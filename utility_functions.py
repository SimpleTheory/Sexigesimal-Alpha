import math
from fractions import Fraction
import pysnooper
from collections.abc import Iterable
import re


#######################################
# Utility functions for base 60 counting system

def reverse(x: list):
    return [i for i in x.__reversed__()]


def divide(dividend, divisor):
    if dividend % divisor == 0:
        return dividend // divisor
    else:
        return dividend / divisor


@pysnooper.snoop()
def flatten(iter_, *args, **kwargs) -> list:
    if isinstance(iter_, dict):
        if dict.values in args:
            temp = iter_.values()
        elif dict.keys in args:
            temp = iter_.keys()
        elif dict.items in args:
            temp = iter_.items()
        else:
            raise ReferenceError(
                'Dict access method (for ex: dict.values) was not also given when a dict was passed into func call.')
        iter_ = [i for i in temp]

    def nested_flatten(xs):
        for x in xs:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                yield from nested_flatten(x)
            else:
                yield x

    return [i for i in nested_flatten(iter_)]


#####################################
# Meaty Functions

def find_factors(number_to_factor, upto_sqrt=False, split=False):
    to_sqrt = []
    after_sqrt = []

    target = math.sqrt(number_to_factor)
    if not target.is_integer():
        target = math.ceil(target)
    else:
        target = int(target)
        to_sqrt.append(target)

    for num in range(2, target):
        quotient = divide(number_to_factor, num)
        if isinstance(quotient, int):
            to_sqrt.append(num)
            after_sqrt.append(quotient)

    to_sqrt.sort()
    after_sqrt.reverse()
    if upto_sqrt:
        return to_sqrt
    elif split:
        return to_sqrt, after_sqrt
    else:
        return to_sqrt + after_sqrt


# @pysnooper.snoop()
def find_powers_within_target(target, exclude_2=False):
    to_sqrt = find_factors(target, upto_sqrt=True)
    if len(to_sqrt) == 0:
        return None
    if exclude_2 and to_sqrt[0] == 2:
        to_sqrt.pop(0)

    power = 1
    powers = []
    result = 0

    while result < target:
        power += 1
        for factor in to_sqrt:
            result = factor ** power
            if result >= target:
                break
            powers.append(result)

    powers.sort()
    return powers


@pysnooper.snoop()
def find_multiples(target: int, exclude2=False, set_=False) -> dict | set:
    bases, inversions, powers = get_all_bases(target)
    all_bases = sorted(bases + inversions + powers)

    multiples_target = target // bases[0]
    multiples = {}

    # for i in range(2, multiples_target):
    #     multiples[str(i)] = []
    #     for base in all_bases:
    #         product = base * i
    #         if product >= target:
    #             break
    #         elif product in all_bases:
    #             continue
    #         else:
    #             multiples[str(i)].append(product)
    for base in all_bases:
        multiples[str(base)] = []
        for i in range(2, multiples_target):
            product = base * i
            if product >= target:
                break
            elif product in all_bases:
                continue
            else:
                multiples[str(base)].append(product)

    try:
        if exclude2:
            del multiples['2']
    except KeyError:
        pass
    if set_:
        temp = flatten(multiples, dict.values)
        return set(temp)
    return multiples


def get_all_bases(target):
    b, inv = find_factors(target, split=True)
    p = find_powers_within_target(target, exclude_2=True)
    return b, inv, p


def get_steps_for_factors(target, exclude_bases=False, exclude2=False, include_key=False):
    include_key = 1 if include_key else 2
    multiples_to_target = {}
    bases, inv = find_factors(target, split=True)
    all_bases = bases + inv
    for base in all_bases:
        multiples_to_target[str(base)] = []
        for i in range(include_key, target):
            product = i * base
            if product == target:
                break
            elif exclude_bases and (product in all_bases):
                continue
            multiples_to_target[str(base)].append(product)
    try:
        if exclude2:
            del multiples_to_target['2']
    except KeyError:
        pass
    return multiples_to_target
    # base_to_inv = dict(zip(bases, inv))
    # inv_to_bases = {v: k for k, v in base_to_inv}
    # def get_all_steps_to_target(dict_):
    #     for key in dict_.keys():
    #         for i in range(dict_[key])


def get_relevant_numbers(target):
    a = get_steps_for_factors(target, include_key=True)
    a = list(set(flatten(a, dict.values)))
    a.sort()
    return a


if __name__ == '__main__':
    pass
    a = get_relevant_numbers(60)
    b = [Fraction(i, 60) for i in a]
    c = [str(i) for i in b]
    d = get_steps_for_factors(60, include_key=True)
    e = {k: [str(Fraction(i, 60)) for i in v] for k, v in d.items()}
    e_list = [i for i in e.values()]
    e2 = {k: [f'{i}/60' for i in v] for k, v in d.items()}
    e2_list = [i for i in e2.values()]
    # print()
    # for i, i2 in zip(e_list, e2_list):
    #     print(i)
    #     print(i2)
    #     print()
    # print()
    # print(e)
    # print(e2)
    print(a)
    for i in sorted(c, key=lambda x: (1/int(re.search('(?<=/)\d+', x).group()), int(re.search('^\d+', x).group()),)):
        print(i)
    # y = lambda x: (x[(len(x) // 2) - 1], x[(len(x) // 2) + 1])
    # # a = {'a': [1,2,3], 'b': 2, 'c': 3}
    # # flatten(a, 8, dict, dict.values)
    # print(x := find_multiples(60, True, True))
    # print({str(i): find_factors(i) for i in x})
    # print('\n\n')
    # d = get_steps_for_factors(60, True, True)
    # print(d)
    # [print(f'{k}: {v}') for k, v in d.items()]
    # print('\n'*5)
    # e = get_steps_for_factors(60)
    # e = set(flatten(e, dict.values))
    # e=list(e);e+=[2,3,5];e.sort()
    # print(e)
    # e2 = [find_factors(i) for i in e]
    # print(e2)
    #
    # # [print(i) for i in get_all_bases(60)]
    # # print(find_multiples(60))
    # # print(set(flatten(find_multiples(60))))
    f = {str(i): [] for i in set([n.denominator for n in b])}
    for den, list_ in f.items():
        for v in b:
            if v.denominator == int(den):
                list_.append(str(v))
    print(f);print()
    g = [i for i in f.values()]
    [print(i,
           [60 //
            int(re.search('(?<=/)\d+', i2).group()) *
            int(re.search('^\d+', i2).group()) for i2 in i]
           ) for i in g]
