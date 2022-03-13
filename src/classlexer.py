from classtoken import *
from classparser import *
from classinterpreter import *

#########################################
# LEXER
#########################################


def check_eof(text: str, position: int) -> bool:
    # Check of the current position is still in the text
    return position > len(text) - 1

def next_digit(text: str, position: int, dot_count: int) -> str:
    # Check if the current character is a digit or a dot
    if not check_eof(text, position) and text[position].isdigit() or not check_eof(text, position) and text[position] == '.':
        if text[position] == '.':
            if dot_count == 1:
                raise Exception("Float only has 1 dot")

            dot_count += 1
            return text[position] + next_digit(text, position + 1, dot_count)

        elif text[position].isdigit():
            return text[position] + next_digit(text, position + 1, dot_count)
    return ''

def next_word(text: str, position: int) -> str:
    # Check if the current character is alphabetical
    if not check_eof(text, position) and text[position].isalpha():
        return text[position] + next_word(text, position + 1)
    return ''

def next_token(tokens: list, index: int, text: str, line: int) -> list:
    # Check if the current position in still in the text
    if index > len(text) - 1:
        tokens.append((TokensEnum.TOKEN_EOF, 'EOF'))
        return tokens

    current_char = text[index]

    if current_char.isspace():
        return next_token(tokens, index + 1, text, line)

    elif current_char == '+':
        tokens.append((TokensEnum.TOKEN_PLUS, '+'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '-':
        tokens.append((TokensEnum.TOKEN_MINUS, '-'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '/':
        tokens.append((TokensEnum.TOKEN_DIVIDE, '/'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '*':
        tokens.append((TokensEnum.TOKEN_MULTIPLY, '*'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '(':
        tokens.append((TokensEnum.TOKEN_LPAREN, '('))
        return next_token(tokens, index + 1, text, line)

    elif current_char == ')':
        tokens.append((TokensEnum.TOKEN_RPAREN, ')'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '[':
        tokens.append((TokensEnum.TOKEN_LBRACKET, '['))
        return next_token(tokens, index + 1, text, line)

    elif current_char == ']':
        tokens.append((TokensEnum.TOKEN_RBRACKET, ']'))
        return next_token(tokens, index + 1, text, line)

    elif current_char == '=':
        # Check if the token is '=' or '=='
        if text[index+1] == '=':
            tokens.append((TokensEnum.TOKEN_DOUBLE_EQUAL, '=='))
            return next_token(tokens, index + 2, text, line)
        else:
            tokens.append((TokensEnum.TOKEN_EQUAL, '='))
            return next_token(tokens, index + 1, text, line)

    elif current_char == '>':
        if text[index + 1] == '=':
            tokens.append((TokensEnum.TOKEN_GREATER_EQUAL, '>='))
            return next_token(tokens, index + 2, text, line)
        else:
            tokens.append((TokensEnum.TOKEN_GREATER, '>'))
            return next_token(tokens, index + 1, text, line)

    elif current_char == '<':
        if text[index + 1] == '=':
            tokens.append((TokensEnum.TOKEN_LESSER_EQUAL, '<='))
            return next_token(tokens, index + 2, text, line)
        else:
            tokens.append((TokensEnum.TOKEN_LESSER, '<'))
            return next_token(tokens, index + 1, text, line)

    elif current_char == ',':
        tokens.append((TokensEnum.TOKEN_COMMA, ','))
        return next_token(tokens, index + 1, text, line)

    elif current_char.isdigit():
        digit = current_char + next_digit(text, index + 1, 0)
        index += len(digit)
        # Check for float
        if '.' in digit:
            tokens.append((TokensEnum.TOKEN_FLOAT, float(digit)))
        else:
            tokens.append((TokensEnum.TOKEN_INT, int(digit)))
        return next_token(tokens, index, text, line)

    elif current_char.isalpha():
        letters = current_char + next_word(text, index + 1)
        index += len(letters)

        # Check for var type
        if letters == 'VAR':
            tokens.append((TokensEnum.VAR, letters))
        elif letters == 'ALS':
            tokens.append((TokensEnum.IF, letters))
        elif letters == 'ANDDAN':
            tokens.append((TokensEnum.ELSE_IF, letters))
        elif letters == 'ANDERS':
            tokens.append((TokensEnum.ELSE, letters))
        elif letters == 'DANN':
            tokens.append((TokensEnum.THEN, letters))
        elif letters == 'WAHREND':
            tokens.append((TokensEnum.WHILE, letters))
        elif letters == 'WIEDERHOLEN':
            tokens.append((TokensEnum.LOOP, letters))
        elif letters == 'ß':
            tokens.append((TokensEnum.FUNCTION, letters))
        elif letters == 'ENDE':
            tokens.append((TokensEnum.ENDE, letters))
        elif letters == 'SLA':
            tokens.append((TokensEnum.SLA, letters))
        else:
            # Variable name
            tokens.append((TokensEnum.TOKEN_NAME, letters))
        return next_token(tokens, index, text, line)

    elif current_char == '\n':
        return next_token(tokens, index + 1, text, line + 1)

    else:
        raise Exception("Illegal character: " "'" + current_char + "'" + " at line: " + str(line))



def run(filename: str, text: str) -> list:
    #Identify the tokens
    tokens = []
    tokens = next_token(tokens, 0, text, 0)
    # Make AST
    #parser = Parser(tokens)
    ast_list = []
    ast = parse(0, tokens, ast_list)
    # split vars from list

    index = 0
    vars_list = []
    ast_list = []
    ast_list, vars_list = splitVars(ast, ast_list, vars_list, index)
    print("ast: ", ast_list)
    print("vars: ", vars_list[0][0])
    # Interpreter
    interpreter = Interpreter()
    result_list = []
    #print(ast_list)
    for i in range(len(ast_list)):
        result = interpreter.visit(ast_list[i][0], vars_list)
        result_list.append(result)
    return result_list


def splitVars(ast: list, ast_list: list, vars_list:list, index: int) -> Tuple[list,list]:
    # Splits the variables from the ast list and returns both lists
    if index > len(ast)-1:
        return ast_list, vars_list
    elif type(ast[index][0]) == VarNode:
        vars_list.append([ast[index][0]])
        return splitVars(ast, ast_list, vars_list, index+1)
    else:
        ast_list.append([ast[index][0]])
        return splitVars(ast, ast_list, vars_list, index+1)

