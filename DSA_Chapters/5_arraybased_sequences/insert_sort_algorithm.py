# chapter 5: Array Based Sequences
    # 5.5.2 Sorting a Sequence: Insertion Sort
import bisect
import random

# Sorting: putting the items of a sequence in order (smallest to largest,
#          A to Z...). "Nondecreasing" order means each item is <= the next,
#          which allows repeats like [1, 2, 2, 3]
#
# Insertion sort is the way most people sort a hand of playing cards:
#   pick up one card at a time and slide it left into its place among
#   the cards you're already holding, which are always kept in order
#
# The big idea: the list is split into two parts
#   [ sorted part | unsorted part ]
#   - At the start, the sorted part is just the first item
#     (one item on its own is always "sorted")
#   - Each pass takes the FIRST item of the unsorted part (called cur),
#     and slides it left into the right place in the sorted part.
#     Every bigger item in the sorted part moves one spot right to make room
#   - After each pass the sorted part is one item longer.
#     When the unsorted part is empty, the whole list is sorted
#
# Why this is an array-based algorithm:
#   It needs two things a python list (a dynamic array) does well:
#     1. jump straight to any index:  A[j]  is O(1)
#     2. move items over by one spot to open a gap
#   Step 2 is the exact same shifting loop as insert() in
#   insert_delete_dynamicArray.py: walk from the right and copy each item
#   one spot over, A[j] = A[j-1]


# ---------- 1. Defining Insertion Sort ----------

# How to write it, step by step:
#   1. Outer loop: k goes from 1 to n-1. A[0:k] is the sorted part,
#      and A[k] is the next item to insert
#   2. Save cur = A[k]. Now index k is a free slot (a "hole") because
#      its value is safe in cur
#   3. Inner loop: start at j = k. While the item left of the hole is
#      bigger than cur, copy it right into the hole (A[j] = A[j-1]).
#      That moves the hole one spot left (j -= 1)
#   4. Stop when you reach the front (j == 0) or the item on the left is
#      <= cur. The hole is where cur belongs, so drop it in: A[j] = cur
#
# Pseudocode (like the book):
#   for k from 1 to n-1:
#       cur = A[k]
#       j = k
#       while j > 0 and A[j-1] > cur:
#           A[j] = A[j-1]
#           j = j - 1
#       A[j] = cur

def insertion_sort(A):
    """Sort list A into nondecreasing order, in place."""
    for k in range(1, len(A)):          # A[0:k] is already sorted
        cur = A[k]                      # the item to insert; index k is now the hole
        j = k                           # j is where the hole is
        while j > 0 and A[j-1] > cur:   # item left of the hole is too big
            A[j] = A[j-1]               # shift it right, into the hole
            j -= 1                      # the hole moves one spot left
        A[j] = cur                      # drop cur into the hole

nums = [5, 2, 4, 6, 1, 3]
insertion_sort(nums)
print(nums)                     # [1, 2, 3, 4, 5, 6]

# It sorts in place: it changes the list you hand it and returns None,
# just like list.sort(). (sorted() is the one that returns a new list)
result = insertion_sort([3, 1, 2])
print(result)                   # None


# ---------- 2. How It Works: Watching Every Step ----------

# Same algorithm, but it prints a picture after every move.
#   _  is the hole (the slot cur came out of, moving left as items shift)
#   |  splits the sorted part (left) from the unsorted part (right)

def _picture(A, sorted_end, hole=None):
    """Draw A like [2, _, 5 | 6, 1, 3]"""
    left = ["_" if i == hole else str(A[i]) for i in range(sorted_end)]
    right = [str(x) for x in A[sorted_end:]]
    if not right:
        return "[" + ", ".join(left) + "]"
    return "[" + ", ".join(left) + " | " + ", ".join(right) + "]"

def insertion_sort_explained(A):
    """Insertion sort that narrates every comparison and shift."""
    print(f"start:                              {_picture(A, 1)}")
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        print(f"pass k={k}: take out cur = {cur}".ljust(36) + _picture(A, k + 1, hole=j))
        while j > 0 and A[j-1] > cur:
            A[j] = A[j-1]
            j -= 1
            print(f"    {A[j]} > {cur}? yes, shift {A[j]} right".ljust(36) + _picture(A, k + 1, hole=j))
        if j == 0:
            print("    reached the front, stop")
        else:
            print(f"    {A[j-1]} > {cur}? no, stop")
        A[j] = cur
        print(f"    drop {cur} into index {j}".ljust(36) + _picture(A, k + 1))

