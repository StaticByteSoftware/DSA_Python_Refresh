"""
Sets, Multisets, and Multimaps (section 10.5)

These are close relatives of the map, and all of them can be built on a hash
table, so the common operations are O(1) on average.

                stores                  can it repeat?       in Python
    set         elements                no                   set
    multiset    elements with counts    yes, elements        collections.Counter
    map         key -> one value        no, keys are unique  dict
    multimap    key -> many values      yes, keys            defaultdict(list)

To choose one, ask what question you need to answer:
    "Is it in there?"                       -> set
    "How many of it are in there?"          -> multiset
    "What is the value for this key?"       -> map
    "What are ALL the values for this key?" -> multimap
"""

from collections import Counter, defaultdict
from collections.abc import MutableSet


# 1. Same data, four containers
#    A book index: each term, and a page where it appears
INDEX_ENTRIES = [
    ("hash", 10),
    ("map", 10),
    ("hash", 12),
    ("set", 12),
    ("hash", 15),
    ("map", 15),
]


def compare_example():
    print("1. Same data, four containers")
    terms = [term for term, _ in INDEX_ENTRIES]
    print("  terms:   ", terms)

    # Set: which terms exist? The repeats are gone.
    # (sorted() is only here because a set has no order of its own)
    print("  set:     ", sorted(set(terms)))

    # Multiset: how many times does each term appear?
    print("  multiset:", Counter(terms))

    # Map: each key holds one value, so a new page overwrites the old one
    term_to_page = {}
    for term, page in INDEX_ENTRIES:
        term_to_page[term] = page
    print("  map:     ", term_to_page)

    # Multimap: each key keeps every value, so no pages are lost
    term_to_pages = defaultdict(list)
    for term, page in INDEX_ENTRIES:
        term_to_pages[term].append(page)
    print("  multimap:", dict(term_to_pages))


# 2. Set: unique elements with no values. It's like the keys of a map.
class MapBackedSet(MutableSet):
    """A set is a map without values, so this one stores elements as dict keys.

    MutableSet only needs these five methods, the same way MutableMapping only
    needed five for ListMap. It supplies remove, pop, clear, and the operators
    |, &, -, ^, and <=. Those operators build their result by passing an
    iterable to the constructor, so __init__ has to accept one.
    """

    def __init__(self, elements=()):
        self._map = {}
        for element in elements:
            self.add(element)

    def __contains__(self, element):
        return element in self._map

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def add(self, element):
        self._map[element] = None  # only the key matters

    def discard(self, element):
        self._map.pop(element, None)

    def __repr__(self):
        return f"MapBackedSet({list(self._map)})"


def set_example():
    print("\n2. Set: unique elements")

    # Duplicates are dropped
    colors = {"red", "green", "red"}
    print("  {'red', 'green', 'red'} has", len(colors), "elements")

    # Gotcha: {} is an empty dict, so an empty set has to be set()
    print("  type({}) is", type({}).__name__, "and type(set()) is", type(set()).__name__)

    # add, in, and discard are all O(1) on average
    colors.add("blue")
    colors.add("blue")  # already there, so nothing changes
    print("  'blue' in colors:", "blue" in colors, "| size:", len(colors))

    # discard ignores a missing element, but remove raises KeyError
    colors.discard("purple")
    try:
        colors.remove("purple")
    except KeyError as error:
        print("  remove raises KeyError for", error)

    # Set math. Small ints happen to print sorted here, but a set has no order.
    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    print("  a =", a, "and b =", b)
    print("  a | b, in either:     ", a | b)
    print("  a & b, in both:       ", a & b)
    print("  a - b, only in a:     ", a - b)
    print("  a ^ b, in exactly one:", a ^ b)
    print("  {3, 4} <= a, subset:  ", {3, 4} <= a)
    print("  a.isdisjoint({8, 9}): ", a.isdisjoint({8, 9}))

    # Elements must be hashable, just like dict keys. A frozenset is a set that
    # can't change, so it can go inside another set.
    try:
        {[1, 2]}
    except TypeError as error:
        print("  a list in a set:", error)
    print("  {frozenset({1, 2}), frozenset({2, 1})} has",
          len({frozenset({1, 2}), frozenset({2, 1})}), "element")

    # MutableSet gave MapBackedSet all of these operators for free
    c = MapBackedSet([1, 2, 2, 3])
    d = MapBackedSet([3, 4])
    print("  MapBackedSet:", c, "| c | d:", c | d, "| c & d:", c & d)


