class Solution1: # Hashmap Solution - 	O(n)
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {} # dic that maps value to index for every number seen
        
        # enumerate gives both index and value each pass
            # i is the index, n is the value
        for i, n in enumerate(nums):
            need = target - n   # the partner would compete the pair (seen)
            if need in seen: # have i already passeed the partner 
                return [seen[need], i] # return the indicis 
            seen[n] = i # no partner yet record in dic 
        return[]

class Solution2: # Sort, Two Pointer - O(n log n)
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        pairs = sorted((n, i) for i, n in enumerate(nums))
        left, right = 0, len(pairs) - 1
        while left < right:
            total = pairs[left][0] + pairs[right][0]
            if total == target:
                return [pairs[left][1], pairs[right][1]]
            elif total < target:
                left += 1
            else: 
                right -= 1