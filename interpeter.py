import sys
import json
# 1 in argv is the filename of the program to be interpreted
 


filename = sys.argv[1] #helloWorld.rz
print(f"Argument received: {filename}")


full_program = ""

grammer = {
    "statement" :
        ["var_dec", "slice_dec", "if_stmt", "else_if_stmt", "else_stmt",
         "for_loop", "sprint_stmt", "trade_stmt", "league", "team", "player"],

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
                        "array", "else if", "for", "league", "team", "player" ]:
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
                    i+=1
                i +=1
                
                tokens.append({"type": "STRING", "value": string})
                continue

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
                    tokens.append({"type": "EQUALS_EQUALS", "value": "=="})
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
            elif token == "%":
                if i < len(full_program) and full_program[i+1] == "=":
                    tokens.append({"type": "MOD_EQUALS", "value": token})
                else:
                    tokens.append({"type": "MOD", "value": token})













            i+=1
    
        else:
            
            i += 1
    return tokens



def parse(tokens):
    #parse the tokens and create an AST
    current = 0
    condition_tokens = []
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
                    "type": tokens[current + 3]["type"],
                    "value": tokens[current + 3]["value"]
                }
            })

            current = current + 5



        elif (
                current + 3 < len(tokens) and
                tokens[current]["type"] in ["IDENTIFIER", "NUMBER", "STRING", "BOOLEAN"] and
                tokens[current + 1]["type"] in ["PLUS", "MINUS", "MULT", "DIV", "MOD"] and
                tokens[current + 2]["type"] in ["IDENTIFIER", "NUMBER", "STRING", "BOOLEAN"] and
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
            
            league_name = tokens[current + 1]["value"]
            team_name = tokens[current + 3]["value"]

            ast["body"].append({
                "type": "Team_Declaration",
                "name": team_name,
                "league": league_name

            })

            current = current + 5
        #Player Declaration:
        elif (
                current + 6 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "player" and
                tokens[current + 1]["type"] == "IDENTIFIER" and
                tokens[current + 2]["type"] == "DOT" and
                tokens[current + 3]["type"] == "IDENTIFIER" and
                tokens[current + 4]["type"] == "DOT" and 
                tokens[current + 5]["type"] == "IDENTIFIER" and
                tokens[current + 6]["type"] == "SEMICOLON"

        ):
            
            league_name = tokens[current + 1]["value"]
            team_name = tokens[current + 3]["value"]
            player_name = tokens[current + 5]["value"]
            ast["body"].append({
                "type": "Player_Declaration",
                "name": player_name,
                "team": team_name,
                "league": league_name

            })
            current = current + 7
         
                #IF STATEMENT


        elif (
                
                current + 6 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "if" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] in ["GREATER_EQUALS", "LESS_EQUALS", "EQUALS_EQUALS", "NOT_EQUALS"] and
                tokens[current + 4]["type"] in ["NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"] and
                tokens[current + 5]["type"] == "RPAREN" and
                tokens[current + 6]["type"] == "LBRACE"

            ):

                condition_tokens.append(tokens[current + 4])
            
                end = current + 7

        

                while end < len(tokens) and tokens[end]["type"] != "RBRACE":
                    end += 1
                
                left_token = tokens[current + 2]
                operator_token = tokens[current + 3]
                right_token = tokens[current + 4]

                body_tokens = tokens[current + 7 :end]
                current = end + 1
                   
                
        
                #need 
                ast["body"].append({
                    "type": "If_Statement",
                    "condition": 
                    {
                        "left": left_token,
                        "operator": operator_token["value"],
                        "right": right_token,
                        "body": body_tokens
                    }

                        


                    
                    })
                
                #ElSE IF STATEMENT:
        elif (
                    current + 8 < len(tokens) and
                    tokens[current]["type"] == "KEYWORD" and
                    tokens[current]["value"] == "else" and
                    tokens[current + 1]["type"] == "KEYWORD" and
                    tokens[current + 1]["value"] == "if" and
                    tokens[current + 2]["type"] == "LPAREN" and
                    tokens[current + 3]["type"] == "IDENTIFIER" and
                    tokens[current + 4]["type"] in ["GREATER_EQUALS", "LESS_EQUALS", "EQUALS_EQUALS", "NOT_EQUALS"] and
                    tokens[current + 5]["type"] in ["NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"] and
                    tokens[current + 6]["type"] == "RPAREN" and
                    tokens[current + 7]["type"] == "LBRACE"
                ):
                    
                    condition_tokens.append(tokens[current + 5])
            
                    end = current + 8

        

                    while end < len(tokens) and tokens[end]["type"] != "RBRACE":
                        end += 1
                
                    left_token = tokens[current + 3]
                    operator_token = tokens[current + 4]
                    right_token = tokens[current + 5]

                    body_tokens = tokens[current + 8 :end]
                    current = end + 1

                    ast["body"].append({
                        "type": "Else_If_Statement",
                        "condition": 
                        {
                            "left": left_token,
                            "operator": operator_token["value"],
                            "right": right_token,
                            "body": body_tokens
                        }

                        


                    
                    })
                # ELSE STATEMENT:
        elif (
                    current + 1 < len(tokens) and
                    tokens[current]["type"] == "KEYWORD" and
                    tokens[current]["value"] == "else" and
                    tokens[current + 1]["type"] == "LBRACE"
                ):
                    end = current + 2
                    while end < len(tokens) and tokens[end]["type"] != "RBRACE":
                        end += 1
                    body_tokens = tokens[current + 2 : end]
                    current = end + 1

                    ast["body"].append({
                        "type": "Else_Statement",
                        "body": body_tokens
                    })
            # FOR LOOP:
        elif (
                current + 15 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "for" and
                tokens[current + 1]["type"] == "LPAREN" and
                tokens[current + 2]["type"] == "KEYWORD" and
                tokens[current + 2]["value"] == "let" and
                tokens[current + 3]["type"] == "IDENTIFIER" and
                tokens[current + 4]["type"] == "EQUALS" and
                tokens[current + 5]["type"] in ["NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"] and
                tokens[current + 6]["type"] == "SEMICOLON" and
                tokens[current + 7]["type"] == "IDENTIFIER" and
                tokens[current + 8]["type"] in ["LESS_EQUALS", "LESS_THAN", "GREATER_EQUALS", "GREATER_THAN", 
                                                "NOT_EQUALS", "EQUALS_EQUALS", "EQUALS"] and
                tokens[current + 9]["type"] in ["NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"] and
                tokens[current + 10]["type"] == "SEMICOLON" and
                tokens[current + 11]["type"] == "IDENTIFIER" and
                tokens[current + 12]["type"] in ["PLUS", "MINUS"] and
                tokens[current + 13]["type"] == "RPAREN" and
                tokens[current + 14]["type"] == "LBRACE"
            ):

                end = current + 15

                while end < len(tokens) and tokens[end]["type"] != "RBRACE":
                    end += 1
                #captures tokens for the initialization, condition, and increment parts of the for loop
                name = tokens[current + 3]["value"]
                value = tokens[current + 5]["value"]
                value_type = tokens[current + 5]["type"]
                left = tokens[current + 7]
                operator = tokens[current + 8]["value"]
                right = tokens[current + 9]
                update_var = tokens[current + 11]
                increment_operator = tokens[current + 12]["value"]
                body_tokens = tokens[current + 15 : end]
                
                current = end + 1

                ast["body"].append({
                    "type": "For_Loop",
                    "declaration": {
                        "type": "VariableDeclaration",
                        "name": name,
                        "value": {
                            "type": value_type,
                            "value": value
                        }
                    },
                    "condition": {
                        "left": left,
                        "operator": operator,
                        "right": right,
                    },
                    "increment": {
                        "variable": update_var,
                        "operator": increment_operator
                    },
                    "body": body_tokens
                })

            
            #Trade Statement:
        elif (
                current + 10 < len(tokens) and
                tokens[current]["type"] == "KEYWORD" and
                tokens[current]["value"] == "trade" and
                tokens[current + 1]["type"] == "LBRACE" and
                tokens[current + 2]["type"] == "IDENTIFIER" and
                tokens[current + 3]["type"] == "DOT" and
                tokens[current + 4]["type"] == "IDENTIFIER" and
                tokens[current + 5]["type"] == "KEYWORD" and
                tokens[current + 5]["value"] == "with" and
                tokens[current + 6]["type"] == "IDENTIFIER" and
                tokens[current + 7]["type"] == "DOT" and
                tokens[current + 8]["type"] == "IDENTIFIER" and
                tokens[current + 9]["type"] == "RBRACE"
                
                

            ):  

            
            team1_type = tokens[current + 2]["type"]
            team1_value = tokens[current + 2]["value"]
            player1_type = tokens[current + 4]["type"]
            player1_value = tokens[current + 4]["value"]
            team2_type = tokens[current + 6]["type"]
            team2_value = tokens[current + 6]["value"]
            player2_type = tokens[current + 8]["type"]
            player2_value = tokens[current + 8]["value"]
            current = current + 10

            ast["body"].append({
                "type": "Trade_Statement",
                "team1": {
                    "type": team1_type,
                    "value": team1_value
                },
                "player1": {
                    "type": player1_type,
                    "value": player1_value
                },
                "team2": {
                    "type": team2_type,
                    "value": team2_value
                },
                "player2": {
                    "type": player2_type,
                    "value": player2_value
                }
            })

                
            





                # If it matches nothing, it is invalid
        else:
                raise ValueError("Syntax error near token " + str(current))

    return ast


