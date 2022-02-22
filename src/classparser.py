from classtoken import *

#########################################
# NODES
#########################################


class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

#########################################
# PARSER
#########################################


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens

    def parse(self, index, tokens):
        result = self.expression(index, tokens)
        return result

    def factor(self, index, tokens):
        token = tokens[index]
        if token[0] in (TOKEN_INT, TOKEN_FLOAT):
            index += 1
            return NumberNode(token)

    def term(self, index, tokens):
        left = self.factor(index, tokens)
        return self.binary_operation(self.factor, (TOKEN_MULTIPLY, TOKEN_DIVIDE), left, index+1, tokens)

    def expression(self, index, tokens):
        left = self.term(index, tokens)
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS), left, index+1, tokens)

    #Using func as decorator
    def binary_operation(self, func, operations: tuple, left, index, tokens):
        if tokens[index][0] not in operations:
            return left
        else:
            operation_token = tokens[index]
            index += 1
            right = func(index, tokens)
            left = BinaryOperationNode(left, operation_token, right)
            return self.binary_operation(func, operations, left, index, tokens)
