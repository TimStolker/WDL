#------
#ToKeNs
#------

TOKEN_INT = 'NUMMER'
TOKEN_FLOAT = 'SCHWEBER'
TOKEN_CHAR = 'CHARAKTER'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLIZIEREN'
TOKEN_DIVIDE = 'TEILEN'
TOKEN_LPAREN = 'LKLAMMER'
TOKEN_RPAREN = 'RKLAMMER'
TOKEN_EOF = 'ENDE DER DATEI'
#spaces toevoegen?

class ToKeN:
    def __init__(self, type : str, value : str) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return 'Token {type}, {value}'.format(type=self.type, value=repr(self.value))

    def __repr__(self) -> str:
        return self.__str__()
