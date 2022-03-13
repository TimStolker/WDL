from classtoken import *
from typing import Tuple, Union, Optional
#########################################
# NODES
#########################################


class NumberNode:
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return f'{self.token}'

    def __repr__(self) -> str:
        return self.__str__()


class VarAccessNode:
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return f'{self.token}'

    def __repr__(self) -> str:
        return self.__str__()


class BinaryOperationNode:
    def __init__(self, left_node: 'Node', operation_token: Token, right_node: 'Node') -> None:
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __str__(self) -> str:
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

    def __repr__(self) -> str:
        return self.__str__()


class VarNode:
    def __init__(self, name: Token, var_value: 'Node') -> None:
        self.name = name
        self.var_value = var_value

    def __str__(self) -> str:
        return f'Var: ({self.name},{self.var_value})'

class IfNode:
    def __init__(self, cases: list, else_case: Union['Node', None]) -> None:
        self.cases = cases
        self.else_case = else_case

class FunctionNode:
    def __init__(self, function_name: str, arguments: list, block: list, return_type: Token) -> None:
        self.function_name = function_name
        self.arguments = arguments
        self.code_block = block
        self.return_type = return_type

    def __str__(self) -> str:
        return f'Function: {self.function_name}, {self.return_type}'

Node = Union[NumberNode,BinaryOperationNode,VarNode, VarAccessNode, IfNode]

#########################################
# PARSER
#########################################


def parse(index: int, tokens: list, ast_list: list) -> list:
    result, index = expression(index, tokens)
    print("parse index result:", type(result), index)
    ast_list.append([result])
    # In case if the code input ends with an if statement (needs further research)
    #if tokens[index][1] == 'EOF':
    #    return ast_list
    if tokens[index+1][1] == 'EOF':
        return ast_list
    else:
        return parse(index+1, tokens, ast_list)


def appendelifcases(index: int, tokens: list, cases: list) -> Tuple[list, int]:
    # Current token
    if tokens[index][0] != TokensEnum.ELSE_IF:
        return cases, index
    condition, then_index = expression(index+1, tokens)
    if tokens[then_index][0] != TokensEnum.THEN:
        raise Exception("No 'DANN' keyword found in 'ANDDAN' statement")
    else:
        expr, new_index = expression(then_index+1, tokens)
        cases.append((condition,expr))
        return appendelifcases(new_index+1, tokens, cases)


def if_expr(index: int, tokens: list) -> Tuple[IfNode, int]:

    cases = []
    else_case = None
    # Get the conditional expression
    condition, then_index = expression(index, tokens)
    if tokens[then_index][0] != TokensEnum.THEN:
        raise Exception("No 'DANN' keyword found for if statement")
    else:
        # Get the expression after 'DANN'
        expr, elif_index = expression(then_index+1, tokens)
        if tokens[elif_index][0] == TokensEnum.ELSE_IF:
            # Store the 'ANDDAN' cases
            cases, new_index = appendelifcases(elif_index+1, tokens, cases)
            if tokens[new_index][0] == TokensEnum.ELSE:
                else_case, else_index = expression(new_index+1, tokens)
            return IfNode(cases, else_case), else_index
        elif tokens[elif_index][0] == TokensEnum.ELSE:
            else_case, else_index = expression(elif_index + 1, tokens)
            print("else: ", else_index, tokens[else_index][0])
            return IfNode(cases, else_case), else_index
        else:
            return IfNode(cases, else_case), elif_index


def factor(index: int, tokens: list) -> Tuple[Node,int,]:
    # The factor is the node that will be used in a term

    # current token
    token = tokens[index]

    # Check for INT or FLOAT
    if token[0] in (TokensEnum.TOKEN_INT, TokensEnum.TOKEN_FLOAT):
        return NumberNode(token), index+1

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

    # Check for IF statement
    elif token[0] == TokensEnum.IF:
        if_expression, new_index = if_expr(index+1, tokens)
        return if_expression, new_index


def term(index: int, tokens: list) -> Tuple[Node,int]:
    # A term is a mutiply or devision node

    # Left side of operation
    left, new_index = factor(index, tokens)
    return binary_operation(factor, (TokensEnum.TOKEN_MULTIPLY, TokensEnum.TOKEN_DIVIDE), left, new_index, tokens)

def arithmic(index: int, tokens:list) -> Tuple[Node,int]:
    left, new_index = term(index, tokens)
    return binary_operation(term, (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS), left, new_index, tokens)

def expression(index: int, tokens: list) -> Tuple[Node,int]:
    # An expression is a plus or minus node

    # Check for variable declaration
    if tokens[index][0] == TokensEnum.VAR:
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

    left, new_index= arithmic(index, tokens)
    return binary_operation(arithmic, (TokensEnum.TOKEN_GREATER, TokensEnum.TOKEN_LESSER, TokensEnum.TOKEN_LESSER_EQUAL, TokensEnum.TOKEN_GREATER_EQUAL, TokensEnum.TOKEN_DOUBLE_EQUAL), left, new_index, tokens)


#Using func as decorator
def binary_operation(func, operations: tuple, left: Node, index: int, tokens: list) -> Tuple[Node,int]:
    # A binary operation is an algorithmic expression

    # Check for endline
    if tokens[index][0] == TokensEnum.ENDE or tokens[index][0] == TokensEnum.END_FUNCTION or tokens[index][0] == TokensEnum.SLA:
        return left, index
    elif tokens[index][0] not in operations or index >= len(tokens):
        return left, index
    else:
        operation_token = tokens[index]
        right, new_index= func(index+1, tokens)
        left = BinaryOperationNode(left, operation_token, right)
        return binary_operation(func, operations, left ,new_index, tokens)
