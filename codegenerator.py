from tokenizer import Type


class CodeGenerator:

    # returns a string format and the value of the expression
    def generate(self, tokens_list):

        generated_code = []
        placeholders = ['&n0', '&n1']

        for line in tokens_list:
            index = 0
            converted_line = '&n0'
            for token in line:
                if token.type == Type.ARITHMETIC:
                    operator = self.get_operation(token)
                    converted_line = converted_line.replace(
                        placeholders[index], '(&n0 ' + operator + ' &n1)')
                    index = 0
                elif token.type == Type.INT:
                    converted_line = converted_line.replace(
                        placeholders[index], token.val)
                    index = index + 1
            generated_code.append(converted_line)
        return generated_code

    def get_operation(self, token):
        if token.val == 'PLUS':
            return '+'
        elif token.val == 'MINUS':
            return '-'
        elif token.val == 'TIMES':
            return '*'
        elif token.val == 'DIVBY':
            return '/'
        elif token.val == 'MODU':
            return '%'
