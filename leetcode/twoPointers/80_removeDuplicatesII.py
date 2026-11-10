class Solution1:
    def removeDuplicates(self, nums: list[int]) -> int:
        count = {}      # empty Dictionary, map each number to how many items weve seen before
        k = 0       # the number of unique elements that appear twice

        # loop over the values in the list, not indexes. num is the actual numbers
        for num in nums: 
            # add one to the numbers tally 
            count[num] = count.get(num,0) + 1
            # count.get(num,0) reurns currenbt count for num or 0 if num isnt in the dictionary yet 
            # +1 coutns this occurance 
            # count[num] stores the new total 

            # have you seen this number at most twice
                # thrid or later ocurance fails and is skipped
            if count[num] <= 2:
                # write the number into the next open slot 
                nums[k] = num
                k += 1 # increase count by 1    
        return k # return how many numbers you kept 

class Solution2:
    def removeDuplicates(self, nums: list[int]) -> int:
        k = 0   # pointer, running count of unique numbers that appear more than twice

        # loops over each value in the list
        for num in nums:
            #if k < 2: less than 2 numbers. num != nums[k-2], the number two slots back in the kept section is differe from num
            if k < 2 or num != nums[k-2]:
                nums[k] = num   # write the kept number itno the open slot 
                k += 1      # move the write poitner forware one slot, increase unique element count
            return k # reutrn unique element count

class Solution3: 
    def removeDuplicates(self, nums: list[int]) -> int:
        k = 0
        for j in range(len(nums)):
            if k < 2 or nums[j] != nums[k-2]:
                nums[k] = nums[j]
                k += 1
        return k