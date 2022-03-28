import Lexer

filename = "codeInput.txt"
f = open(filename, "r")
text = f.read()

Lexer.run(text)
