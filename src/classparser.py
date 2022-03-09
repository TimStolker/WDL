from classtoken import *
from typing import Tuple, Union
#########################################
# NODES
#########################################


class NumberNode:
    def __init__(self, token: Token):
        self.token = token

    def __str__(self) -> str:
        return f'{self.token}'

    def __repr__(self) -> str:
        return self.__str__()


class BinaryOperationNode:
    def __init__(self, left_node: 'Node', operation_token: Token, right_node: 'Node'):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __str__(self) -> str:
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

    def __repr__(self) -> str:
        return self.__str__()


class VarNode:
    def __init__(self, name: Token, value: 'Node'):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'Var: ({self.name},{self.value})'


class AssignNode:
    def __init__(self, left: VarNode, operation: Token, right: NumberNode) -> None:
        self.left = left
        self.token = self.operation = operation
        self.right = right

    def __str__(self) -> str:
        return f'Assign: ({self.left}, {self.operation.value}, {self.right})'


class ConditionalNode:
    def __init__(self, left: Union[VarNode, NumberNode], condition: Token, right :Union[VarNode, NumberNode]) -> None:
        self.left = left
        self.condition = condition
        self.right = right

    def __str__(self) -> str:
        return f'Conditional: ({self.left}, {self.condition}, {self.right})'


class IfElseNode:
    def __init__(self, condition: ConditionalNode, block: list, else_node: Token) -> None:
        self.condition = condition
        self.if_block = block
        self.else_node = else_node

    def __str__(self) -> str:
        return f'IfElse: ({self.condition})'


class FunctionNode:
    def __init__(self, function_name: str, arguments: list, block: list, return_type: Token):
        self.function_name = function_name
        self.arguments = arguments
        self.code_block = block
        self.return_type = return_type

    def __str__(self) -> str:
        return f'Function: {self.function_name}, {self.return_type}'

Node = Union[NumberNode,BinaryOperationNode,VarNode]

#########################################
# PARSER
#########################################


class Parser:
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens

    def parse(self, index: int, tokens: list) -> Node:
        result, index = self.expression(index, tokens)
        return result

    def factor(self, index: int, tokens: list) -> Tuple[Node,int]:
        # The factor is the node that will be used in a term

        # current token
        token = tokens[index]

        # Check for INT or FLOAT
        if token[0] in (TokensEnum.TOKEN_INT, TokensEnum.TOKEN_FLOAT):
            return NumberNode(token), index+1

        elif tokens[index][0] == TokensEnum.VAR:
            if tokens[index+1][0] != TokensEnum.TOKEN_NAME:
                raise Exception("Expected variable name")
            else:
                # Get the value
                var_name = tokens[index+1][1]
                print("var name:", var_name)
                if tokens[index+2][0] != TokensEnum.TOKEN_EQUAL:
                    raise Exception("Expected '='")
                else:
                    expr, new_index = self.expression(index+3, tokens)
                    return VarNode(Token(TokensEnum.TOKEN_NAME,var_name), expr), new_index+1

        # Check for (
        elif token[0] == TokensEnum.TOKEN_LPAREN:
            expr, new_index = self.expression(index+1, tokens)
            # Check for )
            if tokens[new_index][0] == TokensEnum.TOKEN_RPAREN:
                return expr, new_index+1
            else:
                raise Exception("No ) found", tokens[new_index], new_index)

    def term(self, index: int, tokens: list) -> Tuple[Node,int]:
        # A term is a mutiply or devision node

        # Left side of operation
        left, new_index = self.factor(index, tokens)
        return self.binary_operation(self.factor, (TokensEnum.TOKEN_MULTIPLY, TokensEnum.TOKEN_DIVIDE), left, new_index, tokens)

    def expression(self, index: int, tokens: list) -> Tuple[Node,int]:
        # An expression is a plus or minus node

        left, void_index = self.term(index, tokens)
        return self.binary_operation(self.term, (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS), left, void_index, tokens)

    #Using func as decorator
    def binary_operation(self, func, operations: tuple, left: Node, index: int, tokens: list) -> Tuple[Node,int]:
        if tokens[index][0] not in operations or tokens[index][1] == 'EOF':
            return left, index
        else:
            operation_token = tokens[index]
            right, new_index = func(index+1, tokens)
            left = BinaryOperationNode(left, operation_token, right)
            return self.binary_operation(func, operations, left ,new_index, tokens)
