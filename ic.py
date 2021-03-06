
# this is the code generated from the Codegenerator class

import math

def root(i, j):
    return j ** (1 / i)

def is_float(input):
    try:
        num = float(input)
    except ValueError:
        return False
    return True

def is_int(input):
    try:
        num = int(input)
    except ValueError:
        return False
    return True

def request_input(var_name, int_dtype):
    message = '. (Must be string)'
    if int_dtype:
        message = '. (Must be integer)'

    # if type is 0, request int, else request str
    val = input('Enter value for ' + var_name  + message + '\n')

    if int_dtype and not is_int(val):
        print('Incorrect input. Please try again.')
        val = request_input(var_name, type)
        return val

    return int(val)

def mean(*numbers):
    sum = 0

    for number in numbers:
        sum = sum + number
    
    return sum / len(numbers)

def distance(x, y, x1, y1):
    return math.sqrt(math.pow(x - x1, 2) + math.pow(y - y1, 2))


X = 1
print(8)
print(88)
print(69)
print(88)
