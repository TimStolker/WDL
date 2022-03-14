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

class VarAssignNode:
    def __init__(self, var_node: 'VarNode', value: 'Node'):
        self.name = var_node[1]
        self.value = value


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

    def __repr__(self) -> str:
        return self.__str__()

class IfNode:
    def __init__(self, cases: list, else_case: Union['Node', None]) -> None:
        self.cases = cases
        self.else_case = else_case

    def __str__(self) -> str:
        return f'IfNode: ({self.cases}, {self.else_case})'

    def __repr__(self) -> str:
        return self.__str__()

class WhileNode:
    def __init__(self, condition_node: 'Node', body_node: 'Node'):
        self.condition_node = condition_node
        self.body_node = body_node

    def __str__(self) -> str:
        return f'WhileNode: ({self.condition_node}, {self.body_node})'

    def __repr__(self) -> str:
        return self.__str__()

class FunctionNode:
    def __init__(self, function_name: Token, arguments: list, body: list) -> None:
        self.function_name = function_name
        self.arguments = arguments
        self.body = body

    def __str__(self) -> str:
        return f'Function: ({self.function_name}, {self.arguments}, {self.body})'

    def __repr__(self) -> str:
        return self.__str__()

class CallFunctionNode:
    def __init__(self, node_to_call: Token, arguments: list):
        self.node_to_call = node_to_call
        self.arguments = arguments

    def __str__(self) -> str:
        return f'FunctionCall: ({self.node_to_call}, {self.arguments})'

    def __repr__(self) -> str:
        return self.__str__()

Node = Union[NumberNode,BinaryOperationNode,VarNode, VarAccessNode, IfNode, VarAssignNode, WhileNode, FunctionNode]

#########################################
# PARSER
#########################################


def parse(index: int, tokens: list, ast_list: list) -> list:
    result, index = expression(index, tokens)
    ast_list.append([result])
    # In case if the code input ends with an if statement (needs further research)
    # This still needs fixing, if statements tend to return index+1 sometimes
    if tokens[index][1] == 'EOF':
        return ast_list

    elif tokens[index+1][1] == 'EOF':
        return ast_list
    else:
        return parse(index+1, tokens, ast_list)

def addParameters(index: int, tokens: list, arg_name_tokens: list) -> Tuple[list, int]:
    # Check for a comma
    if tokens[index][0] != TokensEnum.TOKEN_COMMA:
        return arg_name_tokens, index
    else:
        # Append the parameter name to the list
        arg_name_tokens.append(tokens[index+1][1])
        return addParameters(index+2, tokens, arg_name_tokens)

def addFuncBody(index: int, tokens: list, body_list: list) -> Tuple[list, int]:
    if tokens[index][0] == TokensEnum.TOKEN_END_FUNCTION:
        # return the body list with the next character
        return body_list, index+1
    expr, new_index = expression(index, tokens)
    body_list.append([expr])
    return addFuncBody(new_index, tokens, body_list)


def appendelifcases(index: int, tokens: list, cases: list) -> Tuple[list, int]:
    if tokens[index][0] != TokensEnum.ELSE_IF:
        return cases, index
    condition, then_index = expression(index+1, tokens)
    if tokens[then_index][0] != TokensEnum.THEN:
        raise Exception("No 'DANN' keyword found in 'ANDALS' statement")
    else:
        expr, new_index = expression(then_index+1, tokens)
        cases.append((expr,condition))
        return appendelifcases(new_index, tokens, cases)


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
        cases.append((expr,condition))
        if tokens[elif_index][0] == TokensEnum.ELSE_IF:
            # Store the 'ANDALS' cases
            cases, new_index = appendelifcases(elif_index, tokens, cases)
            if tokens[new_index][0] == TokensEnum.ELSE:
                else_case, else_index = expression(new_index+1, tokens)
                return IfNode(cases, else_case), else_index
            return IfNode(cases, else_case), new_index
        elif tokens[elif_index][0] == TokensEnum.ELSE:
            else_case, else_index = expression(elif_index + 1, tokens)
            return IfNode(cases, else_case), else_index
        else:
            return IfNode(cases, else_case), elif_index


