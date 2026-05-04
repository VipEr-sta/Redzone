# Redzone

![](redzone_logo.png)

Redzone is a DSL(domain-specific language) used for the purpose of creating and managing fantasy football teams. It lets the developer create leagues, teams, and players, where one can trade players from different teams. These players are measured based on points, which comes from yards and touchdowns. Player points contribute to overall team points. It accomplishes this using dot-scoping, stat-access declaration, and football-themed error messages. 


Example code: 
```javascript
league myLeague;
// Creating league
team myLeague.myTeam;
// creating teams and players
player myLeague.myTeam.myPlayer;
player myLeague.team1.player1;
player myLeague.team2.player2;

let my_score = myLeague.myTeam.myPlayer.points;
(*
comparing points of players on separate teams

*)

if (myLeague.myTeam.myPlayer.points > myLeague.team1.player1.points) {
    trade {
        myTeam.myPlayer with team2.player2;
    }
}

else {
    sprint("Your player is doing excellent this season!");
}


```


EBNF Rules:

```
 

var_dec = "let", identifier, "=" , expression; 

literal = digit, {digit} | '"', {character}, '"'; 

if_stmt = “if”, “(“, expression, “)” , “{“, {statement}, “}” ; 

 

single_line_comment  = “//”, {character}, newline; 

 

mult_line_comment = “(*”, {character}, “*)”; 

 

for_loop = “for”, “(“ , var_dec, ";" , expression, “;”,  assignment, “)”, “{“, {statement}, “}”; 

 

letter = "A" | "B" | "C" | "D" | "E" | "F" | "G" 
      | "H" | "I" | "J" | "K" | "L" | "M" | "N" 
      | "O" | "P" | "Q" | "R" | "S" | "T" | "U" 
      | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" 
      | "c" | "d" | "e" | "f" | "g" | "h" | "i" 
      | "j" | "k" | "l" | "m" | "n" | "o" | "p" 
      | "q" | "r" | "s" | "t" | "u" | "v" | "w" 
      | "x" | "y" | "z" ; 

 

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ; 

 

identifier = letter, { letter | digit | “_” } ; 

 

white_space = ? white space characters ?; 

 

else_stmt = “else”, “{“, {statement}, “}”; 

 

else_if_stmt = “else”, white_space, “if”, “(“, expression, “)” , “{“, {statement}, “}” ; 

 

 

player = “player”, identifier, “.”, identifier, “.” , identifier,“;”; 

 

 

team = “team” , identifier, “.” , identifier,“;” ; 

 

 

league = “league”, identifier, “;”; 

 

slice_dec = “array”, identifier, “=”, “[“, expression, “]”, “;”; 

 

trade_stmt= “trade” , “{“, scoped_identifier_for_trades , “with”, scoped_identifier_for_trades, “}“, “;”; 

scoped_identifier = identifier, “.”, identifier, “.”, identifier; 

scoped_identifier_for_trades= identifier, “.”, identifier; 

 

stat_access = scoped_identifier, “.”, identifier, “;”; 

 

sprint_stmt = “sprint”, “(“, expression, “)”, “;”; 

 

statement = var_dec | if_stmt | else_if_stmt| else_stmt | for_loop | sprint_stmt | trade_stmt | slice_dec;

comp_operators = "==" | "!=" | "<=" | ">=" | "+=" | "-=" | "*=" | "/=";

expression = identifier | literal | expression, operator, expression;

operators = "=" | "+" | "-" | "*" | "/";

 
```

| Feature | Keyword | Example|
|---------|---------|--------|
| Variable | `let` | `let x = 5;` |
| Sprint | `sprint` | `sprint("Hi");` |
|If Statement | `if` | `if (x == 5) {x + 1;}`|
|Else Statement | `else` | `else {x-1;}`|
|Else If Statement | `else if` | `else if (x == 4) {x+2;}` |
| For Loop | `for` | `for (let i=0; i > 5; i+1) {x+5}` |
| Single Line Comment | `//` | `// Single Line comment here` |
| Multi Line Comment | `(* *)` | `(* Multi Line comment here *)` |
| Player | `player` | `player league1.team1.player1;` |
| Team | `team` | `team league1.team1;` |
| League | `league` | `league league1;` |
| Slice | `array` | `array amount = [5,6,7];` |
| Trade Statement | `trade...with` | `trade {team.player with team1.player1;}` |
| Scoped Itentifier | `.` | `player myleague.myteam.myplayer;` |
| Stats | `.points, .yards, .touchdowns` | `sprint(league.team.player.points);` |
| Comparision Operators | `==, !=, etc` | `if (x != 10) {x = 0;}`
| Operators | `=, +, -, etc` | `y = 5 + 5;` |

1. What works:
   1. Variable
   2. Sprint
   3. If Statement
   4. Else If Statement
   5. Else Statement
   6. For Loop
   7. Single Lie Comment
   8. Multiline Comment
   9. Player
   10. Team
   11. League
   12. Trade Statement
   13. Scoped Identifier
   14. Comparison Operators
   15. Operators
       
1. What doesn't work:
   1. Slice
   2. Stats

Memebers: Elijah Goglin


