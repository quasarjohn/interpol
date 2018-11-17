from tokenizer import Type
from ipolexception import IpolException
from ipolexception import ExceptionType


class CodeGenerator:

    # returns a string format and the value of the expression
    def generate(self, tokens_list):

        # append generated code here
        generated_code = []

        # generate helper functions for the generated python code
        generated_code.append(self.get_helper_functions())

        # dictionary containing the variables and their data types
        variables = {}
        # iterate the lines
        for line_number, line in enumerate(tokens_list):

            converted_line = ''
            # check if the line is a declaration of a variable so we can keep
            # track of all the varaibles used in the generated code
            if line[0].type == Type.DTYPE_INT or line[0].type == Type.DTYPE_STR:
                # this is a variable declaration
                data_type = line[0].type
                var_name = line[1].val

                no_error = False

                try:
                    # check if the variable has been declared
                    variables[var_name]
                    print('Error on line ' + str(line_number) +
                          '. Variable `' + var_name + '` has already been declared')
                except Exception:
                    # if not, add it to the variables dictionary
                    no_error = True
                    variables[var_name] = data_type

                # check if this is an assignment
                if len(line) > 2 and no_error:
                    converted_line = var_name + ' = ' + \
                        self.generate_simple_expression(line[2:], variables)
                elif len(line) == 2:
                    # if no value is declared, give a default of 0
                    if line[0].type == Type.DTYPE_INT:
                        converted_line = var_name + ' = 0'
                    else:
                        converted_line = var_name + ' = ""'
                else:
                    return False

            elif line[0].type == Type.STORE:
                # STORE data in VAR
                # either Type.STR or Type.INT
                data = line[1]
                var_name = line[len(line) - 1].val

                try:
                    data_type = variables[var_name]
                    # check if the data type is int by the value is str
                    if data_type == Type.DTYPE_INT and data.type == Type.STR:
                        exception = IpolException(
                            ExceptionType.INCOMPATIBLE_DATA_TYPE_INT, line, line_number + 1)
                        exception.print()
                    elif data_type == Type.DECLARATION_STR and not data.type == Type.STR:
                        exception = IpolException(
                            ExceptionType.INCOMPATIBLE_DATA_TYPE_INT, line, line_number + 1)
                        exception.print()
                    else:
                        converted_line = var_name + ' = ' + \
                            self.generate_simple_expression(
                                line[1:len(line) - 2], variables)
                except:
                    # variable was not declared
                    exception = IpolException(
                        ExceptionType.VARIABLE_NOT_DECLARED, line, line_number + 1)
                    exception.print()
                    return False
            elif line[0].type == Type.INPUT:
                var_name = line[1].val

                data_type = variables[var_name]
                is_int = False

                # check if the user is entering a valid value
                # if the data type of the variable is int, cast the number to int
                if data_type == Type.DTYPE_INT:
                    is_int = True

                converted_line = var_name + \
                    ' = request_input({}, {})'.format(
                        "\'" + var_name + "\'", is_int)

            else:
                # else it is either just PRINT or ARITHMETIC operation
                converted_line = self.generate_simple_expression(
                    line, variables)
                if not converted_line:
                    return False

            generated_code.append(converted_line)
        return generated_code

    def generate_simple_expression(self, line, variables):
        # used for generating arithmetic operations involving two integers
        placeholders = ['&n0', '&n1']

        # this counter is used to move between &n0 and &n1
        index = 0

        # start with a single point
        converted_line = '&n0'

        for line_number, token in enumerate(line):
            if token.type == Type.MEAN:
                converted_line = converted_line.replace(
                        placeholders[index], self.generate_mean_operation(line[line_number:], variables))
                index = 0
                break
            elif token.type == Type.ARITHMETIC:
                if token.val == 'ROOT':
                    converted_line = converted_line.replace(
                        placeholders[index], 'root(&n0, &n1)')
                    index = 0
                else:
                    operator = self.get_operation(token)
                    converted_line = converted_line.replace(
                        placeholders[index], '(&n0 ' + operator + ' &n1)')
                    index = 0
            elif token.type == Type.INT:
                converted_line = converted_line.replace(
                    placeholders[index], token.val)
                index = index + 1
            elif token.type == Type.STR:
                formatted_str = "'" + token.val[1:len(token.val) - 1] + "'"
                formatted_str = formatted_str.replace('&nbsp', ' ')
                converted_line = converted_line.replace(
                    placeholders[index], formatted_str)
                index = index + 1
            elif token.type == Type.VAR:
                try:
                    converted_line = converted_line.replace(
                        placeholders[index], token.val)
                    index = index + 1
                except:
                    exception = IpolException(
                        ExceptionType.VARIABLE_NOT_DECLARED, line, line_number)
                    exception.print()
                    return False
            elif token.type == Type.OUTPUT:
                print_type = 'print(&n0, end=" ")' if token.val == 'GIVEYOU!' else 'print(&n0)'
                converted_line = converted_line.replace(
                    '&n0', print_type)
                index = 0
        return converted_line

    def generate_mean_operation(self, line, variables):
        # used for generating arithmetic operations involving two integers
        placeholders = ['&n0', '&n1']

        # this counter is used to move between &n0 and &n1
        index = 0

        # start with a single point
        converted_line = '&n0'
        is_arith = False
        for line_number, token in enumerate(line):
           
            if token.type == Type.MEAN:
                if not is_arith:
                    converted_line = converted_line.replace(
                    placeholders[index], 'mean(&n0, &n1)')
                    is_arith = True
                else:
                    converted_line = converted_line.replace(
                    placeholders[index], 'mean(&n0)')
                    is_arith = False
                index = 0
            elif token.type == Type.ARITHMETIC:
                if token.val == 'ROOT':
                    converted_line = converted_line.replace(
                        placeholders[index], 'root(&n0, &n1)')
                    index = 0
                    is_arith = True
                else:
                    operator = self.get_operation(token)
                    converted_line = converted_line.replace(
                        placeholders[index], '(&n0 ' + operator + ' &n1)')
                    index = 0
                    is_arith = True
            elif token.type == Type.INT:
                if not is_arith:
                    converted_line = converted_line.replace(
                    placeholders[index], str(token.val) + ', &n0')
                    index = 0
                elif is_arith and index == 1:
                    converted_line = converted_line.replace(
                    placeholders[index], str(token.val))
                    is_arith = False
                    index = 0
                else:
                    converted_line = converted_line.replace(
                    placeholders[index], str(token.val))
                    index = index + 1
            elif token.type == Type.STR:
                formatted_str = "'" + token.val[1:len(token.val) - 1] + "'"
                formatted_str = formatted_str.replace('&nbsp', ' ')
                converted_line = converted_line.replace(
                    placeholders[index], formatted_str)
                index = index + 1
            elif token.type == Type.VAR:
                try:
                    converted_line = converted_line.replace(
                        placeholders[index], token.val)
                    index = index + 1
                except:
                    exception = IpolException(
                        ExceptionType.VARIABLE_NOT_DECLARED, line, line_number)
                    exception.print()
                    return False
            elif token.type == Type.OUTPUT:
                print_type = 'print(&n0, end=" ")' if token.val == 'GIVEYOU!' else 'print(&n0)'
                converted_line = converted_line.replace(
                    '&n0', print_type)
                index = 0
            
            if not is_arith:
                converted_line = converted_line.replace('&n2', '&n0')
                if '&n0' not in converted_line:
                    converted_line = converted_line[:len(converted_line) - 1] + ', &n0' + converted_line[len(converted_line) - 1:]
        
        converted_line = converted_line.replace('&n0', '')
        return converted_line

    def get_operation(self, token):
        if token.val == 'PLUS':
            return '+'
        elif token.val == 'MINUS':
            return '-'
        elif token.val == 'TIMES':
            return '*'
        elif token.val == 'DIVBY':
            return '/'
        elif token.val == 'MODU':
            return '%'
        elif token.val == 'RAISE':
            return '**'

    def get_helper_functions(self):
        return """
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
    val = input('Enter value for ' + var_name  + message + '\\n')

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
"""
