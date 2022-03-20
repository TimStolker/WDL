from classtoken import *
from typing import Tuple, Union, List, Callable
#########################################
# NODES
#########################################


class NumberNode:
    # __init__ :: Token -> None
    def __init__(self, token: Token) -> None:
        self.token = token

    # __init__ :: str
    def __str__(self) -> str:
        return f'NumberNode: ({self.token})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class VarAccessNode:
    # __init__ :: Token -> None
    def __init__(self, token: Token) -> None:
        self.token = token

    # __init__ :: str
    def __str__(self) -> str:
        return f'VarAccessNode: ({self.token})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class VarAssignNode:
    # __init__ :: Token, Node -> None
    def __init__(self, var_node: [Token], value: 'Node') -> None:
        self.name = var_node[1]
        self.value = value

    # __init__ :: str
    def __str__(self) -> str:
        return f'VarAssignNode: ({self.name}, {self.value})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class BinaryOperationNode:
    # __init__ :: Node, Token, Node -> None
    def __init__(self, left_node: 'Node', operation_token: Token, right_node: 'Node') -> None:
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    # __init__ :: str
    def __str__(self) -> str:
        return f'BinaryOperationNode: ({self.left_node}, {self.operation_token}, {self.right_node})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class VarNode:
    # __init__ :: Token, Node -> None
    def __init__(self, name: Token, var_value: 'Node') -> None:
        self.name = name
        self.var_value = var_value

    # __init__ :: str
    def __str__(self) -> str:
        return f'VarNode: ({self.name},{self.var_value})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class IfNode:
    # __init__ :: list, Union['Node', None] -> None
    def __init__(self, cases: list, else_case: Union['Node', None]) -> None:
        self.cases = cases
        self.else_case = else_case

    # __init__ :: str
    def __str__(self) -> str:
        return f'IfNode: ({self.cases}, {self.else_case})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class WhileNode:
    # __init__ :: Node, Node -> None
    def __init__(self, condition_node: 'Node', body_node: 'Node') -> None:
        self.condition_node = condition_node
        self.body_node = body_node

    # __init__ :: str
    def __str__(self) -> str:
        return f'WhileNode: ({self.condition_node}, {self.body_node})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class FunctionNode:
    # __init__ :: Token, list, List[Node] -> None
    def __init__(self, function_name: Token, arguments: list, body: List['Node']) -> None:
        self.function_name = function_name
        self.arguments = arguments
        self.body = body

    # __init__ :: str
    def __str__(self) -> str:
        return f'FunctionNode: ({self.function_name}, {self.arguments}, {self.body})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class CallFunctionNode:
    # __init__ :: Token, list -> None
    def __init__(self, node_to_call: Token, arguments: list) -> None:
        self.node_to_call = node_to_call
        self.arguments = arguments

    # __init__ :: str
    def __str__(self) -> str:
        return f'CallFunctionNode: ({self.node_to_call}, {self.arguments})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


class ReturnNode:
    # __init__ :: Node -> None
    def __init__(self, return_value: 'Node') -> None:
        self.return_value = return_value

    # __init__ :: str
    def __str__(self) -> str:
        return f'ReturnNode: ({self.return_value})'

    # __repr__ :: str
    def __repr__(self) -> str:
        return self.__str__()


Node = Union[NumberNode, BinaryOperationNode, VarNode, VarAccessNode, IfNode, VarAssignNode, WhileNode, FunctionNode, CallFunctionNode, ReturnNode]

#########################################
# PARSER
#########################################


# parse :: int, List[Token], List[List[Node]] -> List[List[Node]]
def parse(index: int, tokens: [List[Token]], ast_list: List[List[Node]]) -> List[List[Node]]:
    # Returns a list of ast lists
    result, index = expression(index, tokens)
    new_ast_list = ast_list+[[result]]
    # In case if the code input ends with an if statement (needs further research)
    # This still needs fixing, if statements tend to return index+1 sometimes
    if tokens[index][1] == 'EOF':
        return new_ast_list

    elif tokens[index+1][1] == 'EOF':
        return new_ast_list
    else:
        return parse(index+1, tokens, new_ast_list)


# parse :: int, List[Token], List[str] -> Tuple[int, int]
def addParameters(index: int, tokens: [List[Token]], arg_name_tokens: List[str]) -> Tuple[list, int]:
    # Add all the parameters of a function to a list
    # Check for a comma
    if tokens[index][0] != TokensEnum.TOKEN_COMMA:
        return arg_name_tokens, index
    else:
        # Append the parameter name to the list
        new_arg_name_tokens = arg_name_tokens+[tokens[index+1][1]]
        return addParameters(index+2, tokens, new_arg_name_tokens)


