import classlexer
from classparser import Parser

filename = "codeInput.txt"
f = open(filename, "r")
text = f.read()

commandline = True

if(commandline):
    while True:
        text = input('Input>> ')
        print(classlexer.run('commandline', text))
else:
    print(classlexer.run(filename, text))
