# Leetcode: 283
# Time:  O(n) - one pass over nums, constant work per element.
# Space: O(1) - only two integer variables; nums is changed in place.

# LeetCode puts every solution inside a class called Solution.
# That's the only reason the class exists.
class Solution:
    # Defines the method. self is required because it's a method in a class.
    # nums: list[int] is a type hint. -> None says the method returns nothing.
    # LeetCode checks nums itself after the call, so there's nothing to return.
    def moveZeroes(self, nums: list[int]) -> None:
        # write = 0 is where the next non-zero element will go.
        # Everything to the left of write is non-zero and in original order.
        write = 0
        # range(len(nums)) gives the indexes 0, 1, ..., n-1.
        # read visits every index once, left to right.
        for read in range(len(nums)):
            # Is this element one we keep up front? If it's 0, the body is skipped,
            # write stays where it is, and the loop moves on.
            if nums[read] != 0:
                # Swaps the non-zero element into the next open slot, and the
                # value that was there (always a 0) back to read's position.
                # Python builds the right side (nums[read], nums[write]) first,
                # then assigns it, so no temp variable is needed.
                # When no zeros have been seen yet, write == read and this
                # swaps the element with itself, which does no harm.
                nums[write], nums[read] = nums[read], nums[write]
                # Moves write to the next open slot.
                write += 1
        # No return. By now every non-zero is in nums[:write], in order,
        # and every slot from write to the end holds a 0.


if __name__ == "__main__":
    # (nums, expected nums after the call)
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),       # LeetCode example 1
        ([0], [0]),                                 # LeetCode example 2
        ([], []),                                   # empty list
        ([1, 2, 3], [1, 2, 3]),                     # no zeros
        ([0, 0, 0], [0, 0, 0]),                     # every element is 0
        ([4, 0, 5, 0, 0, 6], [4, 5, 6, 0, 0, 0]),   # zeros scattered
    ]

    solution = Solution()
    for nums, expected in test_cases:
        original = nums[:]            # copy, because the call changes nums in place
        solution.moveZeroes(nums)
        status = "PASS" if nums == expected else "FAIL"
        print(f"{status}  {original} -> {nums} (expected {expected})")
