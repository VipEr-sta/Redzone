import sys
import json
# 1 in argv is the filename of the program to be interpreted
 


filename = sys.argv[1] #helloWorld.rz
print(f"Argument received: {filename}")


full_program = ""

grammer = {
    "statement" :
        ["var_dec", "slice_dec", "if_stmt", "else_if_stmt", "else_stmt",
         "for_loop", "sprint_stmt", "trade_stmt"],

    "var_dec" :
    ["KEYWORD(let)", "IDENTIFIER",
     "EQUALS", "EXPRESSION", "SEMICOLON" ],
    "sprint_stmt" :
    ["KEYWORD(sprint)", "LPAREN", "EXPRESSION", "RPAREN", "SEMICOLON"],





}

#should start empty but then populate with lexer

tokens = [


]
def readProgram():
    full_program = ""
    #create the entire string for the program code
    with open(filename, "r") as file:
        full_program = file.read()
    print(full_program)
    return full_program
    




def lexer(full_program):
    # will return list of the tokens in the program
    tokens = []
    i = 0
    while i < len(full_program):
        token = full_program[i]

        if token.isalpha():
            #check for words
            word = ""
            while i < len(full_program) and full_program[i].isalpha():
                word += full_program[i]
                i += 1
            if word in ["let", "sprint", "if", "else", "trade", "with",
                        "array", "else if", "for", "league", "team" ]:
                tokens.append({"type": "KEYWORD", "value": word})
            elif word == "True" or word == "False":
                tokens.append({"type": "BOOLEAN", "value": word})
            else:
                tokens.append({"type": "IDENTIFIER", "value": word})
        elif token.isdigit():
            #check for numbers
            number = ""
            while i < len(full_program) and full_program[i].isdigit():
                number += full_program[i]
                i += 1
            tokens.append({"type": "NUMBER", "value": int(number)})

        elif not token.isalnum() and not token.isspace():
            #check for symbols
            if token == ";":
                tokens.append({"type": "SEMICOLON", "value": token})

            elif token == "/":
                if i < len(full_program) and full_program[i+1] == "/":
                    while i < len(full_program) and full_program[i] != "\n":
                        i += 1
                else:
                    while i < len(full_program) and full_program[i+1] != "=":
                        tokens.append({"type": "DIV", "value": full_program[i]})
                        i += 1
            elif token == '"':
                string = ""
                i += 1
                while i < len(full_program) and full_program[i] != '"':
                    string += full_program[i]
                    i += 1
                i += 1
                tokens.append({"type": "STRING", "value": string})

            elif token == "(":
                if  i < len (full_program) and full_program[i+1] == "*":
                    while i < len(full_program) and not (full_program[i] == "*" and full_program[i+1] == ")"):
                        i+=1
                    i+=2
                else:
                    tokens.append({"type": "LPAREN", "value": token})
            elif token == ")":
                if i < len(full_program) and full_program[i-1] == "*":
                    i+2
                else:
                    tokens.append({"type": "RPAREN", "value": token})

            elif token == ".":
                tokens.append({"type": "DOT", "value": token})
            elif token =="{":
                tokens.append({"type": "LBRACE", "value": token})
            elif token == "}":
                tokens.append({"type": "RBRACE", "value": token})
            elif token == "[":
                tokens.append({"type": "LBRACKET", "value": token})
            elif token == "]":
                tokens.append({"type": "RBRACKET", "value": token})
            #comparison operators
            elif token == "=":
                if i + 1 < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "EQUALS_EQUALS", "value": token})
                    i+=1
                else:
                    tokens.append({"type": "EQUALS", "value": token})

            elif token == "!":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "NOT_EQUALS", "value": token})
                    i+=1

            elif token == "<":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "LESS_EQUALS", "value": token})
                    i+=1
                else:
                    tokens.append({"type": "LESS_THAN", "value": token})
            elif token == ">":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "GREATER_EQUALS", "value": token})
                    i+=1
                else:
                    tokens.append({"type": "GREATER_THAN", "value": token})
            elif token == "+":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "PLUS_EQUALS", "value": token})
                else:
                    tokens.append({"type": "PLUS", "value": token})
            elif token == "-":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "MINUS_EQUALS", "value": token})
                else:
                    tokens.append({"type": "MINUS", "value": token})
            elif token == "*":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "MULT_EQUALS", "value": token})
                else:
                    tokens.append({"type": "MULT", "value": token})













            i+=1
    
        else:
            
            i += 1
    return tokens



