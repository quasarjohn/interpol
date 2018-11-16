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

parsed_list = []
final_parsed_list = []
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

    parser = Parser(syntax=Syntax().get_final_syntax())

    # final stage of parsing. Parse to an expression to see if it is valid
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

    # print exceptions if there are any and halt the build process
    if len(exceptions) > 0:
        for exception in exceptions:
            exception.print()
    else:
        # there are no exceptions
        # continue with code generation
        generated_code = CodeGenerator().generate(tokens_list_copy)

        # this may return a bool data type
        if isinstance(generated_code, list):
            runnable_code = '\n'.join(generated_code)

            exec(runnable_code, globals())
        # if bool is returned, that means there was something wrong with the ipol code
        else:
            print('Build failed')

    # for line in tokens_list:
    #     for token in line:
    #         print(token.type, token.val, end = " $ ")


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

if __name__ == "__main__":
    main()
