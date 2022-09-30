import utility_functions
import math

# Base 60 counting system
count_to = 60

base = [1, 2, 3, 4, 5, 6]
inversions = utility_functions.reverse([60 // 2, 60 // 3, 60 // 4, 60 // 5, 60 // 6])
powers = [3 ** 2, 3 ** 3, 4 ** 2, 5 ** 2, 6 ** 2]

total_bases = sorted(base + inversions + powers)

multiples = []
i = 2


# for base in [v for v in total_bases if v <= count_to/2]: