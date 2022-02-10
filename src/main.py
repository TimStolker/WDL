from lexer import *

while True:
    text = input('Angry German noises>> ')
    tokens, error = Lexer.run('token.py placeholder', text)
    if error:
        print(error.as_string())
    else:
        print(tokens)
        #for i in tokens:
        #print(i)
