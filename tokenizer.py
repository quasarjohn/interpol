import sys
import re
from enum import Enum


class Tokenizer:

    def tokenize(self, lines):
        tokens_list = []

        for line in lines:
            tokens = []
            # use space as delimiter
            for word in line.split(' '):
                token = Token(word)
                tokens.append(token)
            tokens_list.append(tokens)

        return tokens_list


class Token:

    def __init__(self, val=None, type=''):
        self. val = val

        # identify its type
        if type == '':
            self.type = self.identify_token(val)
        else:
            self.type = type

    def is_float(self, input):
        try:
            num = float(input)
        except ValueError:
            return False
        return True

    def is_int(self, input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True

    def identify_token(self, val):

        if self.is_int(val):
            return Type.INT

        if self.is_float(val):
            return Type.FLOAT

        if len(re.findall('\[(.+?)\]', val)) > 0:
            return Type.STR

        if val == 'DSTR':
            return Type.DTYPE_STR
        elif val == 'DINT':
            return Type.DTYPE_INT
        elif val == 'GIVEME?':
            return Type.INPUT
        elif val == 'GIVEYOU!' or val == 'GIVEYOU!!':
            return Type.OUTPUT
        elif val == 'WITH':
            return Type.WITH
        elif val == 'IN':
            return Type.IN
        elif val == 'STORE':
            return Type.STORE
        elif val == 'PLUS' or val == 'MINUS' or val == 'TIME' or val == 'DIVBY' or val == 'MODU' or val == 'EXP' or val == 'ROOT' or val == 'RAISE':
            return Type.ARITHMETIC
        elif val == 'MEAN':
            return Type.MEAN
        elif val == 'AND':
            return Type.AND
        elif val == 'DIST':
            return Type.DIST
        elif val == 'CREATE':
            return Type.CREATE
        elif val == 'RUPTURE':
            return Type.RUPTURE
        else:
            return Type.VAR


class Type(Enum):
    # char -> abc...123
    # word -> char | word + char
    VAR = 0

    # GIVEME?
    INPUT = 2
    # GIVEYOU!, GIVEYOU!!
    OUTPUT = 3
    # WITH
    WITH = 4
    # IN
    IN = 5
    # STORE
    STORE = 6
    # PLUS, MINUS, TIMES, DIVBY, MODU, EXP, ROOT
    # basic arithmetic operation accepting two numbers as param
    ARITHMETIC = 7
    # MEAN
    MEAN = 8
    # AND
    AND = 9
    # DIST
    DIST = 10
    # NUMBER
    INT = 11
    # START
    CREATE = 12
    # END
    RUPTURE = 13
    # FLOAT
    FLOAT = 14
    STR = 15

    EXPRESSIONS = 16
    EXPRESSION = 17
    RETURN_TYPE = 18
    ARITH_OP = 19
    AVERAGE = 20
    DISTANCE = 21
    PRINT = 22
    ACCEPT = 23
    ASSIGNMENT = 25
    VAL = 27
    NUMBER = 28
    NUMBERS = 29
    E = 30
    DECLARATION_ASSIGNMENT = 31

    # DSTR, DINT
    DTYPE_INT = 32
    DTYPE_STR = 33
    DTYPE_FLOAT = 34

    DECLARATION_INT = 35
    DECLARATION_STR = 36
    DECLARATION_FLOAT = 37
