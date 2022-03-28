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


def getVarSP(index: int, node: Union[VarNode, VarAccessNode, ReturnNode, str], var_list: List[Tuple[str, int]]) -> int:
    if type(node) == VarAccessNode:
        if node.token[1] == var_list[index][0]:
            return var_list[index][1]
    elif type(node) == str:
        if node == var_list[index][0]:
            return var_list[index][1]
    elif type(node) == ReturnNode:
        if node.return_value.token[1] == var_list[index][0]:
            return var_list[index][1]
    elif node.name[1] == var_list[index][0]:
        return var_list[index][1]
    return getVarSP(index+1, node, var_list)


def getArgsList(index: int, node: FunctionNode, var_list: List[Tuple[str, int]]):
    if index > len(node.arguments)-1:
        return var_list
    new_var_list = var_list + [(node.arguments[index], index*4)]
    return getArgsList(index+1, node, new_var_list)


def getVarList(index: int, node: FunctionNode, var_list: List[Tuple[str, int]], sp: int):
    if index > len(node.body)-1:
        return var_list
    elif type(node.body[index][0]) == VarNode:
        new_var_list = var_list+[(node.body[index][0].name[1], sp)]
        return getVarList(index+1, node, new_var_list, sp+4)
    return getVarList(index+1, node, var_list, sp)


def loadArgs(index: int, arg_list: List[Tuple[str, int]], func_list):
    if index > len(arg_list)-1:
        return func_list
    if index == 0:
        new_func_list = func_list + ["str    r"+str(index)+", [sp]"]
        return loadArgs(index+1, arg_list, new_func_list)
    new_func_list = func_list + ["str    r"+str(index)+", [sp, #"+str(index*4)+"]"]
    return loadArgs(index+1, arg_list, new_func_list)


def checkFuncCall(index: int, node: FunctionNode) -> bool:
    if index > len(node.body)-1:
        return False
    if type(node.body[index][0])==ReturnNode:
        if type(node.body[index][0].return_value) == CallFunctionNode:
            return True
    return checkFuncCall(index+1, node)


