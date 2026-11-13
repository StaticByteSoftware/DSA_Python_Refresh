# Comprehension syntax List,Dictionaries,Set,Generator expressions
    # 1.9 Comprehension Syntax
# Syntax: [expression for value in iterable if condition]
# The if part is optional

n = 5

# Traditional Control structure
squares = []
for k in range(1, n + 1):
    squares.append(k * k)
print(squares)  # [1, 4, 9, 16, 25]

# List comprehension: the same loop on one line
squares = [k * k for k in range(1, n + 1)]
print(squares)  # [1, 4, 9, 16, 25]

# Traditional Control structure with a condition
factors = []
for k in range(1, 13):
    if 12 % k == 0:
        factors.append(k)
print(factors)  # [1, 2, 3, 4, 6, 12]

# List comprehension with a condition
factors = [k for k in range(1, 13) if 12 % k == 0]
print(factors)  # [1, 2, 3, 4, 6, 12]


# The brackets decide what you get back
#   [k * k for k in data]       list
#   {k * k for k in data}       set
#   {k: k * k for k in data}    dictionary
#   (k * k for k in data)       generator

# Example 1
# List comprehension: keeps order and duplicates
words = ['apple', 'bob', 'apple', 'cat']
print([word.upper() for word in words])     # ['APPLE', 'BOB', 'APPLE', 'CAT']
print([word for word in words if len(word) == 3])   # ['bob', 'cat']

# Example 2
# Set comprehension: removes duplicates, and has no order
# sorted() is only here so the output is always the same
print(sorted({word for word in words}))     # ['apple', 'bob', 'cat']
print(sorted({len(word) for word in words}))    # [3, 5]

# Example 3
# Dictionary comprehension: uses key: value instead of a single expression
print({k: k * k for k in range(1, n + 1)})  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
print({word: len(word) for word in words})  # {'apple': 5, 'bob': 3, 'cat': 3}

# Example 4
# Swap the keys and values of a dictionary with .items()
ages = {'ann': 30, 'ben': 25}
print({age: name for name, age in ages.items()})    # {30: 'ann', 25: 'ben'}

# Example 5
# Generator expression: makes values one at a time instead of building a list
squares_gen = (k * k for k in range(1, n + 1))
print(next(squares_gen))    # 1
print(next(squares_gen))    # 4
print(list(squares_gen))    # [9, 16, 25]

# Example 6
# When a generator is the only argument, the extra parentheses can be dropped
total = sum(k * k for k in range(1, n + 1))
print(total)    # 55
print(max(len(word) for word in words))     # 5

# Example 7
# Two for clauses: the first one is the outer loop
print([(x, y) for x in range(2) for y in 'ab'])
# [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]

# Flatten a 2D list
matrix = [[1, 2], [3, 4], [5, 6]]
print([value for row in matrix for value in row])   # [1, 2, 3, 4, 5, 6]

# Example 8
# Building a 2D list: each row needs to be its own list
grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 9
print(grid)     # [[9, 0, 0], [0, 0, 0]]

# Without the comprehension, both rows are the same list
shared = [[0] * 3] * 2
shared[0][0] = 9
print(shared)   # [[9, 0, 0], [9, 0, 0]]

# Example 9
# The loop variable stays inside the comprehension
k = 'unchanged'
print([k for k in range(3)])    # [0, 1, 2]
print(k)    # unchanged
