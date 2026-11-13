# chapter 5: Array Based Sequences
# Multidimensional data sets


# Two dimensional array: rows and columns, like a table
# in Python this is a list of lists, where each inner list is one row
grid = [
    [22, 18, 709, 5, 33],
    [45, 32, 830, 120, 750],
    [4, 880, 45, 66, 61],
]
print('Two Dimensional Array: ', grid)

# access an element with grid[row][column]
print('Row 1, Column 2: ', grid[1][2])       # 830
print('Number of rows: ', len(grid))         # 3
print('Number of columns: ', len(grid[0]))   # 5

# visit every element, one row at a time
for row in grid:
    for value in row:
        print('{0:4d}'.format(value), end='')
    print()


# Building an empty 2D array
r = 3   # number of rows
c = 4   # number of columns

# WRONG: all three rows are references to the same list
bad = [[0] * c] * r
bad[0][0] = 9
print('Wrong way: ', bad)    # the 9 appears in every row

# RIGHT: the comprehension makes a new list for each row
good = [[0] * c for j in range(r)]
good[0][0] = 9
print('Right way: ', good)   # the 9 appears only in the first row


# Multi dimensional array: more than two indices
# this one is 3D: 2 layers, each with 2 rows, each with 3 columns
cube = [
    [                   # layer 0
        [1, 2, 3],
        [4, 5, 6],
    ],
    [                   # layer 1
        [7, 8, 9],
        [10, 11, 12],
    ],
]
print('Three Dimensional Array: ', cube)

# access an element with cube[layer][row][column]
print('Layer 1, Row 0, Column 2: ', cube[1][0][2])   # 9

# one nested loop per dimension
total = 0
for layer in cube:
    for row in layer:
        for value in row:
            total += value
print('Sum of all elements: ', total)    # 78

# building an empty 3D array: same rule, a new list at every level
layers = 2
rows = 3
cols = 4
empty_cube = [[[0] * cols for j in range(rows)] for k in range(layers)]
empty_cube[1][2][3] = 7
print('Empty 3D Array with one value set: ', empty_cube)
