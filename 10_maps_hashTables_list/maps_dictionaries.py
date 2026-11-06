"""
Dictionary vs. Map in Python

MAP  -> the abstract idea (an "abstract data type"). A collection of unique keys,
        each linked to a value. It says WHAT you can do (look up, insert, delete)
        but not HOW it is done. Python expresses this idea with the abstract
        classes collections.abc.Mapping and collections.abc.MutableMapping.

DICT -> a concrete, built-in class that implements a map using a hash table.

So every dict is a map, but not every map is a dict.

Note: the built-in map() function is unrelated. It applies a function to every
item in an iterable. Same word, different thing.
"""

from collections.abc import Mapping, MutableMapping
from timeit import timeit


class ListMap(MutableMapping):
    """A map with no hash table: just a list of [key, value] pairs.

    It only defines the five required methods. MutableMapping supplies the rest
    (get, items, keys, values, pop, update, `in`, ...).
    """

    def __init__(self):
        self._pairs = []

    def __getitem__(self, key):  # O(n): may have to check every pair
        for k, v in self._pairs:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):  # O(n)
        for pair in self._pairs:
            if pair[0] == key:
                pair[1] = value
                return
        self._pairs.append([key, value])

    def __delitem__(self, key):  # O(n)
        for i, pair in enumerate(self._pairs):
            if pair[0] == key:
                del self._pairs[i]
                return
        raise KeyError(key)

    def __iter__(self):
        return (k for k, _ in self._pairs)

    def __len__(self):
        return len(self._pairs)


def show_ages(ages: Mapping):
    """Works with ANY map, because it only relies on the map interface."""
    for name, age in ages.items():
        print(f"  {name} is {age}")
    print(f"  Is Ann in there? {'Ann' in ages}")


if __name__ == "__main__":
    real_dict = {"Ann": 30, "Bob": 25}

    list_map = ListMap()
    list_map["Ann"] = 30
    list_map["Bob"] = 25

    print("1. Same map interface, so the same code works on both")
    print(" dict:")
    show_ages(real_dict)
    print(" ListMap:")
    show_ages(list_map)

    print("\n2. Both are maps, but only one is a dict")
    print("  dict is a Mapping:   ", isinstance(real_dict, Mapping))
    print("  ListMap is a Mapping:", isinstance(list_map, Mapping))
    print("  ListMap is a dict:   ", isinstance(list_map, dict))

    print("\n3. Different implementations have different rules")
    unhashable_key = [1, 2]
    list_map[unhashable_key] = "ok"  # ListMap only compares keys with ==
    print("  ListMap accepts a list as a key:", list_map[unhashable_key])
    try:
        real_dict[unhashable_key] = "fails"  # a hash table must hash the key
    except TypeError as error:
        print("  dict rejects it:", error)

    print("\n4. Different implementations have different speed")
    n = 2_000
    big_dict = {i: i for i in range(n)}
    big_list_map = ListMap()
    for i in range(n):
        big_list_map[i] = i

    last_key = n - 1  # the worst case for ListMap: it is at the end of the list
    dict_time = timeit(lambda: big_dict[last_key], number=1_000)
    list_map_time = timeit(lambda: big_list_map[last_key], number=1_000)
    print(f"  1,000 lookups in dict:    {dict_time:.6f}s  (average O(1))")
    print(f"  1,000 lookups in ListMap: {list_map_time:.6f}s  (O(n))")

    print("\n5. The built-in map() function is a separate thing")
    print(" ", list(map(str.upper, ["ann", "bob"])))
