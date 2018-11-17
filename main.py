import sys
import re
from enum import Enum
from filereader import FileReader
from tokenizer import Tokenizer
from tokenizer import Token
from tokenizer import Type
from myparser import Parser
from pprint import pprint
from syntax import Syntax
from ipolexception import ExceptionCheker
from ipolexception import IpolException
from codegenerator import CodeGenerator
from ipolexception import ExceptionType

parsed_list = []
final_parsed_list = []
ipol_code_verified = []
exceptions = []


def main():
    print('Welcome to IPOL interpreter!')

    # returns lines of string containing the cleaned code
    file_reader = FileReader()
    # tabs removed, double spaces removed
    lines = file_reader.read_file()

    tokenizer = Tokenizer()
    # returns a 2d list containing the tokens per line of code
    tokens_list = tokenizer.tokenize(lines)
    tokens_list_copy = tokens_list.copy()

    # create instance of the parser with the syntax declared in Syntax class
    parser = Parser(syntax=Syntax().get_syntax())

    # iterate each line of the list containing the tokens
    for line in tokens_list:
        recursive_parse(parser, line, callback)


    # create a new instance of the parser now with the syntax for recuding operations to expressions
    parser = Parser(syntax=Syntax().get_final_syntax())

    # Parse to an expression to see if it is valid
    for line in parsed_list:
        recursive_parse(parser, line, callback1)  
        


    exception_checker = ExceptionCheker()

    for i in range(len(final_parsed_list)):
        # there must be a syntax error because it cannot be converted to a single statement
        # check which kind of exception it is
        if len(final_parsed_list[i]) > 1:
            exception = exception_checker.check_exception(
                final_parsed_list[i], i)

            if isinstance(exception, IpolException):
                exceptions.append(exception)

    # now check if the overall structure of the code is valid
    # check if there are unused values
    # for index, token in enumerate(reduce(final_parsed_list)):
    #     if token.type == Type.NUMBER or token.type == Type.STR:
    #         exceptions.append(IpolException(
    #             ExceptionType.UNUSED_VALUE_ERROR, None, index))

    # print exceptions if there are any and halt the build process
    if len(exceptions) > 0:
        for exception in exceptions:
            exception.print()
        return
    else:
        # create a new instance of the parser now with the syntax of the overall ipol code
        parser = Parser(syntax=Syntax().get_ipol_syntax())

        # finally, verify that the full code is valid
        reduced_final_parsed_list = reduce(final_parsed_list)
        # recursive_parse(parser, reduced_final_parsed_list, callback2)
        reduced_final_parsed_list[:] = (token for token in reduced_final_parsed_list \
        if token.type != Type.EMPTY_LINE)
        for token in reduced_final_parsed_list:
            print(token.type)
        # check syntax in class Syntax
        # Type.E means accepted
        # try:
        #     if ipol_code_verified[0][0].type == Type.E:
        #         print('Build Successful\n')
        #     else:
        #         print('Build Failed. wow')
        #         return
        # except:
        #     print('Build Failed. wow')
        #     return

        # there are no exceptions
        # continue with code generation
        tokens_list_copy.pop(0)
        tokens_list_copy.pop(len(tokens_list_copy) - 1)

        generated_code = CodeGenerator().generate(tokens_list_copy)

        # this may return a bool data type
        if isinstance(generated_code, list):
            runnable_code = '\n'.join(generated_code)

            # run the generated python code
            with open('ic.py', '+w') as ic:
                ic.write(runnable_code)

            print('\nBuild Complete.\nView logs on ipol_logs.txt\nView generated code on ic.py\n\n')
            exec(runnable_code, globals())

            with open('ipol_logs.txt', '+w') as logs:
                text_to_write = 'PARSING LOGS\n\nGENERATED TOKENS\n'
                for line in tokens_list:
                    for token in line:
                        text_to_write = text_to_write + '{} -> {}'.format(token.type, token.val) + ", "
                    text_to_write = text_to_write + '\n'

                text_to_write = text_to_write + '\PARSED AS...\n'
                for line in parsed_list:
                    for token in line:
                        text_to_write = text_to_write + str(token.type) + ', '
                    text_to_write = text_to_write + '\n'

                text_to_write = text_to_write + '\nGENERATED INTERMEDIATE CODE\n' + runnable_code
                logs.write(text_to_write)
        # if bool is returned, that means there was something wrong with the ipol code
        else:
            print('Build failed')

def recursive_parse(parser, line, callback):
    parsed = parser.parse(line)
    
    

    # parse the line
    if not equal_ignore_order(parsed, line):
        recursive_parse(parser, parsed, callback)
        # if the line can no longer be parsed, the result will return an empty list
        # thus, just return the previous unparsed list
        if len(parsed) == 0:
            callback(line)
    # the parsing returned the same result ie. NUMBER can be parsed as NUMBER and so on
    # just return the parsed list and end the loop
    else:
        # parser = Parser(syntax=Syntax().get_syntax())
        # parsed = parser.parse(parsed)
        callback(line)

# callback function for getting the parsed list
def callback(parsed):
    parsed_list.append(parsed)

def callback1(parsed):
    final_parsed_list.append(parsed)

def callback2(parsed):
    ipol_code_verified.append(parsed)

# checks if the returned parsed list is equal to the input list
# which means the list can no longer be parsed
def equal_ignore_order(a, b):
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched

# checks wether the series of code are valid ipol code
# E ->  CRETE, EXPRESSIONS, RUPTURE
def reduce(parsed_list):
    # reduce the lines to a single line so we can perform derivation on the tokens
    """
    from
    CREATE
    EXPRESSION
    EXPRESSION...
    RUPTURE 

    to 
    CREATE EXPRESSION EXPRESSION RUPTURE
    """

    single_line_parsed_list = []

    for line in parsed_list:
        for token in line:
            single_line_parsed_list.append(token)

    return single_line_parsed_list


if __name__ == "__main__":
    main()