def parse(tokens):
    #parse the tokens and create an AST
    current = 0
    ast = {
        "type": "Program",
        "body": []
    }

    while current < len(tokens):
        token = tokens[current]
        # Check for variable declaration grammar
        # let identifier = number

        if (
                current + 4 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "let" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "EQUALS" and
                tokens[current + 3]["type"] in ["NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"] and
                tokens[current + 4]["type"] == "SEMICOLON"
        ):
            ast["body"].append({
                "type": "VariableDeclaration",
                "name": tokens[current + 1]["value"],
                "value": {
                    "type": "NumberLiteral",
                    "value": tokens[current + 3]["value"]
                }
            })

            current = current + 5




        elif (
                current + 4 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "let" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "EQUALS" and
                tokens[current + 3]["type"] == "STRING" and
                tokens[current + 4]["type"] == "SEMICOLON"

        ):

            ast["body"].append({
                "type": "VariableDeclaration",
                "name": tokens[current + 1]["value"],
                "value": {
                    "type": "StringLiteral",
                    "value": tokens[current + 3]["value"]
                }
            })

            current = current + 5

        elif (
                current + 4 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "let" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "EQUALS" and
                tokens[current + 3]["type"] == "BOOLEAN" and
                tokens[current + 4]["type"] == "SEMICOLON"

        ):


            ast["body"].append({
                "type": "VariableDeclaration",
                "name": tokens[current + 1]["value"],
                "value": {
                    "type": "BooleanLiteral",
                    "value": tokens[current + 3]["value"]
                }
            })

            current = current + 5

        elif (
                current + 3 < len(tokens) and
                tokens[current]["type"] in ["IDENTIFIER", "NUMBER"] and
                tokens[current + 1]["type"] in ["PLUS", "MINUS", "MULT", "DIV"] and
                tokens[current + 2]["type"] in ["IDENTIFIER", "NUMBER"] and
                tokens[current + 3]["type"] == "SEMICOLON"



            ):

                ast["body"].append({
                    "type": "BinaryExpression",
                    "left": { "type": tokens[current]["type"], "value": tokens[current]["value"] },
                    "operator": tokens[current + 1]["value"],
                    "right": {"type": tokens[current + 2]["type"], "value": tokens[current + 2]["value"] }



                })

                current = current + 4


            # Check for sprint statement grammar:
            # sprint ( IDENTIFIER ) ;
        elif (
                current + 4 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "sprint" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] == "RPAREN" and
                tokens[current + 4]["type"] == "SEMICOLON"
        ):
            ast["body"].append({
                "type": "PrintStatement",
                "name": tokens[current + 2]["value"],
                "argument": {
                    "type": "Identifier",
                    "value": tokens[current + 2]["value"]

                }
            })

            current = current + 5
            #creating a league
        elif (
                current + 2 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "league" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "SEMICOLON"
        ):
            ast["body"].append({
                "type": "League_Declaration",
                "name": tokens[current + 1]["value"],


            })

            current = current + 3
        elif (
                current + 4 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "team" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "DOT" and
                tokens[current + 3]["type"] == "IDENTIFIER" and
                tokens[current + 4]["type"] == "SEMICOLON"
        ):

            current = current + 5
            #Conditionals IF STATEMENT: NUM TYPE
        elif (
                current + 5 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "if" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] == "COMPARISON_OPERATIOR" and
                tokens[current + 4]["type"] == "NUMBER" and
                tokens[current + 5]["type"] == "SEMICOLON"

        ):
            current = current + 6
                #IF STATEMENT: STRING TYPE
        elif (
                current + 5 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "if" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] == "COMPARISON_OPERATOR" and
                tokens[current + 4]["type"] == "STRING" and
                tokens[current + 5]["type"] == "SEMICOLON"

        ):
            current = current + 6
                # IF STATEMENT: BOOL TYPE
        elif (

                current + 5 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "if" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] == "BOOLEAN" and
                tokens[current + 4]["type"] == "COMPARISON_OPERATOR" and
                tokens[current + 5]["type"] == "SEMICOLON"

        ):
            current = current + 6


                # If it matches nothing, it is invalid
        else:
                raise ValueError("Syntax error near token " + str(current))

    return ast


def interpreter(ast):
    #will print output to console




    variables = {}
    leagues = {}
    for item in ast["body"]:
        if item["type"] == "VariableDeclaration":
            variables[item["name"]] = item["value"]["value"]
        elif item["type"] == "League_Declaration":
            leagues[item["name"]] = item["name"]
            #print(leagues[item["name"]])
        elif item["type"] == "Team_Declaration":
            pass
        elif item["type"] == "BinaryExpression":
            left = item["left"]["value"] if item["left"]["type"] == "NUMBER" else variables[item["left"]["value"]]
            right = item["right"]["value"] if item["right"]["type"] == "NUMBER" else variables[item["right"]["value"]]
            if item["operator"] == "+":
                variables[item["left"]["value"]] = left + right
                
            elif item["operator"] == "-":
                variables[item["left"]["value"]] = left - right
            
            elif item["operator"] == "*":
                variables[item["left"]["value"]] = left * right
                
            elif item["operator"] == "/":
                variables[item["left"]["value"]] = left / right
                
        elif item["type"] == "PrintStatement":
            print(variables[item["argument"]["value"]])
        
                
            










if __name__ == "__main__":
    full_program = readProgram()
    tokens = lexer(full_program)
    print(tokens)
    ast = parse(tokens)
    #print(json.dumps(ast, indent=2))
    interpreter(ast)

