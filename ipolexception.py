from enum import Enum

class IpolException:

    def __init__(self, type, tokens, line_number): 
        self.type = type
        self.tokens = tokens
        self.line_number = line_number
        self.message = self.identify_message()

    def identify_message(self):
        if self.type == ExceptionType.UNSUPPORTED_ARITHMETIC_OPERATION:
            return 'Operations on DSTR and DINT datatype is not allowed.'
        elif self.type == ExceptionType.UNSUPPORTED_DATA_TYPE:
            return 'Float data type is not supported.'
        elif self.type == ExceptionType.ILLEGAL_ARGUMENT:
            return 'Illegal argument on built in operation.'
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