insertion_sort_explained([5, 2, 4, 6, 1, 3])
# start:                              [5 | 2, 4, 6, 1, 3]
# pass k=1: take out cur = 2          [5, _ | 4, 6, 1, 3]
#     5 > 2? yes, shift 5 right       [_, 5 | 4, 6, 1, 3]
#     reached the front, stop
#     drop 2 into index 0             [2, 5 | 4, 6, 1, 3]
# pass k=2: take out cur = 4          [2, 5, _ | 6, 1, 3]
#     5 > 4? yes, shift 5 right       [2, _, 5 | 6, 1, 3]
#     2 > 4? no, stop
#     drop 4 into index 1             [2, 4, 5 | 6, 1, 3]
# pass k=3: take out cur = 6          [2, 4, 5, _ | 1, 3]
#     5 > 6? no, stop
#     drop 6 into index 3             [2, 4, 5, 6 | 1, 3]
# pass k=4: take out cur = 1          [2, 4, 5, 6, _ | 3]
#     6 > 1? yes, shift 6 right       [2, 4, 5, _, 6 | 3]
#     5 > 1? yes, shift 5 right       [2, 4, _, 5, 6 | 3]
#     4 > 1? yes, shift 4 right       [2, _, 4, 5, 6 | 3]
#     2 > 1? yes, shift 2 right       [_, 2, 4, 5, 6 | 3]
#     reached the front, stop
#     drop 1 into index 0             [1, 2, 4, 5, 6 | 3]
# pass k=5: take out cur = 3          [1, 2, 4, 5, 6, _]
#     6 > 3? yes, shift 6 right       [1, 2, 4, 5, _, 6]
#     5 > 3? yes, shift 5 right       [1, 2, 4, _, 5, 6]
#     4 > 3? yes, shift 4 right       [1, 2, _, 4, 5, 6]
#     2 > 3? no, stop
#     drop 3 into index 2             [1, 2, 3, 4, 5, 6]
#
# Note: in memory the "hole" isn't empty. It still holds an old value
# (a duplicate of the item that was just copied right). That's fine,
# because cur has the value we need and gets written there at the end

# Why it's correct (loop invariant):
#   At the start of every pass k, A[0:k] holds the first k original items
#   in sorted order. Each pass puts A[k] into its place, so A[0:k+1] is
#   sorted. That's true for k=1 (one item) and every pass keeps it true,
#   so after the last pass, all of A is sorted


# ---------- 3. What It Means: Running Time ----------

# Version that counts the work instead of printing it
#   comparisons: how many times we checked A[j-1] > cur
#   shifts:      how many times we moved an item right
def insertion_sort_counted(A):
    comparisons = 0
    shifts = 0
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j > 0:
            comparisons += 1
            if A[j-1] > cur:
                A[j] = A[j-1]
                shifts += 1
                j -= 1
            else:
                break
        A[j] = cur
    return comparisons, shifts

# The amount of work depends on how out-of-order the list starts out:
#
#   Best case: already sorted
#     Every pass does 1 comparison and 0 shifts (cur is already in place)
#     n - 1 comparisons total            -> O(n)
#
#   Worst case: sorted backwards
#     Pass k has to shift ALL k items in the sorted part
#     1 + 2 + 3 + ... + (n-1) = n(n-1)/2 -> O(n^2)
#
#   Average case: random order
#     cur moves about halfway back each pass, about n^2/4 -> still O(n^2)
#
#   Extra memory: just cur, j and k, no matter how big A is -> O(1)

n = 1000
rng = random.Random(1)      # fixed seed so the "random" list is the same every run

already_sorted = list(range(n))
backwards = list(range(n, 0, -1))
shuffled = list(range(n))
rng.shuffle(shuffled)
nearly_sorted = list(range(n))
for i in range(0, n, 100):  # swap 10 neighbor pairs, everything else in place
    nearly_sorted[i], nearly_sorted[i+1] = nearly_sorted[i+1], nearly_sorted[i]

