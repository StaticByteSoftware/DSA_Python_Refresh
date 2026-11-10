# DSA_Python_Refresh

My practice repo for getting better at Python and learning data structures and algorithms. I'm working through the textbook *Data Structures and Algorithms in Python* by Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser, and solving LeetCode problems along the way.

## Textbook chapters

Each folder matches a chapter of the book and holds the examples I wrote while reading it.

| Chapter | Folder | Topics |
|---|---|---|
| 1. Python Primer | [1_python_intro](1_python_intro/) | Functions, input and output, exceptions, iterators and generators, conditional expressions, comprehensions, scopes and namespaces (LEGB), a GPA calculator |
| 2. Object-Oriented Programming | [2_object_oriented](2_object_oriented/) | Class definitions, the CreditCard class, operator overloading and special methods, inheritance, numeric progressions, abstract base classes |
| 5. Array-Based Sequences | [5_arraybased_sequences](5_arraybased_sequences/) | Compact and reference arrays, a dynamic array built from scratch, insert and delete, insertion sort, 2D arrays |
| 10. Maps, Hash Tables, and Skip Lists | [10_maps_hashTables_list](10_maps_hashTables_list/) | Maps vs. dictionaries, hash functions and collisions, separate chaining and linear probing, load factor and resizing, sets, multisets, and multimaps |

## LeetCode

Now that I've covered the basics in the book, I've started solving LeetCode problems. Each pattern has its own folder, and every solution has comments explaining each step. Some files also have more than one solution so I can compare approaches.

### Two Pointers

[leetcode/twoPointers](leetcode/twoPointers/)

| # | Problem | Difficulty | Solution |
|---|---|---|---|
| 26 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | [26_removeDuplicates.py](leetcode/twoPointers/26_removeDuplicates.py) |
| 27 | [Remove Element](https://leetcode.com/problems/remove-element/) | Easy | [27_remove_element.py](leetcode/twoPointers/27_remove_element.py) |
| 80 | [Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) | Medium | [80_removeDuplicatesII.py](leetcode/twoPointers/80_removeDuplicatesII.py) |
| 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | [283_moveZeros.py](leetcode/twoPointers/283_moveZeros.py) |

### Hash Map

[leetcode/hashMap](leetcode/hashMap/)

| # | Problem | Difficulty | Solution |
|---|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | [1_twoSum.py](leetcode/hashMap/1_twoSum.py) |

### Dynamic Programming

[leetcode/dynamicProgramming](leetcode/dynamicProgramming/)

| # | Problem | Difficulty | Solution |
|---|---|---|---|
| 3693 | [Climbing Stairs II](https://leetcode.com/problems/climbing-stairs-ii/) | Medium | [3693_climbingStairsII.py](leetcode/dynamicProgramming/3693_climbingStairsII.py) |

## Running the code

You need Python 3. The scripts only use the standard library, so there's nothing to install. Run any file directly:

```bash
python3 5_arraybased_sequences/array_examples.py
```

Some LeetCode solutions include their own test cases and print PASS or FAIL for each one:

```bash
python3 leetcode/twoPointers/27_remove_element.py
```