class Compiler:
    # getFuncList :: int, List[List[Node]], List[str], List[str] -> :List[str]
    def getFuncList(self, index: int, ast_list: List[List[Node]], func_list: List[str]) -> List[str]:
        # Returnes a list of asm-instructions
        if index > len(ast_list)-1:
            return func_list
        if type(ast_list[index][0]) == FunctionNode:
            empty_var_list = []
            call = False
            func_args_list, var_list = self.visit(ast_list[index][0], empty_var_list, func_list, index, call)
            # Append the function operations list to the list
            return self.getFuncList(index+1, ast_list, func_args_list)
        return self.getFuncList(index+1, ast_list, func_list)

    # visit :: Node, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit(self, node: Node, var_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, var_list, func_list, func_num, call)

    # visit_FunctionNode :: FunctionNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_FunctionNode(self, node: FunctionNode, var_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        # Create the function name
        func_list_name = func_list + [str(node.function_name) + ":"]

        # Get arguments list
        tmp = []
        index = 0
        arg_list = getArgsList(index, node, tmp)
        # Get variable list
        var_list = getVarList(index, node, tmp, len(arg_list)*4)

        # Check if a function is called within the function
        if checkFuncCall(index, node):
            trueCall = True
            push_func_list = func_list_name+["push    {r7, lr}"]
            add_func_list = push_func_list+["add    r7, sp, #0"]
            func_list_sub = add_func_list + ["sub    sp, #" + str((len(arg_list) + len(var_list)) * 4)]
            func_args_list = loadArgs(index, arg_list, func_list_sub)
            vars_list = arg_list + var_list
            new_func_list = self.goThroughBody(index, node, vars_list, func_args_list, func_num, trueCall)
            func_args_end = new_func_list + [""]

        else:
            func_list_sub = func_list_name+["sub    sp, #"+str((len(arg_list) + len(var_list))*4)]
            func_args_list = loadArgs(index, arg_list, func_list_sub)

            # Combine arguments and variable lists
            vars_list = arg_list+var_list

            new_func_list = self.goThroughBody(index, node, vars_list, func_args_list, func_num, call)

            func_args_end = new_func_list+[""]
        return func_args_end, var_list

    # visit_VarNode :: VarNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_VarNode(self, node: VarNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        mov_func_list = func_list+["mov    r0, #"+str(node.var_value.token[1])]
        index = 0
        sp = getVarSP(index, node, vars_list)
        if sp == 0:
            str_func_list = mov_func_list+["str    r0, [sp]"]
        str_func_list = mov_func_list+["str    r0, [sp, #"+str(sp)+"]"]
        return str_func_list, vars_list

    # visit_VarAssignNode :: VarAssignNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_VarAssignNode(self, node: VarAssignNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        # Check for NumberNode
        if type(node.value.left_node) == NumberNode:
            left_func_list = func_list+["mov    r0, #"+str(node.value.left_node.token[1])]
        # Else variable
        else:
            index = 0
            sp = getVarSP(index, node.value.left_node, vars_list)
            if sp == 0:
                left_func_list = func_list + ["ldr    r0, [sp]"]
            else:
                left_func_list = func_list + ["ldr    r0, [sp, #"+str(sp)+"]"]

        # Check for NumberNode
        if type(node.value.right_node) == NumberNode:
            right_func_list = left_func_list+["mov    r1, #"+str(node.value.right_node.token[1])]
        # Else variable
        else:
            index = 0
            sp = getVarSP(index, node.value.right_node, vars_list)
            if sp == 0:
                right_func_list = left_func_list + ["ldr    r1, [sp]"]
            else:
                right_func_list = left_func_list + ["ldr    r1, [sp, #"+str(sp)+"]"]

        # Make operation
        if node.value.operation_token[1] == "+":
            op_func_list = right_func_list+["add    r0, r0, r1"]
        elif node.value.operation_token[1] == "-":
            op_func_list = right_func_list + ["sub    r0, r0, r1"]
        elif node.value.operation_token[1] == "*":
            op_func_list = right_func_list + ["mul    r0, r0, r1"]
        # Other operator
        else:
            op_func_list = right_func_list

        index = 0
        sp = getVarSP(index, node.name, vars_list)
        if sp == 0:
            str_func_list = op_func_list+["str    r0, [sp]"]
        else:
            str_func_list = op_func_list+["str    r0, [sp, #"+str(sp)+"]"]
        return str_func_list, vars_list

    # visit_IfNode :: IfNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_IfNode(self, node: IfNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        # Check is left_node is a var
        index = 0
        sp = getVarSP(index, node.cases[0][1].left_node, vars_list)
        if sp == 0:
            ldr_func_list = func_list+["ldr    r0, [sp]"]
        else:
            ldr_func_list = func_list+["ldr    r0, [sp, #"+str(sp)+"]"]

        # Get right node:
        branchtype = ""
        if type(node.cases[0][1].right_node) == NumberNode:
            number = node.cases[0][1].right_node.token[1]
            if node.cases[0][1].operation_token[1] == "<":
                branchtype = "blt"
            elif node.cases[0][1].operation_token[1] == ">":
                branchtype = "bgt"
            elif node.cases[0][1].operation_token[1] == "==":
                branchtype = "beq"
            elif node.cases[0][1].operation_token[1] == ">=":
                branchtype = "bge"
            elif node.cases[0][1].operation_token[1] == "<=":
                branchtype = "ble"

            # Make compare instruction
            cmp_func_list = ldr_func_list+["cmp    r0, #"+str(number)]
            branches = [".LBB" + str(func_num) + "_1", ".LBB" + str(func_num) + "_2"]

            bOP_func_list = cmp_func_list+[branchtype+"    "+branches[0]]
            b_func_list = bOP_func_list+["b    "+branches[1]]+[""]

            # Make the first branch
            branch_list = [branches[0] + ":"]
            empty_func_list = []

            # Get the instructions for the node
            func_list, vars_list = self.visit(node.cases[0][0], vars_list, empty_func_list, func_num, call)
            # Append the instructions to branch_list
            instruction_branch_list = branch_list+func_list
            b_branch_list = instruction_branch_list+["b    "+branches[1]]+[""]

            # Create the second branch name
            second_branch_list = b_branch_list+[branches[1]+":"]
            new_func_list = b_func_list+second_branch_list
            return new_func_list, vars_list

        return func_list, vars_list

    # visit_WhileNode :: WhileNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_WhileNode(self, node: WhileNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        branches = [".LBB"+str(func_num)+"_1", ".LBB"+str(func_num)+"_2", ".LBB"+str(func_num)+"_3"]
        b_func_list = func_list+["b    "+branches[0]]+[""]
        branch1_func_list = b_func_list+[branches[0]+":"]

        # Check is left_node is a var
        index = 0
        sp = getVarSP(index, node.condition_node.left_node, vars_list)
        if sp == 0:
            ldr_func_list = branch1_func_list+["ldr    r0, [sp]"]
        else:
            ldr_func_list = branch1_func_list+["ldr    r0, [sp, #"+str(sp)+"]"]

        # Get right node:
        branchtype = ""
        number = node.condition_node.right_node.token[1]
        if type(node.condition_node.right_node) == NumberNode:
            if node.condition_node.operation_token[1] == "<":
                branchtype = "blt"
            elif node.condition_node.operation_token[1] == ">":
                branchtype = "bgt"
            elif node.condition_node.operation_token[1] == "==":
                branchtype = "beq"
            elif node.condition_node.operation_token[1] == ">=":
                branchtype = "bge"
            elif node.condition_node.operation_token[1] == "<=":
                branchtype = "ble"
        cmp_func_list = ldr_func_list+["cmp    r0, #"+str(number)]
        bOP_func_list = cmp_func_list + [branchtype + "    " + branches[1]]
        return_func_list = bOP_func_list + ["b    " + branches[2]] + [""]

        branch2_func_list = return_func_list+[branches[1]+":"]
        while_func_list, vars_list = self.visit(node.body_node, vars_list, branch2_func_list, func_num, call)
        return_func_list = while_func_list+["b    "+branches[0]]+[""]

        branch3_func_list = return_func_list+[branches[2]+":"]

        return branch3_func_list, vars_list

    # visit_ReturnNode :: ReturnNode, List[Tuple[str, int]], List[str], int, bool -> Tuple[List[str], List[Tuple[str, int]]]
    def visit_ReturnNode(self, node: ReturnNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> Tuple[List[str], List[Tuple[str, int]]]:
        # Return value is a number
        if type(node.return_value) == NumberNode:
            number = node.return_value.token[1]
            mov_func_list = func_list+["mov    r0, #"+str(number)]
            add_func_list = mov_func_list+["add    sp, #"+str(len(vars_list)*4)]
            if call:
                pop_func_list = add_func_list+["pop    {r7, pc}"]
                return pop_func_list, vars_list
            else:
                bx_func_list = add_func_list + ["bx    lr"]
                return bx_func_list, vars_list

        # Return value is a variable
        elif type(node.return_value) == VarAccessNode:
            name = node.return_value.token[1]
            index = 0
            sp = getVarSP(index, name, vars_list)
            if sp == 0:
                ldr_func_list = func_list + ["ldr    r0, [sp]"]
            else:
                ldr_func_list = func_list + ["ldr    r0, [sp, #" + str(sp) + "]"]
            add_func_list = ldr_func_list + ["add    sp, #" + str(len(vars_list) * 4)]
            if call:
                pop_func_list = add_func_list+["pop    {r7, pc}"]
                return pop_func_list, vars_list
            else:
                bx_func_list = add_func_list + ["bx    lr"]
                return bx_func_list, vars_list

        elif type(node.return_value) == CallFunctionNode:
            name = node.return_value.node_to_call[1]
            if len(vars_list) == 1:
                ldr_func_list = func_list + ["ldr    r0, [sp]"]
            else:
                ldr_func_list = func_list + ["ldr    r0, [sp, #" + str(len(vars_list)*4) + "]"]

            # Branch to function
            b_func_list = ldr_func_list+["b    "+str(name)]
            add_func_list = b_func_list + ["add    sp, #" + str(len(vars_list) * 4)]
            pop_func_list = add_func_list + ["pop    {r7, pc}"]
            return pop_func_list, vars_list

        return func_list, vars_list

    # goThroughBody :: int, FunctionNode, List[Tuple[str, int]], List[str], int, bool -> List[str]
    def goThroughBody(self, index: int, node: FunctionNode, vars_list: List[Tuple[str, int]], func_list: List[str], func_num: int, call: bool) -> List[str]:
        # Check for ReturnNode
        if type(node.body[index][0]) == ReturnNode:
            return_func_list, vars_list = self.visit(node.body[index][0], vars_list, func_list, func_num, call)
            return return_func_list

        new_func_list, vars_list = self.visit(node.body[index][0], vars_list, func_list, func_num, call)
        return self.goThroughBody(index+1, node, vars_list, new_func_list, func_num, call)


# run :: List[List[Node]] -> None
def run(ast_list: List[List[Node]]) -> None:
    empty_func_name_list = []
    index = 0
    head_list = [".cpu cortex-m0", ".text", ".align 4"]
    f = open("output.asm", "w")
    writeList(index, f, head_list)

    func_name_list = getFuncNameList(index, ast_list, empty_func_name_list)
    writeList(index, f, func_name_list)
    empty_func_list = []
    compiler = Compiler()
    func_list = compiler.getFuncList(index, ast_list, empty_func_list)
    writeList(index, f, func_list)


