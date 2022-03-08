from enum import Enum
from typing import Type
#########################################
# TOKENS
#########################################


class TokensEnum(Enum):
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
    TOKEN_GREATER = 'GRÖSSER'
    TOKEN_LESSER = 'WENIGER'
    TOKEN_ERROR = 'ERROR'
    TOKEN_EOF = 'ENDE DER DATEI'


class Token:
    def __init__(self, type_: TokensEnum, value: str) -> None:
        self.type = type_
        self.value = value

    def __str__(self) -> str:
        return f'({self.type}, {self.value})'

    def __repr__(self) -> str:
        return self.__str__()
