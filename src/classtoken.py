#########################################
# TOKENS
#########################################

TOKEN_INT = 'NUMMER'
TOKEN_FLOAT = 'SCHWEBER'
TOKEN_CHAR = 'CHARAKTER'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLIZIEREN'
TOKEN_DIVIDE = 'TEILEN'
TOKEN_LPAREN = 'LKLAMMER'
TOKEN_RPAREN = 'RKLAMMER'
TOKEN_EQUAL = 'GLEICH'
TOKEN_LBRACKET = 'ECKIGELKLAMMER'
TOKEN_RBRACKET = 'ECKIGERKLAMMER'
TOKEN_GREATER = 'GRÖSSER'
TOKEN_LESSER = 'WENIGER'
TOKEN_COMMA = 'KOMMA'
TOKEN_ERROR = 'ERROR'
TOKEN_EOF = 'ENDE DER DATEI'


class Token:
    def __init__(self, type_: str, value: str) -> None:
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
