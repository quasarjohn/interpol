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

    # for line in tokens_list:
    #     for token in line:
    #         print(token.type)
    # print('$$$$$$$$$$')

    parser = Parser(syntax=Syntax().get_syntax())

    for line in tokens_list:
        recursive_parse(parser, line, callback)

    for p in parsed_list:
        for t in p:
            print(t.type)
        print('**********')


def recursive_parse(parser, line, callback):
    parsed = parser.parse(line)

    if not equal_ignore_order(parsed, line):
        recursive_parse(parser, parsed, callback)
        if len(parsed) == 0:
            callback(line)  

    else:
        parser = Parser(syntax=Syntax().get_syntax())
        parsed = parser.parse(parsed)
        callback(parsed)
        


def callback(parsed):
    parsed_list.append(parsed)


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
