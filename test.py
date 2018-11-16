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

print(mean((3 + (1 + (6 + 5))), 1, 1, 2, 2, 2, 45, 5, 5, 5, (1 + 1), ))