def interpreter(ast, variables=None, leagues=None):
    #will print output to console
    

    if variables is None:
        variables = {}
    if leagues is None:
        leagues = {}


    is_if_executed = False
    is_elif_executed = False
    for item in ast["body"]:
        if item["type"] == "VariableDeclaration":
            if item["value"]["type"] == "BOOLEAN":
                variables[item["name"]] = item["value"]["value"]
            elif item["value"]["type"] == "NUMBER":
                variables[item["name"]] = item["value"]["value"]
            elif item["value"]["type"] == "STRING":
                variables[item["name"]] = item["value"]["value"]
            elif item["value"]["type"] == "IDENTIFIER":
                variables[item["name"]] = variables[item["value"]["value"]]
            else:
                variables[item["name"]] = item["value"]["value"]
        elif item["type"] == "League_Declaration":
            leagues[item["name"]] = item["name"]
            #print(leagues[item["name"]])

        
        elif item["type"] == "Team_Declaration":
            league_name = item["league"]
            team_name = item["name"]
            if league_name in leagues:
                if league_name not in variables:
                    variables[league_name] = {}
                variables[league_name][team_name] = []
            else:
                raise ValueError("League does not exist: " + league_name)
        elif item["type"] == "Player_Declaration":
            #Player Must be on a team
            league_name = item["league"]
            team_name = item["team"]
            player_name = item["name"]
            if league_name in leagues:
                if league_name not in variables:
                    variables[league_name] = {}
                if team_name not in variables[league_name]:
                    variables[league_name][team_name] = []
                variables[league_name][team_name].append(player_name)
            else:
                raise ValueError("League does not exist: " + league_name)
        elif item["type"] == "Trade_Statement":
            team1 = item["team1"]["value"]
            player1 = item["player1"]["value"]
            team2 = item["team2"]["value"]
            player2 = item["player2"]["value"]
            
            #find the teams and players in the variables and trade them
            #league is already checked in the player declaration, so we can assume the league exists
            team1_found = False
            team2_found = False
            for league in variables:
                if team1 in variables[league]:
                    if player1 in variables[league][team1]:
                        team1_found = True
                        variables[league][team1].remove(player1)
                        print(f"Traded {player1} from {team1} to {team2}")
                    else:
                        raise ValueError("Player " + player1 + " not found on team " + team1)
                if team2 in variables[league]:
                    if player2 in variables[league][team2]:
                        team2_found = True
                        variables[league][team2].remove(player2)
                        print(f"Traded {player2} from {team2} to {team1}")
                    else:
                        raise ValueError("Player " + player2 + " not found on team " + team2)

                
        elif item["type"] == "BinaryExpression":

            if item["left"]["type"] == "IDENTIFIER":
                left = variables[item["left"]["value"]]
            elif item["left"]["type"] == "NUMBER":
                left = item["left"]["value"]
            elif item["left"]["type"] == "STRING":
                left = item["left"]["value"]
            elif item["left"]["type"] == "BOOLEAN":
                left = item["left"]["value"]
            else:
                raise ValueError("Operand Intercepted!: " + item["left"]["type"])

            if item["right"]["type"] == "IDENTIFIER":
                right = variables[item["right"]["value"]]
            elif item["right"]["type"] == "NUMBER":
                right = item["right"]["value"]
            elif item["right"]["type"] == "STRING":
                right = item["right"]["value"]
            elif item["right"]["type"] == "BOOLEAN":
                right = item["right"]["value"] == "True" 
            else:
                raise ValueError("Operand Intercepted!: " + item["right"]["type"])
            
            
            if item["operator"] == "+":

                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    variables[item["left"]["value"]] = left + right
                elif isinstance(left, str) and isinstance(right, str):
                    variables[item["left"]["value"]] = left + right
                else:
                    raise ValueError("What an awful throw!: " + str(left) + " and " + str(right))
                
                
                
            elif item["operator"] == "-":
                variables[item["left"]["value"]] = left - right
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    variables[item["left"]["value"]] = left - right
                else:
                    raise ValueError("What an awful throw!: " + str(left) + " and " + str(right))
                
                
            
            elif item["operator"] == "*":
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    variables[item["left"]["value"]] = left * right
                else:
                    raise ValueError("What an awful throw!: " + str(left) + " and " + str(right))

                

                
            elif item["operator"] == "/":
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if right == 0:
                        raise ValueError("Division by zero error!")
                    variables[item["left"]["value"]] = left / right
            elif item["operator"] == "%":
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if right == 0:
                        raise ValueError("Modulo by zero error!")
                    variables[item["left"]["value"]] = left % right
                else:
                    raise ValueError("What an awful throw!: " + str(left) + " and " + str(right))
                
        elif item["type"] == "PrintStatement":
            print(variables[item["argument"]["value"]])

        elif item["type"] == "If_Statement":
            condition = item["condition"]
            left = None
            right = None
            if condition["left"]["type"] == "IDENTIFIER":
                left = variables[condition["left"]["value"]]
            elif condition["left"]["type"] == "NUMBER":
                left = condition["left"]["value"]
            elif condition["left"]["type"] == "STRING":
                left = condition["left"]["value"]
            elif condition["left"]["type"] == "BOOLEAN":
                left = condition["left"]["value"]
            else:
                raise ValueError("Operand Intercepted!: " + condition["left"]["type"])

            if condition["right"]["type"] == "IDENTIFIER":
                right = variables[condition["right"]["value"]]
            elif condition["right"]["type"] == "NUMBER":
                right = condition["right"]["value"]
            elif condition["right"]["type"] == "STRING":
                right = condition["right"]["value"]
            elif condition["right"]["type"] == "BOOLEAN":
                right = condition["right"]["value"] == "True" 
            else:
                raise ValueError("Operand Intercepted!: " + condition["right"]["type"])
            
            operator = condition["operator"]

            if operator == "==":
                if left == right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
            elif operator == "!=":
                if left != right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
            elif operator == "<":
                if left < right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
            elif operator == "<=":
                if left <= right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
            elif operator == ">":
                if left > right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
            elif operator == ">=":
                if left >= right:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_if_executed = True
                else:
                    is_if_executed = False
        elif item["type"] == "Else_If_Statement":
            condition = item["condition"]
            left = None
            right = None
            if condition["left"]["type"] == "IDENTIFIER":
                left = variables[condition["left"]["value"]]
            elif condition["left"]["type"] == "NUMBER":
                left = condition["left"]["value"]
            elif condition["left"]["type"] == "STRING":
                left = condition["left"]["value"]
            elif condition["left"]["type"] == "BOOLEAN":
                left = condition["left"]["value"]
            else:
                raise ValueError("Operand Intercepted!: " + condition["left"]["type"])

            if condition["right"]["type"] == "IDENTIFIER":
                right = variables[condition["right"]["value"]]
            elif condition["right"]["type"] == "NUMBER":
                right = condition["right"]["value"]
            elif condition["right"]["type"] == "STRING":
                right = condition["right"]["value"]
            elif condition["right"]["type"] == "BOOLEAN":
                right = condition["right"]["value"] == "True" 
            else:
                raise ValueError("Operand Intercepted!: " + condition["right"]["type"])
            
            operator = condition["operator"]

            if operator == "==":
                if left == right and not is_if_executed:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_elif_executed = True
                else:
                    is_elif_executed = False
            elif operator == "!=":
                if left != right and not is_if_executed:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_elif_executed = True
                else:
                    is_elif_executed = False
            elif operator == "<":
                if left < right and not is_if_executed:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_elif_executed = True
                else:
                    is_elif_executed = False
            elif operator == "<=":
                if left <= right and not is_if_executed:
                    body_ast = parse(item["condition"]["body"])
                    interpreter(body_ast, variables, leagues)
                    is_elif_executed = True
                else:
                    is_elif_executed = False
        
        elif item["type"] == "Else_Statement":
            if not is_if_executed and not is_elif_executed:
                body_ast = parse(item["body"])
                interpreter(body_ast, variables, leagues)
            else:
                pass
        

        #Starting to get for loop
        #at the moment only supports for (let Identifier = NUMBER;
        #Only going to impliment the for loop with a variable declaration in the initialization, but it can be expanded later to support more complex initialization statements
        elif item["type"] == "For_Loop":
            loop_variable = item["declaration"]["name"]
            loop_variable_value = item["declaration"]["value"]["value"]

            variables[loop_variable] = loop_variable_value

            print(f"Entering for loop with {loop_variable} = {variables[loop_variable]}")
            left = None
            right = None
            condition = item["condition"]
            if condition["left"]["type"] == "IDENTIFIER":
                left = variables[condition["left"]["value"]]
            else:
                raise ValueError("Operand Intercepted!: " + condition["left"]["type"])
            if condition["right"]["type"] == "NUMBER":
                right = condition["right"]["value"]
            elif condition["right"]["type"] == "IDENTIFIER":
                right = variables[condition["right"]["value"]]
            else:
                raise ValueError("Operand Intercepted!: " + condition["right"]["type"])
            if condition["operator"] == "<":
                while left < right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            if condition["operator"] == "<=":
                while left <= right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            if condition["operator"] == ">":
                while left > right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            if condition["operator"] == ">=":
                while left >= right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            if condition["operator"] == "==":
                while left == right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            if condition["operator"] == "!=":
                while left != right:
                    body_ast = parse(item["body"])
                    interpreter(body_ast, variables, leagues)
                    left = variables[condition["left"]["value"]]
                    if item["increment"]["operator"] == "+":
                        variables[item["increment"]["variable"]["value"]] += 1
                    elif item["increment"]["operator"] == "-":
                        variables[item["increment"]["variable"]["value"]] -= 1
            
            
            


        







if __name__ == "__main__":
    full_program = readProgram()
    tokens = lexer(full_program)
    print(tokens)
    print(tokens[8])
    ast = parse(tokens)
    #print(json.dumps(ast, indent=2))
    interpreter(ast)

