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


class VarAccessNode:
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
    def __init__(self, name: Token, var_value: 'Node'):
        self.name = name
        self.var_value = var_value

    def __str__(self) -> str:
        return f'Var: ({self.name},{self.var_value})'

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

Node = Union[NumberNode,BinaryOperationNode,VarNode, VarAccessNode]

#########################################
# PARSER
#########################################


def parse(index: int, tokens: list, ast_list: list) -> list:
    result, index = expression(index, tokens)
    ast_list.append([result])
    if tokens[index+1][1] == 'EOF':
        return ast_list
    else:
        return parse(index+1, tokens, ast_list)


def factor(index: int, tokens: list) -> Tuple[Node,int,]:
    # The factor is the node that will be used in a term

    # current token
    token = tokens[index]

    # Check for INT or FLOAT
    if token[0] in (TokensEnum.TOKEN_INT, TokensEnum.TOKEN_FLOAT):
        return NumberNode(token), index+1

    # Check for Var type
    elif tokens[index][0] == TokensEnum.VAR:
        if tokens[index+1][0] != TokensEnum.TOKEN_NAME:
            raise Exception("Expected variable name")
        else:
            # Get the value
            #var_name = tokens[index+1][1]
            if tokens[index+2][0] != TokensEnum.TOKEN_EQUAL:
                raise Exception("Expected '='")
            else:
                expr, new_index = expression(index+3, tokens)
                var = VarNode(tokens[index+1], expr)
                return var, new_index

    # Check for Var name
    elif tokens[index][0] == TokensEnum.TOKEN_NAME:
        return VarAccessNode(token), index+1


    # Check for (
    elif token[0] == TokensEnum.TOKEN_LPAREN:
        expr, new_index = expression(index+1, tokens)
        # Check for )
        if tokens[new_index][0] == TokensEnum.TOKEN_RPAREN:
            return expr, new_index+1
        else:
            raise Exception("No ) found", tokens[new_index], new_index)


def term(index: int, tokens: list) -> Tuple[Node,int]:
    # A term is a mutiply or devision node

    # Left side of operation
    left, new_index = factor(index, tokens)
    return binary_operation(factor, (TokensEnum.TOKEN_MULTIPLY, TokensEnum.TOKEN_DIVIDE), left, new_index, tokens)


def expression(index: int, tokens: list) -> Tuple[Node,int]:
    # An expression is a plus or minus node

    left, void_index= term(index, tokens)
    return binary_operation(term, (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS), left, void_index, tokens)


#Using func as decorator
def binary_operation(func, operations: tuple, left: Node, index: int, tokens: list) -> Tuple[Node,int]:
    # A binary operation is an algorithmic expression

    # Check for endline
    if tokens[index][0] == TokensEnum.ENDE:
        return left, index
    elif tokens[index][0] not in operations or index >= len(tokens):
        return left, index
    else:
        operation_token = tokens[index]
        right, new_index= func(index+1, tokens)
        left = BinaryOperationNode(left, operation_token, right)
        return binary_operation(func, operations, left ,new_index, tokens)
