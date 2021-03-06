from tokenizer import Token
from tokenizer import Type


class Syntax:

    # Declaration of the grammar for the Parser

    # E -> *CREATE + EXPRESSIONS + *RUPTURE
    E = [[Token(type=Type.CREATE), Token(
        type=Type.EXPRESSIONS), Token(type=Type.RUPTURE)]]

    # EXPRESSIONS -> EXPRESSION | EXPRESSION + EXPRESSIONS | EXPRESSIONS + EXPRESSIONS
    EXPRESSIONS = [
        [Token(type=Type.EXPRESSION)],
        [Token(type=Type.EXPRESSION), Token(type=Type.EXPRESSIONS)],
        [Token(type=Type.EXPRESSIONS), Token(type=Type.EXPRESSIONS)]

    ]

    # EXPRESSION -> PRINT | ACCEPT | DECLARATION | ASSIGNMENT | RETURN_TYPE
    EXPRESSION = [
        [Token(type=Type.PRINT)],
        [Token(type=Type.ACCEPT)],
        [Token(type=Type.DECLARATION_INT)],
        [Token(type=Type.DECLARATION_STR)],
        [Token(type=Type.ASSIGNMENT)],
        [Token(type=Type.DECLARATION_ASSIGNMENT)],

        # [Token(type=Type.RETURN_TYPE)]
    ]

    # RETURN_TYPE -> ARITH_OP | AVERAGE | DISTANCE
    RETURN_TYPE = [
        [Token(type=Type.ARITH_OP)],
        [Token(type=Type.AVERAGE)],
        [Token(type=Type.DISTANCE)]
    ]

    # VAL -> INT | STR
    VAL = [
        [Token(type=Type.INT)],
        [Token(type=Type.STR)]
    ]

    # NUMBER -> RETURN_TYPE | VAL
    NUMBER = [
        [Token(type=Type.RETURN_TYPE)],
        [Token(type=Type.INT)],
        # VAR can be considered a number
        # [Token(type=Type.VAR)]
    ]

    # NUMBERS -> NUMBER | NUMBER + NUMBERS
    NUMBERS = [
        [Token(type=Type.NUMBER)],
        [Token(type=Type.NUMBER), Token(type=Type.NUMBERS)]
    ]

    # DECLARATION -> DTYPE + VAR | DTYPE + VAR + WITH + NUMBER
    DECLARATION_INT = [
        [Token(type=Type.DTYPE_INT), Token(type=Type.VAR)],
    ]

    DECLARATION_STR = [
        [Token(type=Type.DTYPE_STR), Token(type=Type.VAR)],
    ]

    DECLARATION_ASSIGNMENT = [
        [Token(type=Type.DECLARATION_STR), Token(type=Type.WITH), Token(
            type=Type.STR)],
        [Token(type=Type.DECLARATION_INT), Token(type=Type.WITH), Token(
            type=Type.NUMBER)],
    ]

    # ACCEPT -> INPUT + VAR
    ACCEPT = [
        [Token(type=Type.INPUT), Token(type=Type.VAR)],
    ]

    # PRINT -> OUTPUT + NUMBER | OUTPUT + VAR | OUTPUT + STR
    PRINT = [
        [Token(type=Type.OUTPUT), Token(type=Type.NUMBER)],
        [Token(type=Type.OUTPUT), Token(type=Type.VAR)],
        [Token(type=Type.OUTPUT), Token(type=Type.STR)],
    ]

    # ASSIGNMENT -> STORE + NUMBER + IN + VAR
    ASSIGNMENT = [
        [Token(type=Type.STORE), Token(type=Type.NUMBER),
         Token(type=Type.IN), Token(type=Type.VAR)],
        [Token(type=Type.STORE), Token(type=Type.STR),
         Token(type=Type.IN), Token(type=Type.VAR)],
    ]

    # ARITH_OP -> ARITHMETIC + NUMBER + NUMBER
    ARITH_OP = [
        [Token(type=Type.ARITHMETIC), Token(
            type=Type.NUMBER), Token(type=Type.NUMBER)],
        [Token(type=Type.ARITHMETIC), Token(
            type=Type.VAR), Token(type=Type.NUMBER)],
        [Token(type=Type.ARITHMETIC), Token(
            type=Type.NUMBER), Token(type=Type.VAR)],
        [Token(type=Type.ARITHMETIC), Token(
            type=Type.VAR), Token(type=Type.VAR)],
    ]

    # AVERAGE -> MEAN + NUMBERS
    AVERAGE = [
        [Token(type=Type.MEAN), Token(type=Type.NUMBERS)]
    ]

    # DISTANCE -> DIST + NUMBER + NUMBER AND NUMBER + NUMBER
    DISTANCE = [
        [Token(type=Type.DIST), Token(type=Type.NUMBER),
         Token(type=Type.NUMBER), Token(type=Type.AND),
         Token(type=Type.NUMBER), Token(type=Type.NUMBER)]
    ]

    def get_syntax(self):
        syntax = {
            'RETURN_TYPE': (Type.RETURN_TYPE, Syntax.RETURN_TYPE),
            # 'VAL': (Type.VAL, Syntax.VAL),
            'NUMBER': (Type.NUMBER, Syntax.NUMBER),
            'DECLARATION_INT': (Type.DECLARATION_INT, Syntax.DECLARATION_INT),
            'DECLARATION_STR': (Type.DECLARATION_STR, Syntax.DECLARATION_STR),
            'DECLARATION_ASSIGNMENT': (Type.DECLARATION_ASSIGNMENT, Syntax.DECLARATION_ASSIGNMENT),
            'DISTANCE': (Type.DISTANCE, Syntax.DISTANCE),
            'ACCEPT': (Type.ACCEPT, Syntax.ACCEPT),
            'PRINT': (Type.PRINT, Syntax.PRINT),
            'ASSIGNMENT': (Type.ASSIGNMENT, Syntax.ASSIGNMENT),
            'ARITH_OP': (Type.ARITH_OP, Syntax.ARITH_OP),
            'AVERAGE': (Type.AVERAGE, Syntax.AVERAGE),
        }
        return syntax

    def get_final_syntax(self):
        syntax = {
            # 'E': (Type.E, Syntax.E),
            # 'EXPRESSIONS': (Type.EXPRESSIONS, Syntax.EXPRESSIONS),
            'EXPRESSION': (Type.EXPRESSION, Syntax.EXPRESSION),
        }
        return syntax

    def get_ipol_syntax(self):
        syntax = {
            'E': (Type.E, Syntax.E),
            'EXPRESSIONS': (Type.EXPRESSIONS, Syntax.EXPRESSIONS),
        }
        return syntax

    def get_cfg(self):

        return """
**************************************************
E -> CREATE + EXPRESSIONS + RUPTURE
EXPRESSIONS -> EXPRESSION | EXPRESSION + EXPRESSIONS | EXPRESSIONS + EXPRESSIONS
EXPRESSION -> PRINT | ACCEPT | DECLARATION | ASSIGNMENT | RETURN_TYPE
RETURN_TYPE -> ARITH_OP | AVERAGE | DISTANCE
VAL -> INT | STR
NUMBER -> RETURN_TYPE | VAL
NUMBERS -> NUMBER | NUMBER + NUMBERS
DECLARATION -> DTYPE + VAR | DTYPE + VAR + WITH + NUMBER
ACCEPT -> INPUT + VAR
PRINT -> OUTPUT + NUMBER | OUTPUT + VAR | OUTPUT + STR
ASSIGNMENT -> STORE + NUMBER + IN + VAR
ARITH_OP -> ARITHMETIC + NUMBER + NUMBER
AVERAGE -> MEAN + NUMBERS
DISTANCE -> DIST + NUMBER + NUMBER AND NUMBER + NUMBER
*********************************************************************
"""