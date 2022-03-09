from classtoken import *
from classparser import *
from classinterpreter import *

#########################################
# LEXER
#########################################


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text = text

    def check_eof(self, text: str, position: int) -> bool:
        # Check of the current position is still in the text
        return position > len(text) - 1

    def next_digit(self, text: str, position: int, dot_count: int) -> str:
        # Check if the current character is a digit or a dot
        if not self.check_eof(text, position) and text[position].isdigit() or not self.check_eof(text, position) and text[position] == '.':
            if text[position] == '.':
                if dot_count == 1:
                    raise Exception("Float only has 1 dot")

                dot_count += 1
                return text[position] + self.next_digit(text, position + 1, dot_count)

            elif text[position].isdigit():
                return text[position] + self.next_digit(text, position + 1, dot_count)
        return ''

    def next_word(self, text: str, position: int) -> str:
        # Check if the current character is alphabetical
        if not self.check_eof(text, position) and text[position].isalpha():
            return text[position] + self.next_word(text, position + 1)
        return ''

    def next_token(self, tokens: list, index: int, text: str, line: int) -> list:
        # Check if the current position in still in the text
        if index > len(text) - 1:
            tokens.append((TokensEnum.TOKEN_EOF, 'EOF'))
            return tokens

        current_char = text[index]

        if current_char.isspace():
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '+':
            tokens.append((TokensEnum.TOKEN_PLUS, '+'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '-':
            tokens.append((TokensEnum.TOKEN_MINUS, '-'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '/':
            tokens.append((TokensEnum.TOKEN_DIVIDE, '/'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '*':
            tokens.append((TokensEnum.TOKEN_MULTIPLY, '*'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '(':
            tokens.append((TokensEnum.TOKEN_LPAREN, '('))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ')':
            tokens.append((TokensEnum.TOKEN_RPAREN, ')'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '[':
            tokens.append((TokensEnum.TOKEN_LBRACKET, '['))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ']':
            tokens.append((TokensEnum.TOKEN_RBRACKET, ']'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '=':
            tokens.append((TokensEnum.TOKEN_EQUAL, '='))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '>':
            tokens.append((TokensEnum.TOKEN_GREATER, '>'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == '<':
            tokens.append((TokensEnum.TOKEN_LESSER, '<'))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char == ',':
            tokens.append((TokensEnum.TOKEN_COMMA, ','))
            return self.next_token(tokens, index + 1, text, line)

        elif current_char.isdigit():
            digit = current_char + self.next_digit(text, index + 1, 0)
            index += len(digit)
            # Check for float
            if '.' in digit:
                tokens.append((TokensEnum.TOKEN_FLOAT, float(digit)))
            else:
                tokens.append((TokensEnum.TOKEN_INT, int(digit)))
            return self.next_token(tokens, index, text, line)

        elif current_char.isalpha():
            letters = current_char + self.next_word(text, index + 1)
            index += len(letters)

            # Check for var type
            if letters == 'VAR':
                tokens.append((TokensEnum.VAR, letters))
            elif letters == 'ALS':
                tokens.append((TokensEnum.IF, letters))
            elif letters == 'ANDERS':
                tokens.append((TokensEnum.ELSE, letters))
            elif letters == 'DANN':
                tokens.append((TokensEnum.THEN, letters))
            elif letters == 'WAHREND':
                tokens.append((TokensEnum.WHILE, letters))
            elif letters == 'WIEDERHOLEN':
                tokens.append((TokensEnum.LOOP, letters))
            elif letters == 'ß':
                tokens.append((TokensEnum.FUNCTION, letters))
            elif letters == 'ENDE':
                tokens.append((TokensEnum.ENDE, letters))
            else:
                # Variable name
                tokens.append((TokensEnum.TOKEN_NAME, letters))
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
    #return tokens
    #Make AST
    parser = Parser(tokens)
    ast = parser.parse(0, tokens)
    #return ast
    #Interpreter
    interpreter = Interpreter()
    result = interpreter.visit(ast)
    return result
