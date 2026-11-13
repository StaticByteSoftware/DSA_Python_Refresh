# Examples of inheritance in python
    # 2.4 Inheritance
    # 2.4.1 Extending the CreditCard Class
    # 2.4.2 Hierarchy of Numeric Progressions
    # 2.4.3 Abstract Base Classes
import math
from abc import ABC, abstractmethod
from collections.abc import Sequence

# Inheritance: building a new class from an existing one. The new class gets
#              all the existing class's attributes and methods for free
# Base class:  the class being inherited from (also: parent, superclass)
# Subclass:    the class doing the inheriting (also: child, derived class)
# Override:    a subclass writes its own version of an inherited method
# Extend:      a subclass adds new methods, or calls the parent's version of a
#              method and adds more to it
# super():     a way to call the parent's version of a method
# "is-a":      a subclass object is also a base class object
#              (a Dog is an Animal), so it can be used anywhere one is expected


# ---------- 1. Basic Inheritance ----------

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def eat(self):
        return f"{self.name} is eating"

# class Dog(Animal): Dog inherits from Animal
# Dog has no __init__, so it uses Animal's
class Dog(Animal):
    # override: replaces the speak Dog inherited from Animal
    def speak(self):
        return f"{self.name} says woof"

    # extend: a new method that Animal doesn't have
    def fetch(self):
        return f"{self.name} fetches the ball"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow"

generic = Animal("Generic")
rex = Dog("Rex")
tom = Cat("Tom")

print(rex.eat())            # Rex is eating          (inherited, never written in Dog)
print(rex.speak())          # Rex says woof          (Dog's override)
print(generic.speak())      # Generic makes a sound  (Animal's version is unchanged)
print(rex.fetch())          # Rex fetches the ball

try:
    tom.fetch()             # fetch belongs to Dog, Cat doesn't have it
except AttributeError as e:
    print(e)                # 'Cat' object has no attribute 'fetch'

# Polymorphism: the same call runs a different method depending on the
# object's class
for animal in [generic, rex, tom]:
    print(animal.speak())   # Generic makes a sound / Rex says woof / Tom says meow

# How python finds a method: it looks in the object's own class first, then
# the parent, then its parent, up to object. That order is the MRO
# (method resolution order). Every class inherits from object in the end,
# which is where the default __str__ and __repr__ come from
print([cls.__name__ for cls in Dog.__mro__])    # ['Dog', 'Animal', 'object']

# is-a checks
print(isinstance(rex, Dog))         # True
print(isinstance(rex, Animal))      # True   (a Dog is an Animal)
print(isinstance(generic, Dog))     # False  (an Animal isn't necessarily a Dog)
print(issubclass(Cat, Animal))      # True


# ---------- 2. super() and Extending the Constructor ----------

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} earns ${self.salary:,}"

    def yearly_bonus(self):
        return self.salary * 0.05

class Manager(Employee):
    # A subclass that needs extra data writes its own __init__, and that
    # replaces Employee's. So it calls super().__init__ to let Employee set
    # up name and salary, then adds its own attribute
    def __init__(self, name, salary, reports=None):
        super().__init__(name, salary)
        self.reports = reports if reports is not None else []

    # extend: reuse the parent's result and add to it
    def describe(self):
        return super().describe() + f" and manages {len(self.reports)} people"

    def yearly_bonus(self):
        return super().yearly_bonus() + 1000 * len(self.reports)

worker = Employee("Lee", 60000)
boss = Manager("Kim", 90000, ["Lee", "Pat"])

print(worker.describe())        # Lee earns $60,000
print(boss.describe())          # Kim earns $90,000 and manages 2 people
print(worker.yearly_bonus())    # 3000.0
print(boss.yearly_bonus())      # 6500.0  (4500 from Employee's version + 2000)

# Forget super().__init__ and the parent's setup never runs,
# so the attributes it would have made don't exist
class BrokenManager(Employee):
    def __init__(self, name, salary, reports):
        self.reports = reports

broken = BrokenManager("Sam", 70000, [])
try:
    broken.describe()
