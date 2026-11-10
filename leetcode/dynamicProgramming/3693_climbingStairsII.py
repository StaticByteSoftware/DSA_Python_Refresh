# LeetCode 3693 - Climbing Stairs II
# Steps are numbered 0 to n. From step i you can jump to i+1, i+2, or i+3.
# Landing on step j costs: costs[j] + (j - i)^2  ->  jump 1 = +1, jump 2 = +4, jump 3 = +9
# Start on step 0 with cost 0. Return the minimum total cost to reach step n.
#
# dp[i] = cheapest total cost to get from step i to step n, counting the cost of standing on step i
# Time: O(n), the loop runs n times and each pass does a fixed amount of work
# Space: O(n), for the dp list and the new costs list

class Solution:
    def climbStairs(self, n: int, costs: List[int]) -> int:
        # LeetCode's costs[1] is step 1's cost, but Python lists start at index 0
        # after this, costs[i] is the cost of step i, and step 0 (the start) costs 0
        costs = [0] + costs # put 0 at front of list, cost is 1-indexed

        # all slots start at infinity. real steps are 0 to n, the 2 extra slots catch jumps past the top
        # from step n-1, a 3-step jump reads dp[n+2], so that slot has to exist
        # infinity = "impossible move", min() will never pick it
        dp = [inf] * (n + 3)    # makes a list of n+3 slots

        # base case: at the top there's nowhere left to jump, so the cost is just step n's cost
        dp[n] = costs[n]

        # range(n) is 0, 1, ..., n-1 and reversed flips it to n-1, n-2, ..., 0
        # work down from the top: dp[i] needs dp[i+1], dp[i+2], dp[i+3] computed first
        for i in reversed(range(n)):
            # cost of standing on step i + the cheapest of the 3 choices:
            #   jump 1: pay 1, then dp[i+1] for the rest
            #   jump 2: pay 4, then dp[i+2] for the rest
            #   jump 3: pay 9, then dp[i+3] for the rest
            dp[i] = costs[i] + min(dp[i + 1] + 1, dp[i + 2] + 4, dp[i + 3] + 9)

        # cheapest total cost starting from step 0
        return dp[0]

# Trace: n = 4, costs = [1, 2, 3, 4]  ->  after costs = [0] + costs: costs = [0, 1, 2, 3, 4], dp[5] = dp[6] = inf
#   i=4: base case                                   dp[4] = 4
#   i=3: 3 + min(4+1=5,   inf,      inf)        = 8   dp[3] = 8
#   i=2: 2 + min(8+1=9,   4+4=8,    inf)        = 10  dp[2] = 10
#   i=1: 1 + min(10+1=11, 8+4=12,   4+9=13)     = 12  dp[1] = 12
#   i=0: 0 + min(12+1=13, 10+4=14,  8+9=17)     = 13  dp[0] = 13  (path 0 -> 1 -> 2 -> 4)