def while_expr(index: int, tokens: list) -> Tuple[WhileNode, int]:

    condition, loop_index = expression(index, tokens)
    if tokens[loop_index][0] != TokensEnum.LOOP:
        raise Exception("No 'WIEDERHOLEN' declared after condition")
    else:
        body, body_index = expression(loop_index+1, tokens)
        return WhileNode(condition, body), body_index


def func_def(index: int, tokens: list) -> Tuple[FunctionNode, int]:
    # Check for function name
    if tokens[index][0] != TokensEnum.TOKEN_NAME:
        raise Exception("No function name found")
    else:
        func_name = tokens[index][1]
        # Check for '('
        if tokens[index+1][0] != TokensEnum.TOKEN_LPAREN:
            raise Exception("No '(' found in function declaration")
        else:
            arg_name_tokens = []
            # Check for parameter name
            if tokens[index+2][0] == TokensEnum.TOKEN_NAME:
                # Append the parameters to the list
                arg_name_tokens.append(tokens[index+2][1])
                # Append other parameters to the list
                arg_name_tokens, new_index = addParameters(index+3, tokens, arg_name_tokens)
                if tokens[new_index][0] != TokensEnum.TOKEN_RPAREN:
                    raise Exception("No ')' found in function declaration")
                else:
                    if tokens[new_index+1][0] != TokensEnum.TOKEN_BEGIN_FUNCTION:
                        raise Exception("No '{' in function declaration")
                    # Get the expressions
                    empty_body_list = []
                    body_list, new_index = addFuncBody(index+2, tokens, empty_body_list)
                    return FunctionNode(func_name, arg_name_tokens, body_list), new_index





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

    # Check for While statement
    elif token[0] == TokensEnum.WHILE:
        while_expression, new_index = while_expr(index+1, tokens)
        return while_expression, new_index

    # Check for function statement
    elif token[0] == TokensEnum.FUNCTION:
        func_defenition, new_index = func_def(index+1, tokens)
        return func_defenition, new_index

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
                raise Exception("Expected '=' for variable declare")
            else:
                expr, new_index = expression(index+3, tokens)
                var = VarNode(tokens[index+1], expr)
                return var, new_index
    # Check for
    elif tokens[index][0] == TokensEnum.TOKEN_NAME:
        if tokens[index+1][0] != TokensEnum.TOKEN_EQUAL:
            left, new_index = arithmic(index, tokens)
            return binary_operation(arithmic, (TokensEnum.TOKEN_GREATER, TokensEnum.TOKEN_LESSER, TokensEnum.TOKEN_LESSER_EQUAL,TokensEnum.TOKEN_GREATER_EQUAL, TokensEnum.TOKEN_DOUBLE_EQUAL), left, new_index, tokens)
        else:
            expr, new_index = expression(index+2, tokens)
            var = VarAssignNode(tokens[index], expr)
            return var, new_index


    left, new_index= arithmic(index, tokens)
    return binary_operation(arithmic, (TokensEnum.TOKEN_GREATER, TokensEnum.TOKEN_LESSER, TokensEnum.TOKEN_LESSER_EQUAL, TokensEnum.TOKEN_GREATER_EQUAL, TokensEnum.TOKEN_DOUBLE_EQUAL), left, new_index, tokens)


#Using func as decorator
def binary_operation(func, operations: tuple, left: Node, index: int, tokens: list) -> Tuple[Node,int]:
    # A binary operation is an algorithmic expression

    # Check for endline
    if tokens[index][0] == TokensEnum.ENDE or tokens[index][0] == TokensEnum.TOKEN_END_FUNCTION or tokens[index][0] == TokensEnum.SLA or tokens[index][0] == TokensEnum.NELOHREDEIW:
        return left, index
    elif tokens[index][0] not in operations or index >= len(tokens):
        return left, index
    else:
        operation_token = tokens[index]
        right, new_index= func(index+1, tokens)
        left = BinaryOperationNode(left, operation_token, right)
        return binary_operation(func, operations, left ,new_index, tokens)