# addFuncBody :: int, List[Token], List[Node] -> Tuple[List[Node], int]
def addFuncBody(index: int, tokens: [List[Token]], body_list: List[Node]) -> Tuple[List[Node], int]:
    # Returns a list of body nodes
    if tokens[index][0] == TokensEnum.TOKEN_END_FUNCTION:
        # return the body list with the next character
        return body_list, index
    expr, new_index = expression(index, tokens)
    new_body_list = body_list+[[expr]]
    # Check for ReturnNode
    if type(expr) == ReturnNode:
        if type(expr.return_value) == CallFunctionNode:
            # Because a CallFunctionNode ends with a ')', the next index will be the character after that
            return addFuncBody(new_index + 1, tokens, new_body_list)
    # Check for VarAssignNode
    if type(expr) == VarAssignNode:
        if type(expr.value) == CallFunctionNode:
            # Because 'if' and 'while' loops have an ending body node, the next index will be the character after that
            return addFuncBody(new_index + 1, tokens, new_body_list)
    if type(expr) == IfNode or type(expr) == WhileNode or type(expr) == CallFunctionNode:
        return addFuncBody(new_index+1, tokens, new_body_list)
    return addFuncBody(new_index, tokens, new_body_list)


# appendelifcases :: int, List[Token], list -> Tuple[List, int]
def appendelifcases(index: int, tokens: [List[Token]], cases: list) -> Tuple[list, int]:
    # Appends the 'else if' cases to a list and returns it
    if tokens[index][0] != TokensEnum.ELSE_IF:
        return cases, index
    condition, then_index = expression(index+1, tokens)
    expr, new_index = expression(then_index+1, tokens)
    new_cases = cases+[(expr, condition)]
    return appendelifcases(new_index, tokens, new_cases)


# if_expr :: int, List[Token] -> Tuple[IfNode, int]
def if_expr(index: int, tokens: [List[Token]]) -> Tuple[IfNode, int]:
    # Returns an IfNode
    cases = []
    else_case = None
    # Get the conditional expression
    condition, then_index = expression(index, tokens)

    # Get the expression after 'DANN'
    expr, tmp_index = expression(then_index+1, tokens)
    cases_expr = cases + [(expr, condition)]
    # Check if a function call has occurred
    if type(expr) != ReturnNode:
        if type(expr.value) == CallFunctionNode:
            elif_index = tmp_index+1
        else:
            elif_index = tmp_index
    else:
        elif_index = tmp_index

    # Check for elif statements
    if tokens[elif_index][0] == TokensEnum.ELSE_IF:
        # Store the 'ANDALS' cases
        cases_expr_andals, new_index = appendelifcases(elif_index, tokens, cases_expr)
        if tokens[new_index][0] == TokensEnum.ELSE:
            else_case, else_index = expression(new_index+1, tokens)
            return IfNode(cases_expr_andals, else_case), else_index
        return IfNode(cases_expr_andals, else_case), new_index
    # Check for else statement
    elif tokens[elif_index][0] == TokensEnum.ELSE:
        else_case, tmp_index = expression(elif_index + 1, tokens)
        if type(else_case) != ReturnNode:
            if type(else_case.value) == CallFunctionNode:
                else_index = tmp_index + 1
            else:
                else_index = tmp_index
        else:
            else_index = tmp_index

        return IfNode(cases_expr, else_case), else_index
    else:
        return IfNode(cases_expr, else_case), elif_index


# while_expr :: int, List[Token] -> Tuple[WhileNode, int]
def while_expr(index: int, tokens: [List[Token]]) -> Tuple[WhileNode, int]:
    # Returns a WhileNode
    # Get the condition
    condition, loop_index = expression(index, tokens)
    body, body_index = expression(loop_index+1, tokens)
    # Check if a function call is made. If so, the next character will be the one after the ')'
    if type(body.value) == CallFunctionNode:
        return WhileNode(condition, body), body_index+1
    return WhileNode(condition, body), body_index


# func_def :: int, List[Token] -> Tuple[FunctionNode, int]
def func_def(index: int, tokens: [List[Token]]) -> Tuple[FunctionNode, int]:
    # Check for function name

    func_name = tokens[index][1]

    arg_name_tokens = []
    # Check for parameter name
    if tokens[index+2][0] == TokensEnum.TOKEN_NAME:
        # Append the parameters to the list
        arg_name_tokens_par = arg_name_tokens+[tokens[index+2][1]]
        # Append other parameters to the list
        new_arg_name_tokens, new_index = addParameters(index+3, tokens, arg_name_tokens_par)
        empty_body_list = []
        body_list, new_index = addFuncBody(new_index+2, tokens, empty_body_list)
        return FunctionNode(func_name, new_arg_name_tokens, body_list), new_index


