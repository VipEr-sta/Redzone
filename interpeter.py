import sys

filename = sys.argv[1] #helloWorld.rz


full_program = ""
#create the entire string for the program code
with open(filename, "r") as file:
    full_program = file.read()



print(full_program)