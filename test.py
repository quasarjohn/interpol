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

def request_input(var_name, type):
    # if type is 0, request int, else request str
    val = input('Enter value for ' + var_name + '\n')


    return val


X = request_input('X', 0)
