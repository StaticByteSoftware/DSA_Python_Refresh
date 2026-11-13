# examples of scopes in python: local & global
# examples of namespaces
    # 1.10 Scopes and Namespaces
import math
import cmath

# Scope: the part of the code where a name can be seen
# Namespace: a dictionary that maps names to the objects they refer to
# Each scope has its own namespace, so scopes are how python decides which
# namespace to look in

# Python searches for a name in this order and stops at the first match (LEGB)
#   L - Local:     inside the current function
#   E - Enclosing: inside any outer function
#   G - Global:    top level of this file
#   B - Built-in:  names python always has (len, print, max...)


# ---------- Scopes ----------

# Global scope: defined at the top level, every function can read it
school = "State University"

def read_global():
    print(school)

read_global()   # State University

# Local scope: created when the function is called, gone when it returns
def read_local():
    message = "only exists in here"
    print(message)

read_local()    # only exists in here
try:
    print(message)
except NameError as e:
    print(e)    # name 'message' is not defined

# Assigning inside a function makes a new local name
# The global with the same name is hidden, not changed
count = 10

def shadow_global():
    count = 99
    print(count)

shadow_global() # 99
print(count)    # 10

# Python decides a name is local before the function runs, so reading it
# before the assignment fails even though a global exists
total = 0

def add_broken(x):
    total = total + x   # total is local here, and it has no value yet
    return total

try:
    add_broken(5)
except UnboundLocalError as e:
    print(type(e).__name__)     # UnboundLocalError

# global: assign to the global name instead of making a local one
def add_to_total(x):
    global total
    total = total + x

add_to_total(5)
add_to_total(3)
print(total)    # 8

# Changing an object is not the same as assigning a name
# append changes the list, the name scores still points to the same list,
# so no global keyword is needed
scores = [90, 85]

def add_score(score):
    scores.append(score)

add_score(70)
print(scores)   # [90, 85, 70]

# Enclosing scope: an inner function can read the outer function's names
# nonlocal: assign to the enclosing name, like global but one level out
def make_counter():
    value = 0

    def increment():
        nonlocal value
        value += 1
        return value

    return increment

counter = make_counter()
print(counter())    # 1
print(counter())    # 2
print(counter())    # 3

# LEGB in one example
level = "global"

def outer():
    level = "enclosing"

    def inner():
        level = "local"
        print(level)    # finds L first

    inner()
    print(level)        # no L here, so finds E

outer()         # local
                # enclosing
print(level)    # global

# Built-in scope: found last, so your own name can hide a built-in
values = [3, 7, 2]
print(max(values))  # 7

def hide_builtin():
    max = 100           # local max hides the built-in, only in this function
    return max

print(hide_builtin())   # 100
print(max(values))      # 7

# Only functions, classes and modules create a new scope
# if and for blocks do not, so the loop variable is still there after the loop
for i in range(3):
    pass
print(i)    # 2

# Comprehensions are the exception, they have their own scope
squares = [n * n for n in range(3)]
print('n' in globals())     # False


# ---------- Namespaces ----------

# globals(): the namespace of this file as a dict
print(globals()['school'])  # State University
print('school' in globals())    # True

# locals(): the namespace of the current function as a dict
def show_locals(a):
    b = a * 2
    return locals()

print(show_locals(4))   # {'a': 4, 'b': 8}

# Creating a name is the same as adding a key to the namespace
globals()['added_by_hand'] = "hello"
print(added_by_hand)    # hello

# Modules each have their own namespace, so the same name can be used twice
# without a clash. The dot says which namespace to look in
print(math.sqrt(4))     # 2.0
print(cmath.sqrt(4))    # (2+0j)
print(math.__dict__['pi'] == math.pi)   # True

# Classes and instances each have their own namespace too
class Student:
    school = "State University"     # class namespace, shared by all students

    def __init__(self, name):
        self.name = name            # instance namespace, one per student

    def greet(self):
        return "Hi, I am " + self.name

alice = Student("Alice")
bob = Student("Bob")

# vars(): the namespace of an object as a dict
print(vars(alice))  # {'name': 'Alice'}
print(vars(bob))    # {'name': 'Bob'}

# school is not in the instance, so python checks the class next
print(alice.school) # State University

# Assigning through the instance adds to the instance namespace
# The class is not changed and bob still gets the class value
alice.school = "City College"
print(vars(alice))  # {'name': 'Alice', 'school': 'City College'}
print(alice.school) # City College
print(bob.school)   # State University

# dir(): every name you can reach from an object, including the class's names
print([name for name in dir(alice) if not name.startswith('__')])
# ['greet', 'name', 'school']
