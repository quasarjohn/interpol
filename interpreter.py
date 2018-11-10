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


def main():
    print('Welcome to IPOL interpreter!')

    # returns lines of string containing the cleaned code
    file_reader = FileReader()
    # tabs removed, double spaces removed
    lines = file_reader.read_file()

    tokenizer = Tokenizer()
    # returns a 2d list containing the tokens per line of code
    tokens_list = tokenizer.tokenize(lines)

    parser = Parser(syntax=Syntax().get_syntax())

    for line in tokens_list:
        recursive_parse(parser, line)
    


def recursive_parse(parser, line):
    parsed = parser.parse(line)

    for token in line:
        print(token.type)

    print('*************')

    if not equal_ignore_order(parsed, line):
        recursive_parse(parser, parsed)
    else:
        parser = Parser(syntax = Syntax().get_final_syntax())
        parsed = parser.parse(parsed)

        for token in parsed:
            print(token.type)

        print('END OF LINE\n')



def equal_ignore_order(a, b):
    """ Use only when elements are neither hashable nor sortable! """
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched


if __name__ == "__main__":
    main()
