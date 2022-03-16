from numbers import Real
from classtoken import *
from classparser import *
from typing import Tuple, Union
import sys

sys.setrecursionlimit(1000000)


class Interpreter:
    def visit(self, node: Node, var_list: list, func_list: list) -> int:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, var_list, func_list)

    def visit_NumberNode(self, node: NumberNode, var_list: list, func_list: list) -> Tuple[int, list, list]:
        return node.token[1], var_list, func_list

    def visit_ReturnNode(self, node: ReturnNode, var_list: list, func_list: list) -> Tuple[int, list, list]:
        expr = node.return_value
        expr_value, var_list, func_list = self.visit(expr, var_list, func_list)
        if type(expr_value) == NumberNode:
            return expr_value.token[1], var_list, func_list

        return expr_value, var_list, func_list

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, var_list: list, func_list: list) -> Tuple[int, list, list]:
        # Check if the node is a variable name
        if type(node.left_node) == VarAccessNode:
            if node.left_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.left_node.token[1]
                index = 0
                # Get the value of the variable
                value = self.searchVarValue(var_list, var_name, index)

                # if the value is a BinaryOperationNode it has to be calculated first
                if type(value) == BinaryOperationNode:
                    value, var_list, func_list = self.visit(value, var_list, func_list)
                    left = value
                else:
                    left, var_list, func_list = self.visit(value,var_list, func_list)
            else:
                left, var_list, func_list = self.visit(node.left_node, var_list, func_list)
        else:
            left, var_list, func_list = self.visit(node.left_node, var_list, func_list)

        if type(node.right_node) == VarAccessNode:
            if node.right_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.right_node.token[1]
                index = 0
                value = self.searchVarValue(var_list, var_name, index)
                if type(value) == BinaryOperationNode:
                    value, var_list, func_list = self.visit(value, var_list, func_list)
                    right = value
                else:
                    right, var_list, func_list = self.visit(value,var_list, func_list)
            else:
                right, var_list, func_list = self.visit(node.right_node, var_list, func_list)
        else:
            right, var_list, func_list = self.visit(node.right_node, var_list, func_list)

        if node.operation_token[0] == TokensEnum.TOKEN_PLUS:
            return left+right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_MINUS:
            return left-right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_MULTIPLY:
            return left*right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_DIVIDE:
            if right != 0:
                return int(left/right), var_list, func_list
            else:
                raise Exception("Divide by 0 is not possible")
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER:
            return left>right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER_EQUAL:
            return left>=right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER:
            return left<right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER_EQUAL:
            return left<=right, var_list, func_list
        elif node.operation_token[0] == TokensEnum.TOKEN_DOUBLE_EQUAL:
            return left==right, var_list, func_list
        else:
            raise Exception("ERROR with token: ", node.operation_token[0])

    def visit_VarNode(self, node: VarNode, var_list: list, func_list: list) -> Tuple[None, list, list]:
        # Appends the var name to the list
        new_var_list = var_list+[[node]]
        return None, new_var_list, func_list

    def visit_VarAccessNode(self, node: VarAccessNode, var_list: list, func_list: list) -> Tuple[Union[Node, int],list, list]:
        var_name = node.token[1]
        index = 0
        value = self.searchVarValue(var_list, var_name, index)
        return value, var_list, func_list

    def visit_VarAssignNode(self, node: VarAssignNode, var_list: list, func_list: list) -> Tuple[None, list, list]:
        index = 0
        new_var_list = self.checkAssigned(var_list, func_list, node.name, node.value, index)
        return None, new_var_list, func_list

    def visit_IfNode(self, node: IfNode, var_list: list, func_list: list) -> Tuple[Union[None,int, ReturnNode],list, list]:
        # Go through every case
        case_index = 0
        expr_value, var_list, return_node = self.gothroughcases(node, var_list, func_list, case_index)
        # If all the conditions aren't true
        if expr_value == None:
            if node.else_case:
                else_value, var_list, func_list = self.visit(node.else_case, var_list, func_list)
                print("else case: ", else_value)
                return else_value, var_list, func_list
            else:
                return None, var_list, func_list
        # If a condition is true, but has no return type
        elif expr_value == True:
            return return_node, var_list, func_list
        else:
            if node.else_case:
                print("hier", type(node.else_case))
                if type(node.else_case) == ReturnNode:
                    return node.else_case, var_list, func_list
                else_value, var_list, func_list = self.visit(node.else_case, var_list, func_list)
                return else_value, var_list, func_list
            return expr_value, var_list, func_list

    def visit_WhileNode(self, node: WhileNode, var_list: list, func_list: list) -> Tuple[None,list, list]:
        var_list = self.loopNode(node, var_list, func_list)
        return None, var_list, func_list

    def visit_FunctionNode(self, node: FunctionNode, var_list: list, func_list: list) -> Tuple[Union[None,int], list, list]:
        # Get the function name
        function_name = node.function_name

        # Get the body of the function
        body_node_list = node.body

        # Get the arguments of the function
        arg_names = node.arguments

        # Add the function to the function list
        new_func_list = func_list + [[function_name, body_node_list, arg_names]]
        return None, var_list, new_func_list

    def visit_CallFunctionNode(self, node: CallFunctionNode, var_list: list, func_list: list) -> Tuple[Union[None,int], list, list]:
        # Get the function name
        func_call_name = node.node_to_call
        index = 0

        # Get the function node with that name
        function_node = self.getFuncNode(index, func_call_name, func_list)

        empty_function_var_list = []
        # Make a new var list for this function only
        function_var_list = self.getFuncVarList(index, node.arguments, function_node[2], var_list, empty_function_var_list)

        # Go though the body and execute every line until the word 'result' shows up, then return the value after result
        result, new_function_var_list = self.goThroughBody(index, function_node, function_var_list, func_list)

        # Return the result value with the global variable list and function list
        return result, var_list, func_list

    def goThroughBody(self, index: int, function_node: FunctionNode, var_list: list, func_list: list):
        if index > len(function_node[1]):
            raise Exception("No 'return' found")
        else:
            # Check voor ReturnNode
            if type(function_node[1][index][0]) == ReturnNode:
                expr = function_node[1][index][0]
                expr_value, var_list, func_list = self.visit(expr, var_list, func_list)
                return expr_value, var_list
            else:
                void_return, var_list, void_func = self.visit(function_node[1][index][0], var_list, func_list)
                # Check if a ReturnNode was found in the if statements
                if type(void_return) == ReturnNode:
                    expr_value, var_list, func_list = self.visit(void_return, var_list, func_list)
                    return expr_value, var_list
                return self.goThroughBody(index+1, function_node, var_list, func_list)

    def getFuncVarList(self, index: int, callArgsList: list, funcArgsList: list, var_list: list, func_var_list: list ):
        if index > len(callArgsList)-1:
            return func_var_list
        var_name = callArgsList[index]
        tmp_index = 0
        var_value = self.searchVarValue(var_list, var_name, tmp_index)

        name_token = (TokensEnum.TOKEN_NAME, funcArgsList[index])
        node_var = VarNode(name_token, var_value)
        new_func_var_list = func_var_list + [[(node_var)]]
        return self.getFuncVarList(index+1, callArgsList, funcArgsList, var_list, new_func_var_list)

    def getFuncNode(self, index: int, func_name: Token, func_list: list):
        if index > len(func_list)-1:
            raise Exception("No function with name: ", func_name[1])
        if func_name[1] == func_list[index][0]:
            return func_list[index]
        else:
            return self.getFuncNode(index+1, func_name, func_list)

    def loopNode(self, node: WhileNode, var_list: list, func_list: list) -> list:
        condition, var_list, func_list = self.visit(node.condition_node, var_list, func_list)
        if condition != True:
            return var_list
        else:
            void_value, var_list, func_list = self.visit(node.body_node, var_list, func_list)
            return self.loopNode(node, var_list, func_list)

    def checkAssigned(self, var_list: list, func_list: list, var_name: str, value: Node, index: int) -> list:
        if index > len(var_list)-1:
            raise Exception("Var ", var_name, "was never assigned")
        # Variable name has been found in list
        elif var_list[index][0].name[1] == var_name:

            # Calculate the value of the expression
            var_value, var_list, func_list = self.visit(value, var_list, func_list)

            # Make a NumberNode with the calculated value
            token = (TokensEnum.TOKEN_INT, var_value)
            new_value = NumberNode(token)

            # Assign the new (NumberNode) value
            var_list[index][0].var_value = new_value
            return var_list
        else:
            # Check for the next variable
            return self.checkAssigned(var_list, func_list, var_name, value, index+1)

    def searchVarValue(self, var_list: list, var_name: str, index: int) -> Node:
        # Searches the value of a given variable name
        if index > len(var_list)-1:
            raise Exception("Var ", var_name, " was never assigned")
        # Check if the var_name is the same as the one in the list
        elif var_list[index][0].name[1] == var_name:
            # Return the value
            if type(var_list[index][0]) == VarNode:
                return var_list[index][0].var_value
            else:
                return var_list[index][0].var_value.token[1]
        else:
            return self.searchVarValue(var_list, var_name, index+1)

    def gothroughcases(self, node: IfNode, var_list: list, func_list: list, index:int) -> Tuple[Union[int, None],list, Union[ReturnNode,None]]:
        if index > len(node.cases)-1:
            return False, var_list, None
        else:
            condition = node.cases[index][1]
            expr = node.cases[index][0]
            condition_value, var_list, func_list = self.visit(condition, var_list, func_list)
            if condition_value == True:
                # Check for VarAssignNode
                if type(expr) == VarAssignNode:
                    expr_value, var_list, func_list = self.visit(expr, var_list, func_list)
                    return True, var_list, None
                # Else, it's a return node
                return True, var_list, node.cases[index][0]
            else:
                return self.gothroughcases(node, var_list, func_list, index+1)
