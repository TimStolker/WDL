from numbers import Real
from classtoken import *
from classparser import *
from typing import Tuple, Union

class Interpreter:
    def visit(self, node: Node, var_list: list) -> int:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, var_list)

    def visit_NumberNode(self, node: NumberNode, var_list: list) -> int:
        return node.token[1]

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, var_list: list) -> int:
        # Check if the node is a variable name
        if type(node.left_node) == VarAccessNode:
            if node.left_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.left_node.token[1]
                index = 0
                # Get the value of the variable
                value = self.searchVarValue(var_list, var_name, index)

                # if the value is a BinaryOperationNode it has to be calculated first
                if type(value) == BinaryOperationNode:
                    value = self.visit(value, var_list)
                    left = value
                else:
                    left = self.visit(value,var_list)
            else:
                left = self.visit(node.left_node, var_list)
        else:
            left = self.visit(node.left_node, var_list)

        if type(node.right_node) == VarAccessNode:
            if node.right_node.token[0] == TokensEnum.TOKEN_NAME:
                var_name = node.right_node.token[1]
                index = 0
                value = self.searchVarValue(var_list, var_name, index)
                if type(value) == BinaryOperationNode:
                    value = self.visit(value, var_list)
                    right = value
                else:
                    right = self.visit(value,var_list)
            else:
                right = self.visit(node.right_node, var_list)
        else:
            right = self.visit(node.right_node, var_list)

        if node.operation_token[0] == TokensEnum.TOKEN_PLUS:
            return left+right
        elif node.operation_token[0] == TokensEnum.TOKEN_MINUS:
            return left-right
        elif node.operation_token[0] == TokensEnum.TOKEN_MULTIPLY:
            return left*right
        elif node.operation_token[0] == TokensEnum.TOKEN_DIVIDE:
            if right != 0:
                return int(left/right)
            else:
                raise Exception("Divide by 0 is not possible")
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER:
            return left>right
        elif node.operation_token[0] == TokensEnum.TOKEN_GREATER_EQUAL:
            return left>=right
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER:
            return left<right
        elif node.operation_token[0] == TokensEnum.TOKEN_LESSER_EQUAL:
            return left<=right
        elif node.operation_token[0] == TokensEnum.TOKEN_DOUBLE_EQUAL:
            return left==right
        else:
            print("token: ", node.operation_token[0])

    def visit_VarNode(self, node: VarNode, var_list: list) -> Node:
        # Appends the var name to the list
        var_list.append(node.name)
        return node

    def visit_IfNode(self, node: IfNode, var_list: list) -> None:
        # Go through every case
        case_index = 0
        expr_value = self.gothroughcases(node, var_list, case_index)
        if expr_value == None:
            if node.else_case:
                else_value = self.visit(node.else_case, var_list)
                return else_value
            else:
                return None
        else:
            return expr_value


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

    def gothroughcases(self, node: IfNode, var_list: list, index:int) -> Union[int, None]:
        if index > len(node.cases)-1:
            return None
        else:
            condition = node.cases[index][0]
            expr = node.cases[index][1]
            condition_value = self.visit(condition, var_list)
            if condition_value == True:
                expr_value = self.visit(expr, var_list)
                return expr_value
            else:
                return self.gothroughcases(node, var_list, index+1)
