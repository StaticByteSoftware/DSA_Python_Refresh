# chapter 5: Array Based Sequences

from array import array

# Compact array example: IMPORT ARRAY 
primes = array('i', [2,3,5,7,11,13,17,19])
print('Compact Array Example: ',primes)

# Reference array examples: PYTHON LIST
# a Python list stores references to objects, not the objects themselves

# strings:
names = ['Rene', 'Joseph', 'Janet', 'Jonas', 'Helen', 'Virginia']
print('Referential Array of Names: ',names)

# numbers:
numbers = [2,3,5,7,11,13,17,19]
print('Referential Array of Numbers: ',numbers)

# Dynamic Array example
import sys  # provides getsizeof function
n = 27      # number of appends to perform
data = []
for k in range(n):
    a = len(data)   # number of elements
    b = sys.getsizeof(data)     # actual size in bytes
    print('Length: {0:3d}; Size in bytes: {1:4d}'.format(a,b))
    data.append(None)   # increase length by one