print("case            comparisons    shifts")
for name, data in [("already sorted", already_sorted), ("nearly sorted", nearly_sorted),
                   ("random", shuffled), ("backwards", backwards)]:
    comparisons, shifts = insertion_sort_counted(data)
    print(f"{name:<15} {comparisons:>11,} {shifts:>9,}")
# case            comparisons    shifts
# already sorted          999         0
# nearly sorted         1,008        10
# random              250,099   249,107
# backwards           499,500   499,500

# Same n, same algorithm, 500 times more work. The input order matters a lot

# What O(n^2) looks like: double n and the work goes up 4 times
# What O(n) looks like:   double n and the work goes up 2 times
print("    n   backwards shifts   sorted comparisons")
for size in [100, 200, 400, 800]:
    _, worst = insertion_sort_counted(list(range(size, 0, -1)))
    best, _ = insertion_sort_counted(list(range(size)))
    print(f"{size:>5} {worst:>18,} {best:>20,}")
#     n   backwards shifts   sorted comparisons
#   100              4,950                   99
#   200             19,900                  199
#   400             79,800                  399
#   800            319,600                  799

# The real meaning of shifts: inversions
# An inversion is a pair of items in the wrong order (a bigger one comes
# before a smaller one). Each shift fixes exactly one inversion, so
#     shifts = number of inversions in the list
#     running time = O(n + inversions)
# A sorted list has 0 inversions, a backwards one has n(n-1)/2 (every pair),
# which is why the cases above came out the way they did


# ---------- 4. What It Means: Properties ----------

# In place: sorts inside the list it's given, O(1) extra memory (see above)

# Stable: items that compare equal stay in the order they started in.
# This comes from using > (not >=) in the while loop: cur stops as soon as
# it meets an equal item, so it never jumps over it

def insertion_sort_by(A, key):
    """Insertion sort that compares key(item) instead of the item itself,
    like sorted(A, key=...)"""
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j > 0 and key(A[j-1]) > key(cur):
            A[j] = A[j-1]
            j -= 1
        A[j] = cur

grades = [("Ana", 90), ("Ben", 85), ("Cal", 90), ("Dee", 85)]
insertion_sort_by(grades, key=lambda student: student[1])     # sort by grade
print(grades)   # [('Ben', 85), ('Dee', 85), ('Ana', 90), ('Cal', 90)]
                # Ben is still before Dee, Ana still before Cal

# Change > to >= and it's no longer stable: equal items get jumped over
def insertion_sort_by_unstable(A, key):
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j > 0 and key(A[j-1]) >= key(cur):
            A[j] = A[j-1]
            j -= 1
        A[j] = cur

grades = [("Ana", 90), ("Ben", 85), ("Cal", 90), ("Dee", 85)]
insertion_sort_by_unstable(grades, key=lambda student: student[1])
print(grades)   # [('Dee', 85), ('Ben', 85), ('Cal', 90), ('Ana', 90)]  (ties flipped)

# Why stable matters: sorting by two things. Sort by the less important key
# first, then by the more important key. Stability keeps the first sort's
# order inside each group of ties
roster = [("Dee", 85), ("Cal", 90), ("Ben", 85), ("Ana", 90), ("Eve", 75)]
insertion_sort_by(roster, key=lambda student: student[0])     # by name
insertion_sort_by(roster, key=lambda student: student[1])     # then by grade
print(roster)   # [('Eve', 75), ('Ben', 85), ('Dee', 85), ('Ana', 90), ('Cal', 90)]
                # by grade, and names are A-Z within each grade

# Adaptive: the closer to sorted the list already is, the faster it runs
# (see "nearly sorted" in section 3)

# Online: it can sort items as they arrive, one at a time. Each new item
# is just one more pass (see the leaderboard in section 6)

# Comparison-based: it only ever asks "is a > b?", so it sorts anything
# python can compare: numbers, strings, tuples, your own classes...
words = ["pear", "apple", "fig", "banana"]
insertion_sort(words)
print(words)    # ['apple', 'banana', 'fig', 'pear']

points = [(2, "b"), (1, "z"), (2, "a")]     # tuples compare item by item
insertion_sort(points)
print(points)   # [(1, 'z'), (2, 'a'), (2, 'b')]

