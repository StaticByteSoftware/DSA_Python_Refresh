if __name__ == '__main__':
    # enter one number
    print("Enter 1 number: ")
    n = int(input())

    # while Loop solution
    i = 0 
    while i < n:
        print(i**2)
        i += 1

    # for loop solution 
    for i in range(0,n):
        print(i**2)
        i += 1
