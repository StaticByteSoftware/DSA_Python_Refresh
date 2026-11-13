# Example of iterators and generators in python
    # 1.8 Iterators and Generators
import sys

# Iterable: an object that can hand out an iterator when you call iter() on it
#           (list, tuple, str, dict, set, range, file...)
# Iterator: an object that remembers its position and gives back one value at
#           a time when you call next() on it
# Generator: the easy way to write an iterator, using yield instead of a class

# Example Iterator Class
# Counts down from start to 1
# Needs __iter__ and __next__, and has to keep track of its own position
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self     # an iterator is its own iterable

    def __next__(self):
        if self.current <= 0:
            raise StopIteration     # tells the for loop to stop
        value = self.current
        self.current -= 1
        return value

# Example Generator
# Does the same thing as CountDown. Python creates __iter__ and __next__ for us,
# and the local variables are saved between each next() call
def count_down(start):
    current = start
    while current > 0:
        yield current   # pause here and hand back current
        current -= 1

# Example Traditional Function: builds the whole list before returning
    # 1.8 Generators
def factors_list(n):
    results = []
    for k in range(1, n + 1):
        if n % k == 0:      # k divides n evenly, so k is a factor
            results.append(k)
    return results

# Example Generator: same work, but gives one factor at a time
def factors(n):
    for k in range(1, n + 1):
        if n % k == 0:
            yield k

# Example Faster Generator: multiple yields in one function
# Factors come in pairs (k, n // k), so we only have to check up to sqrt(n)
# Runs in O(sqrt(n)) instead of O(n), but the results are no longer in order
def factors_fast(n):
    k = 1
    while k * k < n:
        if n % k == 0:
            yield k
            yield n // k
        k += 1
    if k * k == n:      # n is a perfect square, only yield k once
        yield k

# Example Infinite Generator: never ends, but only computes what we ask for
def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


# Example 1
# What a for loop does behind the scenes: iter() once, then next() until
# StopIteration is raised
data = [1, 2, 4]
i = iter(data)
print(next(i))  # 1
print(next(i))  # 2
print(next(i))  # 4
try:
    next(i)
except StopIteration:
    print('No more values')

# Example 2
# Each iter() call gives a separate iterator with its own position
first = iter(data)
second = iter(data)
next(first)
next(first)
print(next(first))      # 4
print(next(second))     # 1

# Example 3
# An iterator does not copy the list, it just holds a position in it
# so changes to the list show up
scores = [10, 20, 30]
position = iter(scores)
print(next(position))   # 10
scores[1] = 99
print(next(position))   # 99

# Example 4
# Iterator class and generator give the same result
print(list(CountDown(3)))   # [3, 2, 1]
print(list(count_down(3)))  # [3, 2, 1]

# Example 5
# Calling a generator function runs none of its code yet
# The body only runs up to the next yield each time next() is called
gen = count_down(2)
print(gen)          # <generator object count_down at 0x...>
print(next(gen))    # 2
print(next(gen))    # 1

# Example 6
# Three ways to get the factors of 100
print(factors_list(100))        # [1, 2, 4, 5, 10, 20, 25, 50, 100]
print(list(factors(100)))       # [1, 2, 4, 5, 10, 20, 25, 50, 100]
print(list(factors_fast(100)))  # [1, 100, 2, 50, 4, 25, 5, 20, 10]

# Example 7
# Take the first 10 values from a generator that never ends
fib = fibonacci()
print([next(fib) for _ in range(10)])   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Example 8
# Generator expression: list comprehension with () instead of []
# It only holds its current state, so it stays small no matter how many values
squares_list = [x * x for x in range(1000000)]
squares_gen = (x * x for x in range(1000000))
print(sys.getsizeof(squares_list))  # about 8 MB (exact size varies by version)
print(sys.getsizeof(squares_gen))   # about 200 bytes
print(sum(x * x for x in range(1, 6)))  # 55

# Example 9
# Generators only work once. After they run out they stay empty
squares = (x * x for x in range(3))
print(list(squares))    # [0, 1, 4]
print(list(squares))    # []
