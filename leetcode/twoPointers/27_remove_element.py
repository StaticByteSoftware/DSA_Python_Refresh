# Leetcode: 27
# Time:  O(n) - one pass over nums, constant work per element.
# Space: O(1) - only two integer variables; nums is changed in place.

# LeetCode puts every solution inside a class called Solution.
# That's the only reason the class exists.
class Solution:
    # Defines the method. self is required because it's a method in a class.
    # nums: list[int] and val: int are type hints, labels that say what goes in.
    # Python doesn't enforce them. -> int says the method returns an integer.
    def removeElement(self, nums: list[int], val: int) -> int:
        # write = 0 is where the next kept element will go.
        # It also counts how many elements have been kept so far.
        write = 0
        # range(len(nums)) gives the indexes 0, 1, ..., n-1.
        # read visits every index once, left to right.
        for read in range(len(nums)):
            # Is this element one we keep? If it equals val, the body is skipped,
            # write stays where it is, and the loop moves on.
            if nums[read] != val:
                # Copies the kept element down into the next open slot.
                # When nothing has been removed yet, write == read and this
                # copies the element onto itself, which does no harm.
                nums[write] = nums[read]
                # Moves write to the next open slot.
                write += 1
        # Returns write. After the loop it equals the number of kept elements, which is k.
        return write


if __name__ == "__main__":
    # (nums, val, expected k)
    test_cases = [
        ([3, 2, 2, 3], 3, 2),                # LeetCode example 1
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5),    # LeetCode example 2
        ([], 1, 0),                          # empty list
        ([5, 5, 5], 5, 0),                   # every element is val
        ([1, 2, 3], 9, 3),                   # val not in nums
    ]

    solution = Solution()
    for nums, val, expected in test_cases:
        k = solution.removeElement(nums, val)  # nums is changed in place
        status = "PASS" if k == expected else "FAIL"
        print(f"{status}  val={val}  k={k} (expected {expected})  first k: {nums[:k]}")
