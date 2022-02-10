from token import *

#########################################
# ERROR
#########################################

class Error:
    def __init__(self, start_position, end_position, error_name: str, details: str):
        self.start_position = start_position
        self.end_position = end_position
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' In: {self.start_position.filename} AUF ZEILE: {self.start_position.line+1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, start_position, end_position, details):
        super().__init__(start_position, end_position,'UNZULÄSSIGES ZEICHEN ', details)

#########################################
# POSITION
#########################################

class Position:
    def __init__(self, index: int, line: int, filename: str):
        self.index = index
        self.line = line
        self.filename = filename

    def next(self, current_char):
        self.index += 1

        if current_char == ' \n':
            self.line += 1

        return self

    def copy(self):
        return Position(self.index, self.line, self.filename)

#########################################
# LEXER
#########################################

class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text = text
        self.position = Position(0, 0, filename)
        self.current_token = None

    def check_eof(self, text: str, position: int) -> bool:
        return position > len(text) -1

    def next_digit(self, text: str, position: int, dot_count: int) -> str:
        if not self.check_eof(text, position) and text[position].isdigit() or not self.check_eof(text, position) and text[position] == '.':
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

    def next_token(self, tokens: list):
        if self.position.index > len(self.text) -1:
            tokens.append((TOKEN_EOF, ''))
            return tokens, None

        current_char = self.text[self.position.index]

        if current_char.isspace():
            self.position.next(current_char)
            return self.next_token(tokens)

        elif current_char == '+':
            self.position.next(current_char)
            tokens.append((TOKEN_PLUS, '+'))
            return self.next_token(tokens)

        elif current_char == '-':
            self.position.next(current_char)
            tokens.append((TOKEN_MINUS, '-'))
            return self.next_token(tokens)

        elif current_char == '/':
            self.position.next(current_char)
            tokens.append((TOKEN_DIVIDE, '/'))
            return self.next_token(tokens)

        elif current_char == '*':
            self.position.next(current_char)
            tokens.append((TOKEN_MULTIPLY, '*'))
            return self.next_token(tokens)

        elif current_char == '(':
            self.position.next(current_char)
            tokens.append((TOKEN_LPAREN, '('))
            return self.next_token(tokens)

        elif current_char == ')':
            self.position.next(current_char)
            tokens.append((TOKEN_RPAREN, ')'))
            return self.next_token(tokens)

        elif current_char.isdigit():
            digit = current_char + self.next_digit(self.text, self.position.index+1, 0)
            self.position.index += len(digit)
            if '.' in digit:
                tokens.append((TOKEN_FLOAT, float(digit)))
            else:
                tokens.append((TOKEN_INT, int(digit)))
            return self.next_token(tokens)

        elif current_char.isalpha():
            letters = current_char + self.next_word(self.text, self.position.index+1)
            self.position.index += len(letters)
            tokens.append((TOKEN_CHAR, letters))
            return self.next_token(tokens)

        else:
            start_position = self.position.copy()
            char = current_char
            self.position.next(current_char)
            return [], IllegalCharacterError(start_position, self.position, "'" + char + "'")
            #raise Exception("CHARAKTER '" + current_char + "' IST ILLEGAL!")

    def run(filename: str, text: str):
        tokens = []
        lexer = Lexer(filename, text)
        tokens, error = lexer.next_token(tokens)
        return tokens, error
