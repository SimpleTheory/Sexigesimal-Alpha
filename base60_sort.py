# Python program for implementation of Quicksort Sort

# This implementation utilizes pivot as the last element in the nums list
# It has a pointer to keep track of the elements smaller than the pivot
# At the very end of partition() function, the pointer is swapped with the pivot
# to come up with a "sorted" nums relative to the pivot


def partition(first_index, last_index, nums):
    # Last element will be the pivot_value and the first element the pointer
    pivot_value, index_swap_iterative = nums[last_index], first_index
    for i in range(first_index, last_index):
        if nums[i] <= pivot_value:
            # Swapping values smaller than the pivot_value to the front
            nums[i], nums[index_swap_iterative] = nums[index_swap_iterative], nums[i]
            index_swap_iterative += 1
    # Finally swapping the last element with the pointer indexed number
    nums[index_swap_iterative], nums[last_index] = nums[last_index], nums[index_swap_iterative]
    return index_swap_iterative


# With quicksort() function, we will be utilizing the above code to obtain the pointer
# at which the left values are all smaller than the number at pointer index and vice versa
# for the right values.


def quicksort(first_i, last_i, nums):
    if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
        return nums
    if first_i < last_i:
        pi = partition(first_i, last_i, nums)
        quicksort(first_i, pi - 1, nums)  # Recursively sorting the left values
        quicksort(pi + 1, last_i, nums)  # Recursively sorting the right values
    return nums


example = [4, 5, 1, 2, 3]
print(quicksort(0, len(example) - 1, example))

example = [2, 5, 6, 1, 4, 6, 2, 4, 7, 8]
# As you can see, it works for duplicates too
print(quicksort(0, len(example) - 1, example))
