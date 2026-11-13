"""
write a function that can identify if a year is a leep year
The year can be evenly divided by 4, is a leap year, unless:
The year can be evenly divided by 100, it is NOT a leap year, unless:
The year is also evenly divisible by 400. Then it is a leap year.

"""

# My Solution 
def is_leap(year):
    leap = False

    if year % 4 == 0 and year % 100 != 0:
        leap = True
    elif year % 100 == 0 and year % 400 == 0:
        leap = True
    else:
        leap = False

    return leap

# Solution 2 
def is_leap_optimized(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

year = int(input())
print(is_leap(year))
