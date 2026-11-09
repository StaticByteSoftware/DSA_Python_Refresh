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

Now that I've covered the basics in the book, I've started solving LeetCode problems, grouped by pattern. Each solution has comments explaining every step, notes on time and space complexity, and test cases you can run.

| Pattern | # | Problem | Difficulty | Solution |
|---|---|---|---|---|
| Two Pointers | 27 | [Remove Element](https://leetcode.com/problems/remove-element/) | Easy | [27_remove_element.py](leetcode/twoPointers/27_remove_element.py) |

## Running the code

You need Python 3. The scripts only use the standard library, so there's nothing to install. Run any file directly:

```bash
python3 5_arraybased_sequences/array_examples.py
```

LeetCode solutions run their own test cases and print PASS or FAIL for each one:

```bash
python3 leetcode/twoPointers/27_remove_element.py
```
