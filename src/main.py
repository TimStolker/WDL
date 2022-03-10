import classlexer
from classparser import *

filename = "codeInput.txt"
f = open(filename, "r")
text = f.read()

commandline = False

if(commandline):
    while True:
        text = input('Input>> ')
        print(classlexer.run('commandline', text))
else:
    print("output: ",classlexer.run(filename, text))
