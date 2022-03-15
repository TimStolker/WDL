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
        return tokens+[(TokensEnum.TOKEN_EOF, 'EOF')]

    current_char = text[index]

    if current_char.isspace():
        return next_token(tokens, index + 1, text, line)

    elif current_char == '+':
        return next_token(tokens+[(TokensEnum.TOKEN_PLUS, '+')], index + 1, text, line)

    elif current_char == '-':
        return next_token(tokens+[(TokensEnum.TOKEN_MINUS, '-')], index + 1, text, line)

    elif current_char == '/':
        return next_token(tokens+[(TokensEnum.TOKEN_DIVIDE, '/')], index + 1, text, line)

    elif current_char == '*':
        return next_token(tokens+[(TokensEnum.TOKEN_MULTIPLY, '*')], index + 1, text, line)

    elif current_char == '(':
        return next_token(tokens+[(TokensEnum.TOKEN_LPAREN, '(')], index + 1, text, line)

    elif current_char == ')':
        return next_token(tokens+[(TokensEnum.TOKEN_RPAREN, ')')], index + 1, text, line)

    elif current_char == '[':
        return next_token(tokens+[(TokensEnum.TOKEN_LBRACKET, '[')], index + 1, text, line)

    elif current_char == ']':
        return next_token(tokens+[(TokensEnum.TOKEN_RBRACKET, ']')], index + 1, text, line)

    elif current_char == '=':
        # Check if the token is '=' or '=='
        if text[index+1] == '=':
            return next_token(tokens+[(TokensEnum.TOKEN_DOUBLE_EQUAL, '==')], index + 2, text, line)
        else:
            return next_token(tokens+[(TokensEnum.TOKEN_EQUAL, '=')], index + 1, text, line)

    elif current_char == '>':
        if text[index + 1] == '=':
            return next_token(tokens+[(TokensEnum.TOKEN_GREATER_EQUAL, '>=')], index + 2, text, line)
        else:
            return next_token(tokens+[(TokensEnum.TOKEN_GREATER, '>')], index + 1, text, line)

    elif current_char == '<':
        if text[index + 1] == '=':
            return next_token(tokens+[(TokensEnum.TOKEN_LESSER_EQUAL, '<=')], index + 2, text, line)
        else:
            return next_token(tokens+[(TokensEnum.TOKEN_LESSER, '<')], index + 1, text, line)

    elif current_char == ',':
        return next_token(tokens+[(TokensEnum.TOKEN_COMMA, ',')], index + 1, text, line)

    elif current_char == '{':
        return next_token(tokens + [(TokensEnum.TOKEN_BEGIN_FUNCTION, '{')], index + 1, text, line)
    elif current_char == '}':
        return next_token(tokens + [(TokensEnum.TOKEN_END_FUNCTION, '}')], index + 1, text, line)

    elif current_char.isdigit():
        digit = current_char + next_digit(text, index + 1, 0)
        # Check for float
        if '.' in digit:
            return next_token(tokens+[(TokensEnum.TOKEN_FLOAT, float(digit))], index+len(digit), text, line)
        else:
            return next_token(tokens + [(TokensEnum.TOKEN_INT, int(digit))], index + len(digit), text, line)

    elif current_char.isalpha():
        letters = current_char + next_word(text, index + 1)

        # Check for var type
        if letters == 'VAR':
            return next_token(tokens+[(TokensEnum.VAR, letters)], index+len(letters), text, line)
        elif letters == 'ALS':
            return next_token(tokens + [(TokensEnum.IF, letters)], index + len(letters), text, line)
        elif letters == 'ANDALS':
            return next_token(tokens + [(TokensEnum.ELSE_IF, letters)], index + len(letters), text, line)
        elif letters == 'ANDERS':
            return next_token(tokens + [(TokensEnum.ELSE, letters)], index + len(letters), text, line)
        elif letters == 'DANN':
            return next_token(tokens + [(TokensEnum.THEN, letters)], index + len(letters), text, line)
        elif letters == 'WAHREND':
            return next_token(tokens + [(TokensEnum.WHILE, letters)], index + len(letters), text, line)
        elif letters == 'WIEDERHOLEN':
            return next_token(tokens + [(TokensEnum.LOOP, letters)], index + len(letters), text, line)
        elif letters == 'FUNKTION':
            return next_token(tokens + [(TokensEnum.FUNCTION, letters)], index + len(letters), text, line)
        elif letters == 'ENDE':
            return next_token(tokens + [(TokensEnum.ENDE, letters)], index + len(letters), text, line)
        elif letters == 'SLA':
            return next_token(tokens + [(TokensEnum.SLA, letters)], index + len(letters), text, line)
        elif letters == 'NELOHREDEIW':
            return next_token(tokens + [(TokensEnum.NELOHREDEIW, letters)], index + len(letters), text, line)
        elif letters == 'RETURN':
            return next_token(tokens + [(TokensEnum.RETURN, letters)], index + len(letters), text, line)
        else:
            # Variable name
            return next_token(tokens + [(TokensEnum.TOKEN_NAME, letters)], index + len(letters), text, line)

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

    # Interpreter
    interpreter = Interpreter()
    vars_list = []
    func_list = []
    result_list = []
    for i in range(len(ast)):
        result, vars_list, func_list = interpreter.visit(ast[i][0], vars_list, func_list)
        #print("vars: ", vars_list)
        #print("func: ", func_list)
        if result != None:
            result_list.append(result)

    return result_list

