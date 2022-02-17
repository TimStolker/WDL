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
        self.index = -1
        self.current_token = self.tokens[self.index]
        self.next_character()

    def next_character(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        return self.current_token

    def parse(self):
        result = self.expression()
        return result

    def factor(self):
        token = self.current_token
        if token[0] in (TOKEN_INT, TOKEN_FLOAT):
            self.next_character()
            return NumberNode(token)

    def term(self):
        left = self.factor()
        return self.binary_operation(self.factor, (TOKEN_MULTIPLY, TOKEN_DIVIDE), left)

    def expression(self):
        left = self.term()
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS), left)

    #Using func as decorator
    def binary_operation(self, func, operations: tuple, left):
        if self.current_token[0] not in operations:
            return left
        else:
            operation_token = self.current_token
            self.next_character()
            right = func()
            left = BinaryOperationNode(left, operation_token, right)
            return self.binary_operation(func, operations, left)
