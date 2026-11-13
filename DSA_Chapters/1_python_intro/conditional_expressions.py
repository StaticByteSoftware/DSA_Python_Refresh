# Chapter 1.9 - Conditional Expressions
# Syntax: value_if_true if condition else value_if_false

# foo stands in for any function so the examples can run
def foo(value):
    return value * 2

n = -5

# Traditional Control structure
if n >= 0:
    param = n
else:
    param = -n
result = foo(param) # call the function
print(result)   # 10


# Conditional expression syntax
    # directly assign value to variable
param = n if n >= 0 else -n     #pick the appropriate value
result = foo(param)     # call the function
print(result)   # 10

# One line compound expression
result = foo(n if n >= 0 else -n)
print(result)   # 10


# Example 1
# Pick between two strings
score = 72
status = 'pass' if score >= 60 else 'fail'
print(status)   # pass

# Example 2
# Use one directly inside a print
number = 7
print('even' if number % 2 == 0 else 'odd')     # odd

# Example 3
# Return the larger of two values
def larger(a, b):
    return a if a >= b else b

print(larger(3, 9))     # 9

# Example 4
# Use a default when a value is empty (an empty string counts as False)
name = ''
print(name if name else 'guest')    # guest

# Example 5
# Singular or plural as one part of a bigger expression
count = 3
print('{0} {1}'.format(count, 'item' if count == 1 else 'items'))   # 3 items

# Example 6
# Only the chosen side runs, so this never divides by zero
total = 10
divisor = 0
average = total / divisor if divisor != 0 else 0
print(average)  # 0

# Example 7
# Before the for: picks a value for every item, and needs an else
numbers = [1, 2, 3, 4]
print(['even' if x % 2 == 0 else 'odd' for x in numbers])   # ['odd', 'even', 'odd', 'even']
# After the for: a filter that drops items, and has no else
print([x for x in numbers if x % 2 == 0])   # [2, 4]

# Example 8
# Chaining works, but past two choices a regular if/elif is easier to read
score = 85
grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C'
print(grade)    # B

# Example 9
# Watch the order: everything left of the if is the true value
has_bonus = False
print(5 + 1 if has_bonus else 0)    # 0, the whole 5 + 1 is skipped
print(5 + (1 if has_bonus else 0))  # 5
