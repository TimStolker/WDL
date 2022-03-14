from numbers import Real
from classtoken import *
from classparser import *
from typing import Tuple, Union

class Interpreter:
    def visit(self, node: Node, var_list: list) -> int:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, var_list)

    def visit_NumberNode(self, node: NumberNode, var_list: list) -> Tuple[int, list]:
        return node.token[1], var_list

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, var_list: list) -> Tuple[int, list]:
        # Check if the node is a variable name
        if type(node.left_node) == VarAccessNode:
            if node.left_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.left_node.token[1]
                index = 0
                # Get the value of the variable
                value = self.searchVarValue(var_list, var_name, index)

                # if the value is a BinaryOperationNode it has to be calculated first
                if type(value) == BinaryOperationNode:
                    value, var_list = self.visit(value, var_list)
                    left = value
                else:
                    left, var_list = self.visit(value,var_list)
            else:
                left, var_list = self.visit(node.left_node, var_list)
        else:
            left, var_list = self.visit(node.left_node, var_list)

        if type(node.right_node) == VarAccessNode:
            if node.right_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.right_node.token[1]
                index = 0
                value = self.searchVarValue(var_list, var_name, index)
                if type(value) == BinaryOperationNode:
                    value, var_list = self.visit(value, var_list)
                    right = value
                else:
                    right, var_list = self.visit(value,var_list)
            else:
                right, var_list = self.visit(node.right_node, var_list)
        else:
            right, var_list = self.visit(node.right_node, var_list)

        if node.operation_token[0] == TokensEnum.TOKEN_PLUS:
            return left+right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_MINUS:
            return left-right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_MULTIPLY:
            return left*right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_DIVIDE:
            if right != 0:
                return int(left/right), var_list
            else:
                raise Exception("Divide by 0 is not possible")
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER:
            return left>right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER_EQUAL:
            return left>=right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER:
            return left<right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER_EQUAL:
            return left<=right, var_list
        elif node.operation_token[0] == TokensEnum.TOKEN_DOUBLE_EQUAL:
            return left==right, var_list
        else:
            print("ERROR with token: ", node.operation_token[0])

    def visit_VarNode(self, node: VarNode, var_list: list) -> Tuple[None, list]:
        # Appends the var name to the list
        var_list.append([node])
        return None, var_list

    def visit_VarAccessNode(self, node: VarAccessNode, var_list: list) -> Tuple[Union[Node, int],list]:
        var_name = node.token[1]
        index = 0
        value = self.searchVarValue(var_list, var_name, index)
        return value, var_list

    def visit_VarAssignNode(self, node: VarAssignNode, var_list: list) -> Tuple[None, list]:
        index = 0
        new_var_list = self.checkAssigned(var_list, node.name, node.value, index)
        return None, new_var_list

    def visit_IfNode(self, node: IfNode, var_list: list) -> Tuple[Union[None,int],list]:
        # Go through every case
        case_index = 0
        expr_value, var_list = self.gothroughcases(node, var_list, case_index)
        # If all the conditions aren't true
        if expr_value == None:
            if node.else_case:
                else_value, var_list = self.visit(node.else_case, var_list)
                return else_value, var_list
            else:
                return None, var_list
        # If a condition is true, but has no return type
        elif expr_value == True:
            return None, var_list
        else:
            return expr_value, var_list

    def checkAssigned(self, var_list: list, var_name: str, value: Node, index: int) -> list:
        if index > len(var_list)-1:
            raise Exception("Var ", var_name, "was never assigned")
        # Variable name has been found in list
        elif var_list[index][0].name[1] == var_name:

            # Calculate the value of the expression
            var_value, var_list = self.visit(value, var_list)

            # Make a NumberNode with the calculated value
            token = (TokensEnum.TOKEN_INT, var_value)
            new_value = NumberNode(token)

            # Assign the new (NumberNode) value
            var_list[index][0].var_value = new_value
            return var_list
        else:
            # Check for the next variable
            return self.checkAssigned(var_list, var_name, value, index+1)

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

    def gothroughcases(self, node: IfNode, var_list: list, index:int) -> Tuple[Union[int, None],list]:
        if index > len(node.cases)-1:
            return False, var_list
        else:
            condition = node.cases[index][1]
            expr = node.cases[index][0]
            condition_value, var_list = self.visit(condition, var_list)
            if condition_value == True:
                if type(expr) == VarAssignNode:
                    expr_value, var_list = self.visit(expr, var_list)
                    return True, var_list
                expr_value, var_list = self.visit(expr, var_list)
                return expr_value, var_list
            else:
                return self.gothroughcases(node, var_list, index+1)
