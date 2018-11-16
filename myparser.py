from syntax import Syntax
from pprint import pprint
from tokenizer import Token
from tokenizer import Type


class Parser:

    def __init__(self, syntax):
        self.syntax = syntax

    def parse(self, line):
        parsed = []
        buffer = []

        if len(line) > 0:

            for index, token in enumerate(line):
                if token.type == Type.MEAN:
                    is_mean_op = True
                    for token in line[index + 1:]:
                        if not token.type == Type.NUMBER and not token.type == Type.VAR:
                            is_mean_op = False
                    if is_mean_op:
                        p = Token(type=Type.AVERAGE)
                        p.val = buffer.copy()
                        parsed.clear()
                        parsed.append(p)
                        buffer.clear()
                        return parsed

        for token in line:
            # push the token to the buffer
            buffer.append(token)

            # find syntactical matches
            matches = self.find_matches(buffer)

            while len(matches) == 0:
                # no matches probably due to an extra token
                # for example, ARITH VAL VAL is legal but VAL must be converted to number first
                # simply move the token to the parsed list
                if len(buffer) > 0:
                    parsed.append(buffer.pop(0))
                    matches = self.find_matches(buffer)
                else:
                    break

            for m in matches:
                for x in matches[m][1]:
                    # complete match
                    if len(x) == len(buffer):
                        # todo convert the token
                        t = Token(type=matches[m][0])
                        t.val = buffer.copy()

                        # then pop it
                        parsed.append(t)
                        buffer.clear()

        return parsed

    def find_matches(self, buffer):
        size = len(buffer)

        matches = {}

        # check syntaxes that start with the given token
        for s in self.syntax:
            val = self.syntax[s][1]

            for v in val:
                match_count = 0

                if len(v) >= size:
                    for i in range(size):
                        if buffer[i].type == v[i].type:
                            match_count = match_count + 1
                    if match_count == size:
                        matches[s] = self.syntax[s]

        return matches