except AttributeError as e:
    print(e)                    # 'BrokenManager' object has no attribute 'name'


# ---------- 3. Extending the CreditCard Class ----------

# Same CreditCard idea as class_definitions.py, repeated here so this file
# runs by itself (importing that file would run all of its prints too)
class CreditCard:
    def __init__(self, customer, bank, account, limit):
        self._customer = customer
        self._bank = bank
        self._account = account
        self._limit = limit
        self._balance = 0

    def get_balance(self):
        return self._balance

    def charge(self, price):
        """Charge price to the card if there is room. Return True if approved."""
        if price + self._balance > self._limit:
            return False
        self._balance += price
        return True

    def make_payment(self, amount):
        self._balance -= amount

class PredatoryCreditCard(CreditCard):
    """A CreditCard that charges interest and a fee for declined charges"""

    def __init__(self, customer, bank, account, limit, apr):
        super().__init__(customer, bank, account, limit)
        self._apr = apr     # annual percentage rate, 0.0825 means 8.25%

    # override charge, but still use the parent's version to do the real work
    def charge(self, price):
        success = super().charge(price)
        if not success:
            self._balance += 5      # $5 fee for a declined charge
        return success

    # a new method the parent doesn't have
    def process_month(self):
        """Add one month of interest to the balance"""
        if self._balance > 0:
            monthly_factor = (1 + self._apr) ** (1 / 12)
            self._balance *= monthly_factor

card = PredatoryCreditCard("Jo Bowman", "Main St Bank", "5391 0375 9387 5309", 1000, 0.0825)
print(card.charge(800))             # True
print(card.charge(500))             # False  (declined, $5 fee added)
print(card.get_balance())           # 805    (get_balance is inherited)
card.process_month()
print(round(card.get_balance(), 2)) # 810.34

# Notice PredatoryCreditCard uses self._balance directly even though it was
# created in CreditCard. That works because _balance is protected, not private.
# Section 4 shows the difference


# ---------- 4. Protected vs Private Members in Subclasses ----------

#   _name    protected: the class AND its subclasses use it freely.
#            Outside code is asked (by convention) to leave it alone
#   __name   private:   python renames it using the class that wrote it,
#            so self.__secret inside Parent becomes self._Parent__secret.
#            A subclass writing self.__secret gets _Child__secret instead,
#            which is a different name

class Parent:
    def __init__(self):
        self.public = "public"
        self._protected = "protected"
        self.__private = "private"      # stored as _Parent__private

    def show_private(self):
        return self.__private           # inside Parent, so it means _Parent__private

class Child(Parent):
    def use_protected(self):
        return self._protected          # fine: protected is meant for subclasses

    def use_private(self):
        return self.__private           # inside Child, so it means _Child__private

kid = Child()
print(kid.public)                       # public
print(kid.use_protected())              # protected
print(kid.show_private())               # private  (Parent's own method can reach it)

try:
    kid.use_private()
except AttributeError as e:
    print(e)                            # 'Child' object has no attribute '_Child__private'

# vars() shows what's really stored on the object
print(vars(kid))    # {'public': 'public', '_protected': 'protected', '_Parent__private': 'private'}

# Why private exists: it stops a subclass from overwriting the parent's data
# by accident just because it picked the same name

class UnsafeCounter:
    def __init__(self):
        self._count = 0

    def tick(self):
        self._count += 1
        return self._count

class UnsafeChild(UnsafeCounter):
    def __init__(self):
        super().__init__()
        self._count = "child's own data"    # same name, wipes out the counter

class SafeCounter:
    def __init__(self):
        self.__count = 0                    # _SafeCounter__count

    def tick(self):
        self.__count += 1
        return self.__count

class SafeChild(SafeCounter):
    def __init__(self):
        super().__init__()
        self.__count = "child's own data"   # _SafeChild__count, a separate name

try:
    UnsafeChild().tick()
except TypeError as e:
    print(e)                # can only concatenate str (not "int") to str
print(SafeChild().tick())   # 1  (the parent's counter was never touched)

# Rule of thumb: use _protected by default (the book does).
# Use __private only when subclasses must not touch or clash with a name


