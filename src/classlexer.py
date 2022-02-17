from classtoken import *
from classparser import Parser

#########################################
# LEXER
#########################################

class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text = text

    def check_eof(self, text: str, position: int) -> bool:
        return position > len(text) - 1

    def next_digit(self, text: str, position: int, dot_count: int) -> str:
        if not self.check_eof(text, position) and text[position].isdigit() or not self.check_eof(text, position) and \
                text[position] == '.':
            if text[position] == '.':
                if dot_count == 1:
                    raise Exception("DU DUMMKOPF, EIN SCHWEBER HAT NUR EINEN PUNKT")
                dot_count += 1
                return text[position] + self.next_digit(text, position + 1, dot_count)
            elif text[position].isdigit():
                return text[position] + self.next_digit(text, position + 1, dot_count)
        return ''

    def next_word(self, text: str, position: int) -> str:
        if not self.check_eof(text, position) and text[position].isalpha():
            return text[position] + self.next_word(text, position + 1)
        return ''

    def next_token(self, tokens: list, index: int, text: str, line: int) -> list:
        if index > len(text) - 1:
            tokens.append((TOKEN_EOF, ''))
            return tokens

        current_char = text[index]

        if current_char.isspace():
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '+':
            tokens.append((TOKEN_PLUS, '+'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '-':
            tokens.append((TOKEN_MINUS, '-'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '/':
            tokens.append((TOKEN_DIVIDE, '/'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '*':
            tokens.append((TOKEN_MULTIPLY, '*'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '(':
            tokens.append((TOKEN_LPAREN, '('))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ')':
            tokens.append((TOKEN_RPAREN, ')'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '[':
            tokens.append((TOKEN_LBRACKET, '['))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ']':
            tokens.append((TOKEN_RBRACKET, ']'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '=':
            tokens.append((TOKEN_EQUAL, '='))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '>':
            tokens.append((TOKEN_GREATER, '>'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '<':
            tokens.append((TOKEN_LESSER, '<'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ',':
            tokens.append((TOKEN_COMMA, ','))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char.isdigit():
            digit = current_char + self.next_digit(text, index + 1, 0)
            index += len(digit)
            if '.' in digit:
                tokens.append((TOKEN_FLOAT, float(digit)))
            else:
                tokens.append((TOKEN_INT, int(digit)))
            return self.next_token(tokens, index, text, line)

        elif current_char.isalpha():
            letters = current_char + self.next_word(text, index + 1)
            index += len(letters)
            tokens.append((TOKEN_CHAR, letters))
            return self.next_token(tokens, index, text, line)

        elif current_char == '\n':
            return self.next_token(tokens, index + 1, text, line + 1)

        else:
            raise Exception("Illegal character: " "'" + current_char + "'" + " at line: " + str(line))



def run(filename: str, text: str) -> list:
    #Identify the tokens
    tokens = []
    lexer = Lexer(filename, text)
    tokens = lexer.next_token(tokens, 0, text, 0)
    #Make AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast

