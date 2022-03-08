from classtoken import *

#########################################
# NODES
#########################################


class NumberNode:
    def __init__(self, token: list):
        self.token = token

    def __str__(self) -> str:
        return f'{self.token[1]}'

    def __repr__(self) -> str:
        return self.__str__()


class BinaryOperationNode:
    def __init__(self, left_node: NumberNode, operation_token: NumberNode, right_node: NumberNode):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __str__(self) -> str:
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

    def __repr__(self) -> str:
        return self.__str__()

class UnaryOperationNode:
    def __init__(self, op_token, node):
        self.operation_token = op_token
        self.node = node

    def __str__(self) -> str:
        return f'({self.operation_token}, {self.node})'

    def __repr__(self) -> str:
        return self.__str__()

#########################################
# PARSER
#########################################


class Parser:
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens

    def parse(self, index: int, tokens: list):
        result = self.expression(index, tokens)
        return result

    def factor(self, index: int, tokens: list):
        # current token
        token = tokens[index]

        # Check for + or -
        if token[0] in (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS):
            factor = self.factor(index+1, tokens)
            return UnaryOperationNode(token, factor)

        # Check for INT or FLOAT
        elif token[0] in (TokensEnum.TOKEN_INT, TokensEnum.TOKEN_FLOAT):
            index += 1
            return NumberNode(token)

        # Check for (
        elif token[0] == TokensEnum.TOKEN_LPAREN:
            #print("index bij expr",index)
            expr = self.expression(index+1, tokens)
            return expr

    def term(self, index: int, tokens: list):
        # Left side of operation
        left = self.factor(index, tokens)
        return self.binary_operation(self.factor, (TokensEnum.TOKEN_MULTIPLY, TokensEnum.TOKEN_DIVIDE), left, index+1, tokens)

    def expression(self, index: int, tokens: list):
        left= self.term(index, tokens)
        return self.binary_operation(self.term, (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS), left, index+1, tokens)

    #Using func as decorator
    def binary_operation(self, func, operations: tuple, left: NumberNode, index: int, tokens: list):
        #print("Token index: ",tokens[index])
        if tokens[index][0] not in operations:
            #print("left:",left," Index: ", index)
            return left
        else:
            operation_token = tokens[index]
            right = func(index+1, tokens)
            left = BinaryOperationNode(left, operation_token, right)
            return self.binary_operation(func, operations, left, index+2, tokens)