# 3. Multiset (also called a bag): like a set, but duplicates count
def multiset_example():
    print("\n3. Multiset: elements with counts")

    # A multiset is really a map of element -> count. Here's one by hand:
    counts = {}
    for letter in "banana":
        counts[letter] = counts.get(letter, 0) + 1
    print("  by hand:", counts)

    # Counter does the same thing. It's a subclass of dict.
    bag = Counter("banana")
    print("  Counter:", bag)

    # A missing element has a count of 0, so there's no KeyError
    print("  bag['z']:", bag["z"])

    # Gotcha: there are two sizes, and len() is only the distinct elements
    print("  distinct elements, len(bag):", len(bag))
    print("  total elements, sum(bag.values()):", sum(bag.values()))

    print("  bag.most_common(1):", bag.most_common(1))
    print("  sorted(bag.elements()):", sorted(bag.elements()))

    # Gotcha: a count of 0 doesn't remove the element
    bag["b"] -= 1
    print("  after bag['b'] -= 1:", bag, "| 'b' in bag:", "b" in bag)
    del bag["b"]
    print("  after del bag['b']:", bag, "| 'b' in bag:", "b" in bag)

    # Multiset math works on the counts
    a = Counter("aab")
    b = Counter("abb")
    print("  a =", a, "and b =", b)
    print("  a + b, add counts:", a + b)
    print("  a - b, subtract, dropping counts of 0 or less:", a - b)
    print("  a & b, smaller count:", a & b)
    print("  a | b, larger count: ", a | b)

    # The key difference from a set: a set ignores how many times things appear
    print('  set("aab") == set("abb"):', set("aab") == set("abb"))
    print('  Counter("aab") == Counter("abb"):', Counter("aab") == Counter("abb"))


# 4. Multimap: like a map, but one key can have many values
class MultiMap:
    """Based on the MultiMap in section 10.5.

    Python has no multimap class. The usual approach is a dict whose values are
    lists, which is what this wraps.
    """

    def __init__(self):
        self._map = {}  # key -> list of values
        self._n = 0  # number of (key, value) pairs, not number of keys

    def add(self, key, value):
        self._map.setdefault(key, []).append(value)
        self._n += 1

    def find(self, key):
        # Return one value for key, or raise KeyError if key is missing
        return self._map[key][0]

    def find_all(self, key):
        # Return a copy, so callers can't change the list stored in the map
        return list(self._map.get(key, []))

    def pop(self, key):
        # Remove and return one (key, value) pair
        values = self._map[key]
        value = values.pop()
        if not values:  # don't leave an empty list, or the key still looks present
            del self._map[key]
        self._n -= 1
        return key, value

    def keys(self):
        return self._map.keys()

    def __contains__(self, key):
        return key in self._map

    def __iter__(self):
        for key, values in self._map.items():
            for value in values:
                yield key, value

    def __len__(self):
        return self._n


def multimap_example():
    print("\n4. Multimap: one key, many values")

    index = MultiMap()
    for term, page in INDEX_ENTRIES:
        index.add(term, page)

    print("  find('hash'):", index.find("hash"))
    print("  find_all('hash'):", index.find_all("hash"))
    print("  find_all('tree'):", index.find_all("tree"))
    print("  all pairs:", list(index))

    # Gotcha: there are two sizes here too
    print("  total pairs, len(index):", len(index))
    print("  distinct keys, len(index.keys()):", len(index.keys()))

    # Popping the last value for a key removes the key too
    print("  pop('set'):", index.pop("set"), "| 'set' in index:", "set" in index)

    # In everyday code, skip the class and use defaultdict(list)
    friends = defaultdict(list)
    friends["ann"].append("bob")
    friends["ann"].append("cara")
    print("  defaultdict(list):", dict(friends))

    # Gotcha: reading a missing key with [] adds it. Use .get() to only read.
    print("  friends['zoe']:", friends["zoe"], "| 'zoe' in friends:", "zoe" in friends)
    print("  friends.get('yan', []):", friends.get("yan", []),
          "| 'yan' in friends:", "yan" in friends)

    # Use defaultdict(set) if a key shouldn't hold the same value twice
    tags = defaultdict(set)
    tags["post1"].add("python")
    tags["post1"].add("python")
    print("  defaultdict(set):", dict(tags))


# 5. Problems where the choice of container is the whole solution
def intersection(nums1, nums2):
    """LeetCode 349. Each shared value appears once, so use sets."""
    return list(set(nums1) & set(nums2))


def intersect_with_counts(nums1, nums2):
    """LeetCode 350. Shared values keep their repeats, so use multisets."""
    return list((Counter(nums1) & Counter(nums2)).elements())


def is_anagram(s, t):
    """LeetCode 242. The letter counts must match, so a set isn't enough."""
    return Counter(s) == Counter(t)


def build_graph(edges):
    """An adjacency list is a multimap of node -> all of its neighbors.

    Graph problems like LeetCode 207 start this way. group_anagrams in
    hashTable_example.py is a multimap too: sorted letters -> all the words.
    """
    graph = defaultdict(list)
    for start, end in edges:
        graph[start].append(end)
    return dict(graph)


def leetcode_examples():
    print("\n5. Picking the right one for a problem")
    print("  intersection([1, 2, 2, 1], [2, 2]):", intersection([1, 2, 2, 1], [2, 2]))
    print("  intersect_with_counts([1, 2, 2, 1], [2, 2]):",
          intersect_with_counts([1, 2, 2, 1], [2, 2]))
    print('  is_anagram("listen", "silent"):', is_anagram("listen", "silent"))
    print('  is_anagram("aab", "abb"):', is_anagram("aab", "abb"))
    print("  build_graph([(1, 2), (1, 3), (2, 3)]):", build_graph([(1, 2), (1, 3), (2, 3)]))


if __name__ == "__main__":
    compare_example()
    set_example()
    multiset_example()
    multimap_example()
    leetcode_examples()