# ---------- 5. Hierarchy of Numeric Progressions ----------

# A progression is a sequence of numbers where each one is built from the
# one before it. The base class does all the shared work (being an iterator,
# printing). Each subclass only overrides _advance(), the one step that differs
#   Progression             0, 1, 2, 3, ...           add 1
#   ArithmeticProgression   start, +inc, +inc, ...    add a fixed amount
#   GeometricProgression    start, *base, *base, ...  multiply by a fixed amount
#   FibonacciProgression    a, b, a+b, ...            add the previous two

class Progression:
    """Base class for progressions. Default produces 0, 1, 2, 3, ..."""

    def __init__(self, start=0):
        self._current = start

    # protected method: meant to be overridden by subclasses,
    # not called from outside
    def _advance(self):
        """Update self._current to the next value.
        A subclass can set self._current to None to end the progression"""
        self._current += 1

    def __next__(self):
        if self._current is None:
            raise StopIteration
        answer = self._current
        self._advance()     # runs the subclass's _advance if it has one
        return answer

    def __iter__(self):
        return self         # a progression is an iterator (see iterator_generators.py)

    def print_progression(self, n):
        """Print the next n values"""
        print(" ".join(str(next(self)) for _ in range(n)))

class ArithmeticProgression(Progression):
    """Adds a fixed increment each step: start, start+inc, start+2inc, ..."""

    def __init__(self, increment=1, start=0):
        super().__init__(start)
        self._increment = increment

    def _advance(self):     # override
        self._current += self._increment

class GeometricProgression(Progression):
    """Multiplies by a fixed base each step: start, start*b, start*b^2, ..."""

    def __init__(self, base=2, start=1):
        super().__init__(start)
        self._base = base

    def _advance(self):     # override
        self._current *= self._base

class FibonacciProgression(Progression):
    """Each value is the sum of the two before it: first, second, first+second, ..."""

    def __init__(self, first=0, second=1):
        super().__init__(first)
        # a made-up value "before" first, chosen so that the first
        # _advance gives prev + current = (second - first) + first = second
        self._prev = second - first

    def _advance(self):     # override
        self._prev, self._current = self._current, self._prev + self._current

Progression().print_progression(10)                 # 0 1 2 3 4 5 6 7 8 9
ArithmeticProgression(5).print_progression(10)      # 0 5 10 15 20 25 30 35 40 45
ArithmeticProgression(5, 2).print_progression(10)   # 2 7 12 17 22 27 32 37 42 47
GeometricProgression().print_progression(10)        # 1 2 4 8 16 32 64 128 256 512
GeometricProgression(3).print_progression(10)       # 1 3 9 27 81 243 729 2187 6561 19683
FibonacciProgression().print_progression(10)        # 0 1 1 2 3 5 8 13 21 34
FibonacciProgression(4, 6).print_progression(10)    # 4 6 10 16 26 42 68 110 178 288

# A progression is an iterator, so it remembers where it stopped
fib = FibonacciProgression()
fib.print_progression(5)    # 0 1 1 2 3
fib.print_progression(5)    # 5 8 13 21 34

# These progressions never end, so never call list() on one.
# Use a for loop with break, or next() a set number of times
for value in GeometricProgression(10):
    if value > 1000:
        break
    print(value)            # 1, 10, 100, 1000 (one per line)

print(isinstance(fib, Progression))     # True  (a FibonacciProgression is a Progression)

# Multi-level inheritance: a subclass of a subclass
# CountdownProgression -> ArithmeticProgression -> Progression -> object
class CountdownProgression(ArithmeticProgression):
    """Counts down from start to 0, then stops"""

    def __init__(self, start):
        super().__init__(increment=-1, start=start)

    def _advance(self):
        super()._advance()          # ArithmeticProgression's version: subtract 1
        if self._current < 0:
            self._current = None    # tells __next__ to stop

print(list(CountdownProgression(5)))    # [5, 4, 3, 2, 1, 0]  (it ends, so list() is safe)
print([cls.__name__ for cls in CountdownProgression.__mro__])
# ['CountdownProgression', 'ArithmeticProgression', 'Progression', 'object']


