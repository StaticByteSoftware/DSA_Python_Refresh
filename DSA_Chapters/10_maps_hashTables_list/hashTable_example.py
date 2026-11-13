"""
Hash Tables in Python

A hash table stores key-value pairs in an array of "buckets". It finds the
bucket for a key in two steps:

    key  --hash()-->  integer  --% capacity-->  bucket index

The index is calculated, not searched for, so a lookup doesn't need to scan the
whole table. Python's dict and set are both hash tables.

What you need to know (each one has an example below):
    1. A hash function turns a key into a bucket index
    2. Collisions happen when two keys get the same index
    3. Separate chaining handles collisions with a list in each bucket
    4. Linear probing handles collisions by moving to the next open slot
    5. The load factor tracks how full the table is, and resizing keeps it low
    6. Keys must be hashable, and equal keys must have equal hashes
    7. Lookups are O(1) on average, but O(n) if every key collides
    8. In real code you use dict and set, which solve many LeetCode problems

                average   worst
    lookup      O(1)      O(n)
    insert      O(1)*     O(n)
    delete      O(1)      O(n)
    * amortized: most inserts are fast, but an occasional one triggers a resize
"""

from collections import Counter, defaultdict
from collections.abc import MutableMapping
from timeit import timeit


# 1. Hash function: key -> integer -> bucket index
def hash_function_example():
    print("1. Hash function")

    # Small integers hash to themselves
    print("  hash(42) =", hash(42))

    # String hashes are big, and they change every time you run the program.
    # Python randomizes them for security, so never save a hash for later.
    print('  hash("cat") =', hash("cat"))

    # Equal values always have equal hashes, even across types
    print("  hash(1) == hash(1.0):", hash(1) == hash(1.0))

    # % capacity squeezes the hash into a valid index. The book also covers the
    # MAD method, ((a * h + b) % p) % capacity, which spreads keys more evenly.
    capacity = 8
    for key in ["cat", "dog", 42]:
        print(f"  {key!r} goes in bucket {hash(key) % capacity} of {capacity}")


# 2. Collisions: different keys, same bucket
def collision_example():
    print("\n2. Collisions")

    # There are far more possible keys than buckets, so collisions can't be
    # avoided. A hash table has to have a plan for them.
    capacity = 8
    for key in [3, 11, 19]:
        print(f"  {key} % {capacity} = {key % capacity}")


