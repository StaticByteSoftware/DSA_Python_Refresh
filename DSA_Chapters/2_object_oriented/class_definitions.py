# Examples of class definitions in python
    # 2.3 Class Definitions
    # 2.3.1 Example: CreditCard Class
    # 2.3.2 Operator Overloading and Python's Special Methods
from functools import singledispatchmethod

# Class:       a blueprint that says what data an object holds and what it can do
# Object:      one thing built from that blueprint (also called an instance)
# Attribute:   a piece of data stored on an object (self.name)
# Method:      a function defined inside a class. "Member function" is the
#              C++/Java name for the same thing
# self:        the object the method was called on. Python passes it in for you
# Constructor: __init__, runs once when a new object is made, sets up its data


# ---------- 1. A Basic Class ----------

class Dog:
    # class attribute: one copy shared by every Dog
    species = "Canis familiaris"

    # constructor: Dog("Rex", 3) makes a new empty object, then calls
    # __init__(new_object, "Rex", 3)
    def __init__(self, name, age):
        # instance attributes: every Dog gets its own copy
        self.name = name
        self.age = age

    # method: the first parameter is always self
    def bark(self):
        return f"{self.name} says woof"

    # a method can change the object's data through self
    def have_birthday(self):
        self.age += 1

rex = Dog("Rex", 3)
fido = Dog("Fido", 5)

print(rex.bark())       # Rex says woof
print(fido.bark())      # Fido says woof
rex.have_birthday()
print(rex.age)          # 4
print(fido.age)         # 5     (fido is a separate object, so it didn't change)
print(rex.species, fido.species)    # Canis familiaris Canis familiaris


# ---------- 2. The self Identifier ----------

# rex.bark() is shorthand for Dog.bark(rex): python passes rex in as self
print(Dog.bark(rex))    # Rex says woof

# self is just the first parameter. "self" is a convention, not a keyword

# Forget self in the def, and python still passes the object in, so there is
# one argument too many
class NoSelf:
    def hello():
        return "hi"

try:
    NoSelf().hello()
except TypeError as e:
    print(e)    # NoSelf.hello() takes 0 positional arguments but 1 was given

# Forget self. on the assignment, and you only make a local variable that
# disappears when __init__ ends
class NoSelfDot:
    def __init__(self, name):
        name = name             # local variable, not stored on the object

forgot = NoSelfDot("Max")
print(hasattr(forgot, "name"))  # False


# ---------- 3. The Constructor (__init__) ----------

# __init__ runs on its own right after python creates the object
# It returns nothing. Its job is to give the object its starting data
# (Technically __new__ builds the object and __init__ fills it in, but
# __init__ is what people mean by "constructor" in python)
# Default values let the caller leave out arguments
# It is also a good place to reject bad arguments

class Rectangle:
    def __init__(self, width, height=1):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    # methods can call other methods through self,
    # and can take other objects of the same class
    def is_bigger_than(self, other):
        return self.area() > other.area()

r1 = Rectangle(4, 5)
r2 = Rectangle(10)          # height uses the default of 1
print(r1.area())            # 20
print(r2.area())            # 10
print(r1.is_bigger_than(r2))    # True

try:
    Rectangle(-2, 3)
except ValueError as e:
    print(e)    # width and height must be positive

# Watch out: never use a list (or other mutable) as a default value.
# The default is made once and shared by every object. Use None instead
class Team:
    def __init__(self, members=None):
        self.members = members if members is not None else []

a, b = Team(), Team()
a.members.append("Kim")
print(b.members)            # []   (each Team got its own list)


# ---------- 4. Three Kinds of Methods ----------

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    # instance method: gets self, works with one object's data
    def to_fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    # class method: gets cls (the class itself) instead of self
    # Common use: a second way to build an object ("alternate constructor")
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        return cls((fahrenheit - 32) * 5 / 9)

    # static method: gets neither self nor cls. A plain function that lives
    # in the class because it belongs with it
    @staticmethod
    def is_freezing(celsius):
        return celsius <= 0

boiling = Temperature(100)
also_boiling = Temperature.from_fahrenheit(212)
print(boiling.to_fahrenheit())      # 212.0
print(also_boiling.celsius)         # 100.0
print(Temperature.is_freezing(-5))  # True


# ---------- 5. Encapsulation ----------

# Encapsulation: keep an object's data inside it and make outside code go
# through methods instead of changing the data directly. The methods can then
# enforce the rules (no going over the limit, no negative payments...)

# Python has no private keyword. It uses naming conventions instead:
#   name     public:    anyone can use it
#   _name    protected: means "internal, don't touch from outside"
#                       It is only a convention, python does not stop you
#   __name   private:   python renames it to _ClassName__name ("name mangling")
#                       so it is harder to reach by accident

