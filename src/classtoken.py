from enum import Enum
from typing import Type
#########################################
# TOKENS
#########################################


class TokensEnum(Enum):
    # Special tokens
    TOKEN_INT           = 'NUMMER'
    TOKEN_FLOAT         = 'SCHWEBER'
    TOKEN_PLUS          = '+'
    TOKEN_MINUS         = '-'
    TOKEN_MULTIPLY      = '*'
    TOKEN_DIVIDE        = '/'
    TOKEN_LPAREN        = '('
    TOKEN_RPAREN        = ')'
    TOKEN_EQUAL         = '='
    TOKEN_BEGIN_FUNCTION= '{'
    TOKEN_END_FUNCTION  = '}'
    TOKEN_COMMA         = ','

    TOKEN_ERROR         = 'ERROR'
    TOKEN_EOF           = 'EOF'
    TOKEN_NAME = 'NAME'

    # Conditional tokens
    TOKEN_GREATER       = '>'
    TOKEN_LESSER        = '<'
    TOKEN_GREATER_EQUAL = '>='
    TOKEN_LESSER_EQUAL  = '<='
    TOKEN_DOUBLE_EQUAL  = '=='

    # Reserved words
    IF = 'ALS'
    ELSE_IF = 'ANDALS'
    ELSE = 'ANDERS'
    THEN = 'DANN'
    WHILE = 'WAHREND'
    LOOP = 'WIEDERHOLEN'
    FUNCTION = 'FUNKTION'
    VAR = 'VAR'
    ENDE = 'ENDE'
    RETURN = 'RETURN'

    # End words
    SLA = 'SLA'
    NELOHREDEIW = 'NELOHREDEIW'




class Token:
    def __init__(self, token_type: TokensEnum, value: str) -> None:
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f'({self.type}, {self.value})'

    def __repr__(self) -> str:
        return self.__str__()