# A class only needs __lt__ (see class_definitions.py, section 7).
# For A[j-1] > cur, python first tries A[j-1].__gt__(cur). Student doesn't
# have one, so python flips it around and calls cur.__lt__(A[j-1]) instead
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

    def __lt__(self, other):
        return self.gpa < other.gpa

    def __repr__(self):
        return f"{self.name}({self.gpa})"

students = [Student("Ana", 3.2), Student("Ben", 3.9), Student("Cal", 2.8)]
insertion_sort(students)
print(students)  # [Cal(2.8), Ana(3.2), Ben(3.9)]


# ---------- 5. Variations ----------

# Descending order (largest first): flip > to <
def insertion_sort_descending(A):
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j > 0 and A[j-1] < cur:
            A[j] = A[j-1]
            j -= 1
        A[j] = cur

nums = [5, 2, 4, 6, 1, 3]
insertion_sort_descending(nums)
print(nums)     # [6, 5, 4, 3, 2, 1]

# Swap version: you'll see this one a lot online and in interviews.
# It works, but each move is a swap (two writes) instead of one shift, and
# cur gets written over and over instead of once. The hole version is better
def insertion_sort_swaps(A):
    for k in range(1, len(A)):
        j = k
        while j > 0 and A[j-1] > A[j]:
            A[j-1], A[j] = A[j], A[j-1]
            j -= 1

nums = [5, 2, 4, 6, 1, 3]
insertion_sort_swaps(nums)
print(nums)     # [1, 2, 3, 4, 5, 6]

# Binary insertion sort: the sorted part is sorted, so binary search can
# find where cur goes in O(log n) comparisons instead of O(n).
# bisect_right (ch 4 binary search, built into python) returns the spot
# AFTER any equal items, which keeps it stable.
# BUT the items still have to shift right to make room, which is O(n) per
# pass, so the worst case is still O(n^2). Fewer comparisons, same moves
def binary_insertion_sort(A):
    for k in range(1, len(A)):
        cur = A[k]
        j = bisect.bisect_right(A, cur, 0, k)   # where cur goes in A[0:k]
        A[j+1:k+1] = A[j:k]                     # shift that chunk right by one
        A[j] = cur

nums = [5, 2, 4, 6, 1, 3]
binary_insertion_sort(nums)
print(nums)     # [1, 2, 3, 4, 5, 6]


# ---------- 6. Problems You Can Solve With It ----------

# Problem 1: keep a list sorted as new items arrive (online sorting)
# Example: a top-5 leaderboard. Each new score is ONE pass of insertion
# sort: put it at the end, slide it left into place. O(k) per new score
# instead of re-sorting the whole list
def add_score(top_scores, score, limit=5):
    """Insert score into top_scores (kept high to low), keep only the best limit"""
    top_scores.append(score)            # new item starts at the end, like A[k]
    j = len(top_scores) - 1
    while j > 0 and top_scores[j-1] < score:    # < because it's high to low
        top_scores[j] = top_scores[j-1]
        j -= 1
    top_scores[j] = score
    if len(top_scores) > limit:
        top_scores.pop()                # drop the lowest score

leaderboard = []
for score in [40, 95, 72, 88, 60, 99, 15, 91]:
    add_score(leaderboard, score)
print(leaderboard)      # [99, 95, 91, 88, 72]

# python has this built in for low-to-high lists: bisect.insort
# (binary search for the spot, then shift)
readings = [10, 20, 30, 40]
bisect.insort(readings, 25)
print(readings)         # [10, 20, 25, 30, 40]

# Problem 2: sort data that is almost sorted already
# Example: events logged by timestamp where a few arrived a little late.
# Each late event only moves back a couple of spots, so this is close to O(n)
events = [(1, "login"), (2, "view"), (4, "click"), (3, "scroll"),
          (5, "view"), (7, "buy"), (6, "click"), (8, "logout")]
comparisons, shifts = insertion_sort_counted(events)
print([t for t, _ in events])       # [1, 2, 3, 4, 5, 6, 7, 8]
print(comparisons, shifts)          # 9 2   (only 2 items had to move)

