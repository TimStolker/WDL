from enum import Enum
from typing import Type
#########################################
# TOKENS
#########################################


class TokensEnum(Enum):
    # Special tokens
    TOKEN_INT           = 'NUMMER'
    TOKEN_NINT          = 'NEGATIVE NUMMER'
    TOKEN_FLOAT         = 'SCHWEBER'
    TOKEN_PLUS          = '+'
    TOKEN_MINUS         = '-'
    TOKEN_MULTIPLY      = '*'
    TOKEN_DIVIDE        = '/'
    TOKEN_LPAREN        = '('
    TOKEN_RPAREN        = ')'
    TOKEN_EQUAL         = '='
    TOKEN_GREATER       = '>'
    TOKEN_LESSER        = '<'
    TOKEN_ERROR         = 'ERROR'
    TOKEN_EOF           = 'EOF'
    TOKEN_NAME = 'NAME'

    # Reserved words
    IF = 'ALS'
    ELSE = 'ANDERS'
    THEN = 'DANN'
    WHILE = 'WAHREND'
    LOOP = 'WIEDERHOLEN'
    FUNCTION = 'ß'
    VAR = 'VAR'




class Token:
    def __init__(self, token_type: TokensEnum, value: str) -> None:
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f'({self.type}, {self.value})'

    def __repr__(self) -> str:
        return self.__str__()