# Example: CreditCard (2.3.1), uses _protected names
class CreditCard:
    def __init__(self, customer, bank, account, limit):
        self._customer = customer
        self._bank = bank
        self._account = account
        self._limit = limit
        self._balance = 0       # every new card starts at 0

    # getters (accessors): outside code can read the data but not change it
    def get_customer(self):
        return self._customer

    def get_balance(self):
        return self._balance

    def get_limit(self):
        return self._limit

    # mutators: the only ways to change the balance, so the rules always run
    def charge(self, price):
        """Charge price to the card if there is room. Return True if approved."""
        if price + self._balance > self._limit:
            return False
        self._balance += price
        return True

    def make_payment(self, amount):
        if amount <= 0:
            raise ValueError("payment must be positive")
        self._balance -= amount

card = CreditCard("Jo Bowman", "Main St Bank", "5391 0375 9387 5309", 1000)
print(card.charge(200))     # True
print(card.charge(900))     # False  (200 + 900 is over the 1000 limit)
card.make_payment(50)
print(card.get_balance())   # 150

# The underscore is a warning, not a lock. This works, but breaks the rules
print(card._balance)        # 150

# Example: BankAccount, uses a __private name and @property
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner          # public
        self.__balance = balance    # private, stored as _BankAccount__balance

    # @property lets outside code read acct.balance like an attribute
    # (no parentheses) while a method runs behind the scenes
    @property
    def balance(self):
        return self.__balance

    # runs on acct.balance = value, so it can check the value first
    # (leave the setter out and the property becomes read-only)
    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self.__balance = value

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.__balance += amount

acct = BankAccount("Ana", 100)
acct.deposit(50)
print(acct.balance)         # 150  (calls the getter)
acct.balance = 300          # calls the setter
print(acct.balance)         # 300

try:
    acct.balance = -10      # setter rejects it
except ValueError as e:
    print(e)                # balance cannot be negative

try:
    print(acct.__balance)   # the real name was mangled, so this name doesn't exist
except AttributeError as e:
    print(e)                # 'BankAccount' object has no attribute '__balance'

print(acct._BankAccount__balance)   # 300  (mangled name, still reachable)


# ---------- 6. Dunder Methods ----------

# Dunder ("double underscore") methods are named __like_this__
# You rarely call them yourself. Python calls them when you use built-in
# syntax or functions on your object:
#   print(obj), str(obj)  -> obj.__str__()
#   repr(obj)             -> obj.__repr__()
#   len(obj)              -> obj.__len__()
#   obj[i]                -> obj.__getitem__(i)
#   x in obj              -> obj.__contains__(x)
#   for x in obj          -> obj.__iter__()
#   if obj:               -> obj.__bool__()   (uses __len__ if no __bool__)
# __init__ is a dunder method too

# Without __str__ or __repr__, printing shows the class and memory address
print(rex)                  # <__main__.Dog object at 0x...>

class Playlist:
    def __init__(self, name, songs=None):
        self.name = name
        self.songs = list(songs) if songs is not None else []

    def add(self, song):
        self.songs.append(song)

    # readable text for users. print() uses this
    def __str__(self):
        return f"{self.name} ({len(self)} songs)"

    # exact text for developers, ideally the code that would rebuild the
    # object. The REPL and containers like lists use this one
    def __repr__(self):
        return f"Playlist({self.name!r}, {self.songs!r})"

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, song):
        return song in self.songs

    def __iter__(self):
        return iter(self.songs)

trip = Playlist("Road Trip", ["Sunrise", "Highway"])
trip.add("Night Drive")

print(trip)                 # Road Trip (3 songs)
print(repr(trip))           # Playlist('Road Trip', ['Sunrise', 'Highway', 'Night Drive'])
print([trip])               # [Playlist('Road Trip', ['Sunrise', 'Highway', 'Night Drive'])]
print(len(trip))            # 3
print(trip[0])              # Sunrise
print(trip[-1])             # Night Drive
print(trip[0:2])            # ['Sunrise', 'Highway']  (slices go to __getitem__ too)
print("Highway" in trip)    # True
for song in trip:
    print(song)             # Sunrise, Highway, Night Drive (one per line)
print(bool(Playlist("Empty")))  # False  (no __bool__, so it uses len() == 0)


# ---------- 7. Operator Overloading ----------

# Operator overloading: giving an operator a meaning for your own class by
# writing the dunder method python calls for it
#   a + b    -> a.__add__(b)
#   a - b    -> a.__sub__(b)
#   a * b    -> a.__mul__(b)
#   3 * a    -> a.__rmul__(3)   ("reflected": int doesn't know how to
#                                multiply a Vector, so python asks a instead)
#   -a       -> a.__neg__()
#   a == b   -> a.__eq__(b)     (!= uses __eq__ and flips the result)
#   a < b    -> a.__lt__(b)
#   a[i] = x -> a.__setitem__(i, x)
#   abs(a)   -> a.__abs__()

# Built-in types already do this. + means something different for each:
print(1 + 2)                # 3       (int addition)
print("ab" + "cd")          # abcd    (string joining)
print([1] + [2])            # [1, 2]  (list joining)

