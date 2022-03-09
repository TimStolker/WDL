from numbers import Real
from classtoken import *


class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def visit_NumberNode(self, node) -> int:
        return node.token[1]

    def visit_BinaryOperationNode(self,node) -> int:
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        if node.operation_token[0] == TokensEnum.TOKEN_PLUS:
            return left+right
        elif node.operation_token[0] == TokensEnum.TOKEN_MINUS:
            return left-right
        elif node.operation_token[0] == TokensEnum.TOKEN_MULTIPLY:
            return left*right
        elif node.operation_token[0] == TokensEnum.TOKEN_DIVIDE:
            if right != 0:
                return left/right
            else:
                raise Exception("Divide by 0 is not possible")