# ---------- 6. Abstract Base Classes ----------

# Abstract base class (ABC): a class that exists only to be inherited from.
# You can't make an object of it directly
# Abstract method: a method the ABC declares but doesn't write.
#                  Every subclass MUST write it, or the subclass can't be
#                  made into objects either
# Concrete method: a normal method in the ABC. It can call the abstract
#                  methods, so it's written once and works for every subclass
#
# The book writes class Sequence(metaclass=ABCMeta).
# class Shape(ABC) is the shorter way to write the same thing

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Every subclass must write this"""

    @abstractmethod
    def perimeter(self):
        """Every subclass must write this"""

    # concrete method: works for every shape because it only relies on the
    # abstract methods, which each subclass is forced to provide
    def describe(self):
        return f"{type(self).__name__}: area {self.area():.2f}, perimeter {self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius

    def area(self):
        return math.pi * self._radius ** 2

    def perimeter(self):
        return 2 * math.pi * self._radius

class Square(Shape):
    def __init__(self, side):
        self._side = side

    def area(self):
        return self._side ** 2

    def perimeter(self):
        return 4 * self._side

class Triangle(Shape):      # forgot to write perimeter
    def __init__(self, base, height):
        self._base = base
        self._height = height

    def area(self):
        return 0.5 * self._base * self._height

for shape in [Circle(1), Square(2)]:
    print(shape.describe())     # Circle: area 3.14, perimeter 6.28 / Square: area 4.00, perimeter 8.00

try:
    Shape()                     # can't make an object of an ABC
except TypeError as e:
    print(e)    # Can't instantiate abstract class Shape without an implementation for abstract methods 'area', 'perimeter'

try:
    Triangle(3, 4)              # missing perimeter, so it's still abstract
except TypeError as e:
    print(e)    # Can't instantiate abstract class Triangle without an implementation for abstract method 'perimeter'

# Example: the book's Sequence ABC (2.4.3)
# A subclass writes only __len__ and __getitem__, and gets __contains__,
# index and count for free
class MySequence(ABC):
    """Our own version of a sequence base class"""

    @abstractmethod
    def __len__(self):
        """Return the length of the sequence"""

    @abstractmethod
    def __getitem__(self, j):
        """Return the element at index j"""

    def __contains__(self, val):
        for j in range(len(self)):
            if self[j] == val:
                return True
        return False

    def index(self, val):
        for j in range(len(self)):
            if self[j] == val:
                return j
        raise ValueError("value not in sequence")

    def count(self, val):
        k = 0
        for j in range(len(self)):
            if self[j] == val:
                k += 1
        return k

class Squares(MySequence):
    """The first n square numbers: 0, 1, 4, 9, 16, ..."""

    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n

    def __getitem__(self, j):
        if j < 0:
            j += self._n            # allow negative indexes like a list
        if not 0 <= j < self._n:
            raise IndexError("index out of range")
        return j * j                # computed, nothing is stored

sq = Squares(6)
print(len(sq))              # 6
print(sq[3])                # 9
print(sq[-1])               # 25
print(16 in sq)             # True   (MySequence's __contains__)
print(sq.index(25))         # 5      (MySequence's index)
print(sq.count(4))          # 1      (MySequence's count)
print(list(sq))             # [0, 1, 4, 9, 16, 25]

# Python ships this exact idea as collections.abc.Sequence. Write __len__ and
# __getitem__ and you also get __contains__, __iter__, __reversed__, index, count
class Cubes(Sequence):
    """The first n cube numbers: 0, 1, 8, 27, ..."""

    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n

    def __getitem__(self, j):
        if j < 0:
            j += self._n
        if not 0 <= j < self._n:
            raise IndexError("index out of range")
        return j ** 3

cubes = Cubes(5)
print(list(cubes))              # [0, 1, 8, 27, 64]
print(list(reversed(cubes)))    # [64, 27, 8, 1, 0]
print(cubes.index(27))          # 3
print(isinstance(cubes, Sequence))  # True