# A "k-sorted" list: every item is at most k spots from where it belongs.
# Each pass shifts at most k items, so insertion sort is O(n * k).
# For small k, that beats O(n log n) sorts
k_sorted = [2, 1, 3, 5, 4, 6, 8, 7, 9]   # k = 1
comparisons, shifts = insertion_sort_counted(k_sorted)
print(k_sorted, shifts)             # [1, 2, 3, 4, 5, 6, 7, 8, 9] 3

# Problem 3: measure how unsorted a list is (count inversions)
# shifts = inversions, so counting shifts on a copy gives the answer
# Example: how different are two people's rankings?
# Write the friend's ranking in terms of your positions and count
# the pairs that are out of order (0 = same ranking)
def count_inversions(A):
    _, shifts = insertion_sort_counted(list(A))     # copy, so A isn't changed
    return shifts

my_ranking = ["Inception", "Up", "Jaws", "Heat", "Alien"]
friend_ranking = ["Up", "Inception", "Heat", "Alien", "Jaws"]
my_position = {movie: i for i, movie in enumerate(my_ranking)}
as_my_positions = [my_position[movie] for movie in friend_ranking]
print(as_my_positions)                      # [1, 0, 3, 4, 2]
print(count_inversions(as_my_positions))    # 3  (3 pairs ranked differently)

# Problem 4: sorting small lists
# For a few dozen items, insertion sort is often faster than the "fast"
# O(n log n) sorts because each step is so simple. Python's own sort()
# uses binary insertion sort on short runs (up to 64 items) and then
# merges the runs together

# LeetCode problems that use it:
#   35  Search Insert Position   find where cur would go (the bisect step)
#   147 Insertion Sort List      same algorithm on a linked list. No
#                                shifting needed (just relink the node),
#                                but you can't walk backwards, so you
#                                search for the spot from the front
#   912 Sort an Array            insertion sort is too slow here:
#                                n can be 50,000, and 50,000^2 / 2 is about
#                                1.25 billion steps. Needs O(n log n)


# ---------- 7. When To Use It (and When Not To) ----------

# Use it when:
#   - the list is small (a few dozen items)
#   - the list is already nearly sorted
#   - items arrive one at a time and the list has to stay sorted
#   - you need stable, in-place sorting with no extra memory
# Don't use it when:
#   - the list is big and in random order. O(n^2) gets slow fast:
#     10x the items = 100x the work
#
# sort             best        average     worst       extra memory  stable
# insertion        O(n)        O(n^2)      O(n^2)      O(1)          yes
# selection        O(n^2)      O(n^2)      O(n^2)      O(1)          no
# bubble           O(n)        O(n^2)      O(n^2)      O(1)          yes
# merge (ch 12)    O(n log n)  O(n log n)  O(n log n)  O(n)          yes
# quick (ch 12)    O(n log n)  O(n log n)  O(n^2)      O(log n)      no
# python sort()    O(n)        O(n log n)  O(n log n)  O(n)          yes
# (bubble's O(n) best case needs the "stop if no swaps" check)


# ---------- 8. Common Mistakes ----------

# Mistake 1: leaving out j > 0
# In Java this crashes right away. In python, A[-1] is the LAST item, so
# when j reaches 0 the loop keeps going and starts reading and writing the
# wrong end of the list
def insertion_sort_no_check(A):
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while A[j-1] > cur:         # missing j > 0
            A[j] = A[j-1]
            j -= 1
        A[j] = cur

try:
    insertion_sort_no_check([3, 1, 2])
except IndexError as e:
    print(e)        # list index out of range  (crashes after scrambling the list)

bad = [3, 1, 1, 5]
insertion_sort_no_check(bad)
print(bad)          # [1, 1, 5, 3]  (wrong, and no error at all!)

# Mistake 2: using >= instead of >
#   Still sorts, but it's no longer stable and it does extra shifts
#   (see section 4)

# Mistake 3: comparing to A[j] instead of cur
#   while j > 0 and A[j-1] > A[j]  only works in the swap version.
#   In the hole version A[j] gets overwritten by the shift, so after the
#   first shift you'd be comparing against the wrong value

# Mistake 4: expecting a new list back
#   sorted_nums = insertion_sort(nums)  gives None. It changes nums itself
