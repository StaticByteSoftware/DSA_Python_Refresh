# Example of function in python
    # 1.5 Functions
def count(data, target):
    n = 0
    for item in data:
        if item == target:  # found a match
            n+=1
    return n 

# Example multiple Return: test if a value exists in a sequence 
    # 1.5 Return Statement

def contains(data2,target2):
    for item in data2:
        if item == target2:
            return True
    return False

# Example Mutable Prameters 
def scale(data, factor):
    for j in range(len(data)):
        data[j] *= factor
        return data

# Example 1
# Print the number of occurances of target 
target = 3
data = [1,2,3,4,5,3]
print(count(data,target))

# Example 2
# Print if Value Exist in List
myTarget = 2
list = [1,2,3,4,5]
print(contains(list,myTarget))

# Example 3
# Multiply all entires of a dataset by given factor
numbers = [1,2,3,4,5]
print(scale(numbers, 2)) # [2, 4, 6, 8, 10]



