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

parsed_list = []

def main():
    print('Welcome to IPOL interpreter!')

    # returns lines of string containing the cleaned code
    file_reader = FileReader()
    # tabs removed, double spaces removed
    lines = file_reader.read_file()

    tokenizer = Tokenizer()
    # returns a 2d list containing the tokens per line of code
    tokens_list = tokenizer.tokenize(lines)

    # create instance of the parser with the syntax declared in Syntax class
    parser = Parser(syntax=Syntax().get_syntax())

    # iterate each line of the list containing the tokens
    for line in tokens_list:
        recursive_parse(parser, line, callback)

    # print parsed list for debugging purposes
    for p in parsed_list:
        for t in p:
            print(t.type)
        print('**********')
        


def recursive_parse(parser, line, callback):
    parsed = parser.parse(line)

    # parse the line
    if not equal_ignore_order(parsed, line):
        recursive_parse(parser, parsed, callback)
        # if the line can no longer be parsed, the result will return an empty list
        # thus, just return the previous unparsed list
        if len(parsed) == 0:
            callback(line)  

    # the tokens have been parsed to a single statement ie. PRINT, ARITH_OP, etc
    # convert these to STATEMENT or STATEMENTS for the final parsing
    elif len(parsed) == 1:
        parser = Parser(syntax=Syntax().get_final_syntax())
        parsed = parser.parse(parsed)
        callback(parsed)
    # the parsing returned the same result ie. NUMBER can be parsed as NUMBER and so on
    # just return the parsed list and end the loop
    else:
        parser = Parser(syntax=Syntax().get_syntax())
        parsed = parser.parse(parsed)
        callback(parsed)
        
# callback function for getting the parsed list
def callback(parsed):
    parsed_list.append(parsed)

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
