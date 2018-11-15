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
            if line[0].type == Type.DTYPE_INT or line[0].type == Type.DECLARATION_STR:
                # this is a variable declaration
                data_type = line[0].type
                var_name = line[1].val

                no_error = False

                try:
                    variables[var_name]
                    print('Error on line ' + str(line_number) +
                          '. Variable `' + var_name + '` has already been declared')
                except Exception:
                    no_error = True
                    variables[var_name] = data_type

                variables[var_name] = data_type

                # check if this is an assignment
                if len(line) > 2 and no_error:
                    converted_line = var_name + ' = ' + \
                        self.generate_simple_expression(line[2:])
                elif len(line) == 2:
                    pass
                else:
                    return False

            elif line[0].type == Type.STORE:
                # STORE data in VAR
                # either Type.STR or Type.INT
                data = line[1]
                var_name = line[len(line) - 1].val
                print(var_name)
                print(variables[var_name])

                try:
                    data_type = variables[var_name]
                    if data_type == Type.DTYPE_INT and data.type == Type.STR:
                        exception = IpolException(
                            ExceptionType.INCOMPATIBLE_DATA_TYPE_INT, line, line_number)
                        exception.print()
                    elif data_type == Type.DECLARATION_STR and not data.type == Type.STR:
                        exception = IpolException(
                            ExceptionType.INCOMPATIBLE_DATA_TYPE_INT, line, line_number)
                        exception.print()
                    else:
                        converted_line = var_name + ' = ' + self.generate_simple_expression(line[1:len(line) - 2])
                except:
                    # variable was not declared
                    exception = IpolException(
                        ExceptionType.VARIABLE_NOT_DECLARED, line, line_number)
                    exception.print()

            else:
                converted_line = self.generate_simple_expression(line)

            generated_code.append(converted_line)
        return generated_code

    def generate_simple_expression(self, line):
        # used for generating arithmetic operations involving two integers
        placeholders = ['&n0', '&n1']

        # this counter is used to move between &n0 and &n1
        index = 0

        # start with a single point
        converted_line = '&n0'

        for token in line:
            if token.type == Type.ARITHMETIC:
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
            elif token.type == Type.OUTPUT:
                converted_line = converted_line.replace(
                    '&n0', 'print(&n0, end=" ")')
                index = 0
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
"""
