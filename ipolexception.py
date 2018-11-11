from enum import Enum
from tokenizer import Type
from tokenizer import Token

class IpolException:

    def __init__(self, type, tokens, line_number):
        self.type = type
        self.tokens = tokens
        self.line_number = line_number
        self.message = self.identify_message()

    def identify_message(self):
        if self.type == ExceptionType.UNSUPPORTED_ARITHMETIC_OPERATION:
            return 'Arithmetic operations on DSTR datatype is not allowed.'
        elif self.type == ExceptionType.UNSUPPORTED_DATA_TYPE:
            return 'Float data type is not supported.'
        elif self.type == ExceptionType.ILLEGAL_ARGUMENT:
            return 'Illegal argument on mean function. Only integers are allowed'
        elif self.type == ExceptionType.NOT_A_STATEMENT:
            return 'The statement cannot be parsed.'


class ExceptionType(Enum):

    # caused by STR + INT OPERATION | FLOAT data type
    UNSUPPORTED_ARITHMETIC_OPERATION = 0

    # this version does not support float data types
    UNSUPPORTED_DATA_TYPE = 1

    # passing illegal arguments to build in methods
    # for example, passing a STR to MEAN operation
    ILLEGAL_ARGUMENT = 2

    # if the tokens cannot be parsed to a single statement
    # for example GIVEYOU! 3 3 will be parsed as <PRINT><NUMBER>
    # this cannot be further simplified and will throw an exception
    NOT_A_STATEMENT = 3


class ExceptionCheker:

    def check_exception(self, tokens, line):

        for token in tokens:
            # ipol does not support float data type
            if token.type == Type.FLOAT:
                return IpolException(ExceptionType.UNSUPPORTED_DATA_TYPE, tokens, line)

        # check for possible syntax errors in arithmetic operations
        if tokens[0].type == Type.ARITHMETIC:
            # check for strings. string is not allowed in arithmetic operations
            for token in tokens:
                if token.type == Type.STR:
                    return IpolException(ExceptionType.UNSUPPORTED_ARITHMETIC_OPERATION, tokens, line)

        # mean operation is not parsed to a single expression due to multiple parameters
        # check if all its parameters are numbers
        elif tokens[0].type == Type.MEAN:
            for token in tokens[1:]:
                if not token.type == Type.NUMBER:
                    return IpolException(ExceptionType.ILLEGAL_ARGUMENT, tokens, line)

        
        return IpolException(ExceptionType.NOT_A_STATEMENT, tokens, line)


