from Parser import *
from typing import Tuple, Union, Callable, TextIO


def getFuncNameList(index: int, ast: List[List[Node]], func_list: List[str]) -> List[str]:
    if index > len(ast)-1:
        return func_list
    if type(ast[index][0]) == FunctionNode:
        new_func_list = func_list + [".global "+str(ast[index][0].function_name)]
        return getFuncNameList(index + 1, ast, new_func_list)
    return getFuncNameList(index+1, ast, func_list)


def writeList(index: int, file: TextIO, instruction_list: List) -> None:
    if index > len(instruction_list)-1:
        file.write("\n")
        return
    file.write(str(instruction_list[index])+"\n")
    return writeList(index+1, file, instruction_list)

def loadParameters(index: int, node: FunctionNode, func_list: List[str]) -> List[str]:
    if index > len(node.arguments)-1:
        return func_list
    if index == len(node.arguments)-1:
        new_func_list = func_list+["str    r"+str(index)+", [sp]"]
        return loadParameters(index+1, node, new_func_list)
    else:
        new_func_list = func_list + ["str    r" + str(index) + ", [sp, #"+ str(len(node.arguments*4)-(index+1)*4)]
        return loadParameters(index+1, node, new_func_list)



class Compiler:
    def getFuncList(self, index: int, ast_list: List[List[Node]], func_list: List) -> List[str]:
        if index > len(ast_list)-1:
            return func_list
        if type(ast_list[index][0]) == FunctionNode:
            tmp_list = []
            func_list_sp, void_var_list = self.visit(ast_list[index][0], func_list, tmp_list)
            # Append the function operations list to the list
            new_func_list = func_list+func_list_sp
            return self.getFuncList(index+1, ast_list, new_func_list)
        return self.getFuncList(index+1, ast_list, func_list)

    def visit(self, node: Node, var_list: List[Token], func_list: List) -> Tuple[List[str], List[Token]]:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, var_list, func_list)

    def visit_FunctionNode(self, node: FunctionNode, var_list: List[Token], func_list: List[str]) -> Tuple[List[str], List[Token]]:
        # Create the function name
        int_str = str(((len(node.arguments)) * "int,"))
        # Append function name+parameters
        func_list_name = func_list + [str(node.function_name) + "(" + int_str[:-1] + "):"]

        # Create the first line
        func_list_sp = func_list_name + [str("sub    sp, #" + str(len(node.arguments) * 4))]

        # Load parameters
        index = 0
        func_list_par = loadParameters(index, node, func_list_sp)

        return func_list_par, var_list


def run(ast_list: List[List[Node]]):
    empty_func_name_list = []
    index = 0
    head_list = [".cpu cortex-m0", ".text", ".align 4"]
    f = open("output.txt", "w")
    writeList(index, f, head_list)

    func_name_list = getFuncNameList(index, ast_list, empty_func_name_list)
    writeList(index, f, func_name_list)
    empty_func_list = []
    compiler = Compiler()
    func_list = compiler.getFuncList(index, ast_list, empty_func_list)
    writeList(index, f, func_list)