class Vector:
    """A vector in any number of dimensions, like Vector(1, 2, 3)"""

    def __init__(self, *coords):
        self._coords = list(coords)

    def __len__(self):
        return len(self._coords)

    def __getitem__(self, i):
        return self._coords[i]

    def __setitem__(self, i, value):
        self._coords[i] = value

    def __repr__(self):
        return f"Vector{tuple(self._coords)}"

    # There is no __iter__, but "for a in self" and zip(self, other) still
    # work: python falls back to calling self[0], self[1], ... until IndexError

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("dimensions must match")
        return Vector(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError("dimensions must match")
        return Vector(*[a - b for a, b in zip(self, other)])

    # * does two different jobs depending on what it gets (see section 8)
    #   Vector * number -> scale every coordinate
    #   Vector * Vector -> dot product (a single number)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(*[a * other for a in self])
        if isinstance(other, Vector):
            return sum(a * b for a, b in zip(self, other))
        return NotImplemented   # tells python "I can't do this", so it raises TypeError

    def __rmul__(self, other):
        return self * other     # number * Vector is the same as Vector * number

    def __neg__(self):
        return Vector(*[-a for a in self])

    def __abs__(self):
        return sum(a * a for a in self) ** 0.5    # length of the vector

    def __eq__(self, other):
        return isinstance(other, Vector) and self._coords == other._coords

    def __lt__(self, other):
        return abs(self) < abs(other)   # shorter vector counts as "less"

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

print(v1 + v2)              # Vector(5, 7, 9)
print(v2 - v1)              # Vector(3, 3, 3)
print(v1 * 2)               # Vector(2, 4, 6)
print(2 * v1)               # Vector(2, 4, 6)   (uses __rmul__)
print(v1 * v2)              # 32                (1*4 + 2*5 + 3*6)
print(-v1)                  # Vector(-1, -2, -3)
print(abs(Vector(3, 4)))    # 5.0
print(v1 == Vector(1, 2, 3))    # True   (same coordinates)
print(v1 is Vector(1, 2, 3))    # False  (different objects; "is" can't be overloaded)
print(v1 != v2)             # True
print(v2 < v1)              # False

# Once < exists, sorted(), min() and max() work on your objects
print(sorted([v2, Vector(0, 1), v1]))   # [Vector(0, 1), Vector(1, 2, 3), Vector(4, 5, 6)]

v1[0] = 10                  # calls __setitem__
print(v1)                   # Vector(10, 2, 3)

# When __mul__ returns NotImplemented, python tries the right side's __rmul__.
# None has none, so python gives up and raises TypeError
try:
    v1 * None
except TypeError as e:
    print(e)                # unsupported operand type(s) for *: 'Vector' and 'NoneType'

# Defining __eq__ sets __hash__ to None, so a Vector can't be a set member or
# dict key (see chapter 10). That's right for Vector: it can change, and a key
# whose hash changes would get lost in the hash table
try:
    {v1}
except TypeError as e:
    print(e)                # unhashable type: 'Vector'


# ---------- 8. Method Overloading ----------

# Method overloading (Java/C++): several methods with the same name but
# different parameters. The compiler picks one based on the arguments
# Python does NOT do this. A class stores its methods by name, so a second
# def with the same name replaces the first
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):     # replaces the add above
        return a + b + c

calc = Calculator()
print(calc.add(1, 2, 3))    # 6
try:
    calc.add(1, 2)          # the 2-argument version is gone
except TypeError as e:
    print(e)                # Calculator.add() missing 1 required positional argument: 'c'

# Python gets the same result in other ways:

# Way 1: default values, one method handles several call shapes
class Greeter:
    def greet(self, name="friend", greeting="Hello"):
        return f"{greeting}, {name}!"

g = Greeter()
print(g.greet())                    # Hello, friend!
print(g.greet("Sam"))               # Hello, Sam!
print(g.greet("Sam", "Welcome"))    # Welcome, Sam!
print(g.greet(greeting="Hi"))       # Hi, friend!  (keyword argument)

# Way 2: *args takes any number of arguments
class Adder:
    def add(self, *numbers):
        return sum(numbers)

adder = Adder()
print(adder.add(1, 2))              # 3
print(adder.add(1, 2, 3, 4))        # 10

# Way 3: check the argument's type and branch on it
# Vector.__mul__ above does this: a number scales it, a Vector gives a dot product

# Way 4: singledispatchmethod picks a version based on the type of the first
# argument after self. The closest thing python has to real overloading
class Describer:
    @singledispatchmethod
    def describe(self, value):          # used when no other type matches
        return f"something else: {value!r}"

    @describe.register
    def _(self, value: int):
        return f"an int: {value}"

    @describe.register
    def _(self, value: str):
        return f"a string of length {len(value)}"

    @describe.register
    def _(self, value: list):
        return f"a list with {len(value)} items"

d = Describer()
print(d.describe(42))               # an int: 42
print(d.describe("hello"))          # a string of length 5
print(d.describe([1, 2, 3]))        # a list with 3 items
print(d.describe(3.5))              # something else: 3.5

# Constructors can't be overloaded either, since there is only one __init__
# Use default values (Rectangle above) or a @classmethod alternate
# constructor (Temperature.from_fahrenheit above) instead