# factor :: int, List[Token] -> Tuple[Node, int]
def factor(index: int, tokens: [List[Token]]) -> Tuple[Node, int]:
    # The factor is the node that will be used in a term

    # current token
    token = tokens[index]
    # Check for INT or FLOAT
    if token[0] in (TokensEnum.TOKEN_INT, TokensEnum.TOKEN_FLOAT):
        return NumberNode(token), index+1

    # Check for a RETURN
    elif tokens[index][0] == TokensEnum.RETURN:
        expr, new_index = expression(index + 1, tokens)
        return ReturnNode(expr), new_index

    # Check for Var name
    elif tokens[index][0] == TokensEnum.TOKEN_NAME:
        if tokens[index+1][0] != TokensEnum.TOKEN_LPAREN:
            return VarAccessNode(token), index+1
        else:
            # Function call
            # Get the function name token
            function_name = tokens[index]

            # Get the parameters
            arg_tokens = []
            if tokens[index+2][0] == TokensEnum.TOKEN_INT or tokens[index+2][0] == TokensEnum.TOKEN_NAME:
                new_arg_tokens = arg_tokens+[tokens[index+2][1]]
                full_arg_tokens, new_index = addParameters(index+3, tokens, new_arg_tokens)
                return CallFunctionNode(function_name, full_arg_tokens), new_index

    # Check for (
    elif token[0] == TokensEnum.TOKEN_LPAREN:
        expr, new_index = expression(index+1, tokens)
        # Check for )
        if tokens[new_index][0] == TokensEnum.TOKEN_RPAREN:
            return expr, new_index+1

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
        func_definition, new_index = func_def(index+1, tokens)
        return func_definition, new_index


# term :: int, List[token] -> Tuple[Node, int]
def term(index: int, tokens: List[Token]) -> Tuple[Node, int]:
    # A term is a multiply or division binary operation node

    # Get the left side of operation
    left, new_index = factor(index, tokens)
    return binary_operation(factor, (TokensEnum.TOKEN_MULTIPLY, TokensEnum.TOKEN_DIVIDE), left, new_index, tokens)


# arithmic :: int, List[Token] -> Tuple[Node, int]
def arithmic(index: int, tokens: List[Token]) -> Tuple[Node, int]:
    # Arithmic is a plus or minus binary operation node

    # Get the left side of operation
    left, new_index = term(index, tokens)
    return binary_operation(term, (TokensEnum.TOKEN_PLUS, TokensEnum.TOKEN_MINUS), left, new_index, tokens)


# expression :: int, List[Token] -> Tuple[Node, int]
def expression(index: int, tokens: [List[Token]]) -> Tuple[Node, int]:
    # Check for variable declaration
    if tokens[index][0] == TokensEnum.VAR:
        expr, new_index = expression(index+3, tokens)
        var = VarNode(tokens[index+1], expr)
        return var, new_index
    # Check for var assign
    elif tokens[index][0] == TokensEnum.TOKEN_NAME:
        if tokens[index+1][0] != TokensEnum.TOKEN_EQUAL:
            left, new_index = arithmic(index, tokens)
            return binary_operation(arithmic, (TokensEnum.TOKEN_GREATER, TokensEnum.TOKEN_LESSER, TokensEnum.TOKEN_LESSER_EQUAL, TokensEnum.TOKEN_GREATER_EQUAL, TokensEnum.TOKEN_DOUBLE_EQUAL), left, new_index, tokens)
        else:
            expr, new_index = expression(index+2, tokens)
            var = VarAssignNode(tokens[index], expr)
            return var, new_index

    # Get the left side of operation
    left, new_index = arithmic(index, tokens)
    return binary_operation(arithmic, (TokensEnum.TOKEN_GREATER, TokensEnum.TOKEN_LESSER, TokensEnum.TOKEN_LESSER_EQUAL, TokensEnum.TOKEN_GREATER_EQUAL, TokensEnum.TOKEN_DOUBLE_EQUAL), left, new_index, tokens)


# binary_operation :: Callable[[int, List[Token]], Tuple[Node, int]], tuple, Node, int, List[Token] -> Tuple[Node, int]
def binary_operation(func: Callable[[int, List[Token]], Tuple[Node, int]], operations: tuple, left: Node, index: int, tokens: [List[Token]]) -> Tuple[Node, int]:
    # A binary operation is an algorithmic expression

    # Check for end line
    if tokens[index][0] == TokensEnum.ENDE or tokens[index][0] == TokensEnum.TOKEN_END_FUNCTION or tokens[index][0] == TokensEnum.SLA or tokens[index][0] == TokensEnum.NELOHREDEIW:
        return left, index
    elif tokens[index][0] not in operations or index >= len(tokens):
        return left, index
    else:
        operation_token = tokens[index]
        right, new_index = func(index+1, tokens)
        left = BinaryOperationNode(left, operation_token, right)
        return binary_operation(func, operations, left, new_index, tokens)