# 3. Separate chaining: each bucket holds a list of the pairs that landed there
class ChainingHashTable(MutableMapping):
    """A map that handles collisions with a list in each bucket.

    Like ListMap in maps_dictionaries.py, it's another way to implement a map.
    MutableMapping supplies get, items, pop, `in`, and the rest.
    """

    MAX_LOAD = 0.75

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._n = 0

    def _bucket_for(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def __getitem__(self, key):
        for k, v in self._bucket_for(key):
            if k == key:  # a bucket can hold other keys, so compare each one
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        bucket = self._bucket_for(key)
        for pair in bucket:
            if pair[0] == key:  # key already exists, so replace its value
                pair[1] = value
                return
        bucket.append([key, value])
        self._n += 1
        if self.load_factor() > self.MAX_LOAD:
            self._resize(2 * len(self._buckets))

    def __delitem__(self, key):
        bucket = self._bucket_for(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._n -= 1
                return
        raise KeyError(key)

    def __iter__(self):
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def __len__(self):
        return self._n

    def __repr__(self):
        return repr(self._buckets)

    def capacity(self):
        return len(self._buckets)

    def load_factor(self):
        return self._n / len(self._buckets)

    def _resize(self, capacity):
        # A key's index depends on the capacity, so every key must be re-added.
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(capacity)]
        self._n = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value


def chaining_example():
    print("\n3. Separate chaining")
    table = ChainingHashTable()
    table[3] = "a"
    table[11] = "b"
    table[19] = "c"  # all three keys land in bucket 3
    print(" ", table)
    print("  table[11] =", table[11])

    del table[11]
    print("  after deleting 11:", table)


# 4. Linear probing: each slot holds one pair. If a slot is taken, try the next.
#    Python's dict also keeps pairs in the table itself ("open addressing"), but
#    it jumps around instead of checking neighboring slots.
EMPTY = "empty"  # nothing has ever been stored in this slot
DELETED = "deleted"  # a pair used to be here (also called a "tombstone")


class ProbingHashTable(MutableMapping):
    """A map that handles collisions by moving to the next open slot."""

    # Stay well under half full. Taken slots clump together ("clustering"),
    # which makes probes longer and longer as the table fills up.
    MAX_LOAD = 0.5

    def __init__(self, capacity=8):
        self._slots = [EMPTY] * capacity
        self._n = 0

    def _probe(self, key):
        # Give each index to try, wrapping around at the end of the table
        capacity = len(self._slots)
        start = hash(key) % capacity
        for step in range(capacity):
            yield (start + step) % capacity

    @staticmethod
    def _is_open(slot):
        return slot is EMPTY or slot is DELETED

    def _find(self, key):
        # Return the index holding key, or None if key isn't in the table
        for i in self._probe(key):
            slot = self._slots[i]
            if slot is EMPTY:  # key would have been placed here, so it's absent
                return None
            if slot is not DELETED and slot[0] == key:
                return i
        return None

    def __getitem__(self, key):
        i = self._find(key)
        if i is None:
            raise KeyError(key)
        return self._slots[i][1]

    def __setitem__(self, key, value):
        i = self._find(key)
        if i is not None:  # key already exists, so replace its value
            self._slots[i][1] = value
            return
        for i in self._probe(key):
            if self._is_open(self._slots[i]):
                self._slots[i] = [key, value]
                self._n += 1
                break
        if self._n / len(self._slots) > self.MAX_LOAD:
            self._resize(2 * len(self._slots))

    def __delitem__(self, key):
        i = self._find(key)
        if i is None:
            raise KeyError(key)
        self._slots[i] = DELETED
        self._n -= 1

    def __iter__(self):
        for slot in self._slots:
            if not self._is_open(slot):
                yield slot[0]

    def __len__(self):
        return self._n

    def __repr__(self):
        return repr(self._slots)

    def _resize(self, capacity):
        # Re-adding only the live pairs also clears out the DELETED markers
        old_slots = self._slots
        self._slots = [EMPTY] * capacity
        self._n = 0
        for slot in old_slots:
            if not self._is_open(slot):
                self[slot[0]] = slot[1]


def probing_example():
    print("\n4. Linear probing")
    table = ProbingHashTable()
    table[3] = "a"
    table[11] = "b"  # slot 3 is taken, so this goes in slot 4
    table[19] = "c"  # slots 3 and 4 are taken, so this goes in slot 5
    print(" ", table)

    # A DELETED marker tells a search to keep going
    del table[11]
    print("  after deleting 11:", table)
    print("  is 19 still found?", 19 in table)

    # Why not just empty the slot? Because a search stops at an EMPTY slot, so
    # it would never reach 19. This is the classic linear probing bug.
    table._slots[4] = EMPTY
    print("  if slot 4 were EMPTY, is 19 found?", 19 in table)


# 5. Load factor: items / capacity
#    A fuller table means more collisions, so tables grow before they get full.
#    Common limits are 0.9 for chaining and 0.5 for probing. Python's dict stays
#    under 2/3. Doubling makes resizes rare, the same reason appending to the
#    DynamicArray from chapter 5 is amortized O(1).
def resizing_example():
    print("\n5. Load factor and resizing")
    table = ChainingHashTable(capacity=4)
    for key in range(1, 21):
        old_capacity = table.capacity()
        table[key] = key
        if table.capacity() != old_capacity:
            print(f"  item {key}: capacity {old_capacity} -> {table.capacity()}, "
                  f"load factor is now {table.load_factor():.2f}")


# 6. Hashable keys: a key needs a __hash__ that never changes
#    If a == b, then hash(a) must equal hash(b), or the table can't find the key.
class Point:
    """A custom key. If you define __eq__ without __hash__, Python makes the
    class unhashable, so you have to write both."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))  # hash the same values __eq__ compares


def hashable_keys_example():
    print("\n6. Hashable keys")

    # Immutable built-ins (int, str, tuple) work. Mutable ones (list, dict, set)
    # don't. A tuple only works if everything inside it is hashable too.
    locations = {(1, 2): "tuple keys work"}
    print(" ", locations[(1, 2)])
    try:
        locations[[1, 2]] = "list keys fail"
    except TypeError as error:
        print("  list key:", error)

    # Two separate but equal objects count as the same key
    print("  Point(1, 2) in {Point(1, 2)}:", Point(1, 2) in {Point(1, 2)})

    # Never change a key after adding it. Its hash changes, so the table looks
    # in the wrong bucket and the pair is lost.
    point = Point(1, 2)
    treasure = {point: "gold"}
    point.x = 99
    print("  key changed after adding it, is it found?", point in treasure)


# 7. Worst case: if every key collides, the table acts like a plain list
class BadKey:
    """Every instance has the same hash, so every key collides."""

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return 1


class GoodKey(BadKey):
    """Same as BadKey, but with a hash that spreads keys out."""

    def __hash__(self):
        return hash(self.value)


def worst_case_example():
    print("\n7. Worst case: O(n) per operation")
    n = 2_000
    good_time = timeit(lambda: {GoodKey(i): i for i in range(n)}, number=1)
    bad_time = timeit(lambda: {BadKey(i): i for i in range(n)}, number=1)
    print(f"  add {n:,} keys with a good hash: {good_time:.5f}s")
    print(f"  add {n:,} keys with a bad hash:  {bad_time:.5f}s")


# 8. In practice: use dict and set. These are common LeetCode patterns.
def two_sum(nums, target):
    """LeetCode 1. Remember what you've seen: O(n) instead of checking all pairs."""
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []


def contains_duplicate(nums):
    """LeetCode 217. `in` on a set is O(1), but `in` on a list is O(n)."""
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def first_unique_char(s):
    """LeetCode 387. Counter builds a dict of value -> how many times it appears."""
    counts = Counter(s)
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    return -1


def group_anagrams(words):
    """LeetCode 49. Anagrams have the same sorted letters, so use that as the key.

    The key is a tuple because a list isn't hashable. defaultdict creates the
    empty list the first time a key shows up.
    """
    groups = defaultdict(list)
    for word in words:
        groups[tuple(sorted(word))].append(word)
    return list(groups.values())


def leetcode_examples():
    print("\n8. dict and set in practice")
    print("  two_sum([2, 7, 11, 15], 9):", two_sum([2, 7, 11, 15], 9))
    print("  contains_duplicate([1, 2, 3, 1]):", contains_duplicate([1, 2, 3, 1]))
    print('  first_unique_char("leetcode"):', first_unique_char("leetcode"))
    print('  group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]):')
    print("   ", group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

    # dict remembers insertion order (since Python 3.7). set does not, so never
    # rely on the order of a set.
    print("  dict keeps order:", list({"b": 1, "a": 2, "c": 3}))


if __name__ == "__main__":
    hash_function_example()
    collision_example()
    chaining_example()
    probing_example()
    resizing_example()
    hashable_keys_example()
    worst_case_example()
    leetcode_examples()
