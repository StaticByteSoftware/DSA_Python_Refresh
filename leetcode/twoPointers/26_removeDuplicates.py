class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        k = 1   # number of unique elements
        # the first element nums[0] is unique, thus start at 1
    
        # loop through length of array starting at index 1, num[0] alreay unique
        for j in range(1, len(nums)):
            # Is the number im looking at different from he last unique number?
            if nums[j] != nums[k-1]:   #nums[j] current num, nums[k-1] last unique value written
                #nums[k-1] k is the empty slot, k-1 is the slot just before it
                nums[k] = nums[j] #copy the unique number into next open slot
                k += 1 # k= k+1 we kept one unique number, move k right 
        return k # return k, k is the number of unique elements