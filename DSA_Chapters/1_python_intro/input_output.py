#input 
year = int(input('In what year were you born? '))
#output
print('I was born in: ',year)


# split up input:
reply = input('Enter x and y, seperated by spaces: ')
pieces = reply.split()  #returns a list of strings, as seperated by spaces
x = float(pieces[0])
y = float(pieces[1])
print(pieces)

# Target fat burning heart rate by age
age = int(input('Enter your age in years: '))
max_heart_rate = 206.9 - (0.67 * age)   
target = 0.65 * max_heart_rate
print('Your target fat-burning heart rate is', target)