"""
I was curious about how the computational costs of using if-elif-else logic vs.
match + case logic compare for when you want a single function that can execute
several different approaches based on an input flag.

BLUF: For small numbers of conditions, the difference is negligible. For larger
numbers of conditions, match/case logic will be faster bc it can jump straight
to the right approach, whereas if-elif-else logic has to evaluate each and every
conditional until it finds one that it meets.
"""

import timeit

def if_elif_test(x):
    if x == 1:
        return "One"
    elif x == 2:
        return "Two"
    elif x == 3:
        return "Three"
    elif x == 4:
        return "Four"
    elif x == 5:
        return "Five"
    else:
        return "Invalid"

def match_case_test(x):
    match x:
        case 1:
            return "One"
        case 2:
            return "Two"
        case 3:
            return "Three"
        case 4:
            return "Four"
        case 5:
            return "Five"
        case _:
            return "Invalid"

# Timing the functions
x_value = 5  # Change this to test different cases

if_time = timeit.timeit(lambda: if_elif_test(x_value), number=1000000)
match_time = timeit.timeit(lambda: match_case_test(x_value), number=1000000)

print(f"if-elif-else time: {if_time:.6f} seconds")
print(f"match-case time: {match_time:.6f} seconds")