switch = lambda role: 'O' if role == 'X' else 'X'


initial_context = '''I am playing Tic-Tac-Toe with an opponent. I want you to help me win the game. I am "{self}" and my opponent is "{oppo}".'''


availablility_prompt = '''Which positions are empty in the given Tic-Tac-Toe board?

Examples

Example
Tic-Tac-Toe Board:

1 | 2 | 3
---------
4 | X | 6
---------
7 | 8 | 9

Empty Positions: 1,2,3,4,6,7,8,9

Example
Tic-Tac-Toe Board:

O | O | X
---------
O | X | O
---------
7 | X | X

Role: O

Empty Positions: 7

Your Turn
Tic-Tac-Toe Board:

{state}

Empty Positions:'''


initial_prompt = '''The initial Tic-Tac-Toe Board:

1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

'''


action_prompt = '''In the game of Tic-Tac-Toe, two players, "X" and "O," alternate placing their symbols on a 3x3 grid. The objective is to be the first to get three of their symbols in a row, either horizontally, vertically, or diagonally. We use numbers to indicate empty positions, and then replace them with "X" or "O" as moves are made. For example, an empty board is denoted by

1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

Your task is to identify the optimal position for the next move based on the current board state. Assume that it's your turn and you're playing as "{role}". Please make sure the optimal position is EMPTY. For example, in the following Tic-Tac-Toe Board:

1 | 2 | 3
---------
4 | X | 6
---------
7 | 8 | 9

Position 5 is occupied by "X". Thus, position 5 is not an optimal position. Provide only the optimal position in the first line. In the second line, give a brief explanation for this choice.

Current Tic-Tac-Toe Board:

{state}

Role: {role}

Optimal Position:'''


action_prompt_v1 = '''In the game of Tic-Tac-Toe, two players, "X" and "O," alternate placing their symbols on a 3x3 grid. The objective is to be the first to get three of their symbols in a row, either horizontally, vertically, or diagonally.

Your task is to identify the optimal position for the next move based on the current board state. Assume that it's your turn and you're playing as "{role}".

Examples

Example
Tic-Tac-Toe Board:

O | X | O
---------
X | O | X
---------
7 | 8 | X

Role: O

Empty Position: 7,8
Optimal Position: 8

Now Analyze the Following Tic-Tac-Toe Board.
Tic-Tac-Toe Board:

{state}

Role: {role}

Empty Positions: {action_space}
Please make sure the output is an empty position without "X" or "O".
Optimal Position:'''


propose_prompt = '''In the game of Tic-Tac-Toe, two players, "X" and "O," alternate placing their symbols on a 3x3 grid. The objective is to be the first to get three of their symbols in a row, either horizontally, vertically, or diagonally. We use numbers to indicate empty positions, and then replace them with "X" or "O" as moves are made. For example, an empty board is denoted by

1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

Your task is to identify the optimal position for the next move based on the current board state. Assume that it's your turn and you're playing as "{role}". 

Guidelines for Optimal Moves:
{improvement_plan}

Instructions
List the top {n} positions for placing my symbol on the Tic-Tac-Toe board. Please make sure the suggested positions are empty without "X" or "O". For example, in the following Tic-Tac-Toe Board:

1 | 2 | 3
---------
4 | X | 6
---------
7 | 8 | 9

Position 5 is occupied by "X". Thus, position 5 should not be suggested.
Provide the top {n} positions in the first line, separated by commas. In the second line, give a brief explanation for each choice.

Current Tic-Tac-Toe Board:

{state}

Role: {role}

Suggested Positions:'''


propose_prompt_v1 = '''In the game of Tic-Tac-Toe, two players, "X" and "O," alternate placing their symbols on a 3x3 grid. The objective is to be the first to get three of their symbols in a row, either horizontally, vertically, or diagonally.

Your task is to identify the optimal position for the next move based on the current board state. Assume that it's your turn and you're playing as "{role}".

Guidelines for Optimal Moves:
{improvement_plan}

Instructions
List the top {n} positions for placing my symbol on the Tic-Tac-Toe board. Provide these positions in the first line, separated by commas. In the second line, give a brief explanation for each choice.

Example:

Example 1
Tic-Tac-Toe Board:

O | X | O
---------
X | O | X
---------
7 | 8 | X

Role: O

Empty Positions: 7,8

Suggested Positions: 7,8

Example 2
Tic-Tac-Toe Board:

1 | 2 | 3
---------
4 | X | 6
---------
7 | 8 | 9

Role: O

Empty Positions: 1,2,3,4,6,7,8,9

Suggested Positions: 1,2,3,4

Your Turn
Suggest Up to {n} Optimal Positions for My "{role}" on the Following Tic-Tac-Toe Board.

Tic-Tac-Toe Board:

{state}

Role: {role}

Empty Positions: {action_space}

Please make sure the outputs are empty positions
Suggested Positions:'''


dynamics_prompt = '''Predict the Next State of the Tic-Tac-Toe Board

In a game of Tic-Tac-Toe, two players, "X" and "O," take turns to place their symbols on a 3x3 grid. Your task is to predict what the board will look like after a specified move has been made.

Examples
{examples}
Now, Predict the Next State of the Following Tic-Tac-Toe Board:
Initial Tic-Tac-Toe Board:

{state}

Move: Player puts "{role}" in position {action}.

Updated Board:'''


oppo_prompt = '''In Tic-Tac-Toe, each player takes turns placing their respective symbols ("X" or "O") on a 3x3 board. Your task is to predict where the opponent will place their symbol based on their past moves and the current board state.

Example
Tic-Tac-Toe Board:

O | X | O
---------
X | O | X
---------
7 | 8 | X

Opponent's Move: "O" in position 7
{examples}
Here's how the Tic-Tac-Toe board currently looks:
Tic-Tac-Toe Board:

{state}

Given the history and current board state, where do you think the opponent will place their "{role}" next? Please make sure the output is an empty position without "X" or "O".

Opponent's Move: "{role}" in position'''


complete_prompt = '''In the game of Tic-Tac-Toe, two players alternate turns to fill a 3x3 grid with their respective symbols: "X" and "O". A board is considered "completely filled" when all nine cells of the grid contain either an 'X' or an 'O', with no empty spaces or other characters. 

Examples:
{examples}
Now for the Current Tic-Tac-Toe Board:
Tic-Tac-Toe Board:

{state}

Is the board completely filled?

Answer:'''


complete_prompt_v1 = '''In the game of Tic-Tac-Toe, two players alternate turns to fill a 3x3 grid with their respective symbols: "X" and "O". A board is considered "completely filled" when all nine cells of the grid contain either an 'X' or an 'O', with no empty spaces or other characters. 

Examples:

Example 1:

Tic-Tac-Toe Board:

O | X | X
---------
X | X | O
---------
O | O | X

Question: Is the board completely filled?

Answer: Yes

Example 2:

Tic-Tac-Toe Board:

X | O | X
---------
O | X | O
---------
7 | X | O

Is the board completely filled?

Answer: No

Now for the Current Tic-Tac-Toe Board:
Tic-Tac-Toe Board:

{state}

Is the board completely filled?

Answer:'''


evaluate_prompt_v1 = '''Determine the Winner in a Tic-Tac-Toe Game

In Tic-Tac-Toe, two players, "X" and "O," take turns to place their respective symbols on a 3x3 board. The first player to get three of their symbols in a row—either horizontally, vertically, or diagonally—wins the game. Your task is to evaluate the board state and determine if there is a winner.

Examples

Example 1
Tic-Tac-Toe Board:

O | X | O
---------
X | X | X
---------
O | O | X

Question: Is there a winner?

Answer: Let's think step by step.

First row: O X O, no winner
Second row: X X X, X wins

Therefore, "X" wins

Example 2
Tic-Tac-Toe Board:

X | 2 | O
---------
4 | O | X
---------
O | X | 9

Question: Is there a winner?

Answer: Let's think step by step.

First row: X 2 O, no winner
Second row: 4 O X, no winner
Third row: O X 9, no winner
First column: X 4 O, no winner
Second column: 2 O X, no winner
Thrid column: O X 9, no winner
Main diagonal: X O 9, no winner
Anti-diagonal: O O O, O wins

Therefore, "O" wins.

Example 3
Tic-Tac-Toe Board:

O | X | O
---------
4 | X | X
---------
O | 8 | 9

Question: Is there a winner?

Answer: Let's think step by step.

First row: X 2 O, no winner
Second row: 4 X X, no winner
Third row: O 8 9, no winner
First column: 0 4 O, no winner
Second column: X X 8, no winner
Thrid column: O X 9, no winner
Main diagonal: O X O, no winner
Anti-diagonal: O X 9, no winner

Therefore, there is no winner.

Now, for the Current Tic-Tac-Toe Board:
Tic-Tac-Toe Board:

{state}

Question: Is there a winner?

Answer: Let's think step by step.'''


evaluate_prompt = '''Determine the Winner in a Tic-Tac-Toe Game

In Tic-Tac-Toe, two players, "X" and "O," take turns to place their respective symbols on a 3x3 board. The first player to get three of their symbols in a row—either horizontally, vertically, or diagonally—wins the game. Your task is to evaluate the board state and determine if there is a winner.

Examples

Example
Tic-Tac-Toe Board:

O | X | O
---------
X | X | X
---------
O | O | X

Question: Is there a winner?

Answer: Let's think step by step.

First row: O X O, no winner
Second row: X X X, X wins

Therefore, "X" wins

Example
Tic-Tac-Toe Board:

X | 2 | O
---------
4 | O | X
---------
O | X | 9

Question: Is there a winner?

Answer: Let's think step by step.

First row: X 2 O, no winner
Second row: 4 O X, no winner
Third row: O X 9, no winner
First column: X 4 O, no winner
Second column: 2 O X, no winner
Thrid column: O X 9, no winner
Main diagonal: X O 9, no winner
Anti-diagonal: O O O, O wins

Therefore, "O" wins.
{examples}
Now, for the Current Tic-Tac-Toe Board:
Tic-Tac-Toe Board:

{state}

Question: Is there a winner?

Answer: Let's think step by step.'''


record_self_prompt = '''My Move: "{role}" in position {action}

Tic-Tac-Toe Board:

{state}

'''


record_oppo_prompt = '''Opponent's Move: "{role}" in position {action}

Tic-Tac-Toe Board:

{state}

'''


improve_prompt = '''\n\nPlease refine your strategy and summarize what you have learned succinctly. Improvement Plan:'''


optimize_prompt = '''Here are some saved Tic-Tac-Toe games:

{saved_games}

Please summarize all the improvement plans:'''


# Generate Examples
## Generate dynamics prediction examples
example_dynamics_prompt = '''
Example
Initial Tic-Tac-Toe Board:

{state}

Move: Player puts "{role}" in position {action}.

Updated Board:

{next_state}
'''


## Opponent modeling examples
example_oppo_prompt = '''
Example
Tic-Tac-Toe Board:

{state}

Opponent's Move: "{role}" in position {action}
'''

## Generate 
example_winner_prompt = '''
Example
Tic-Tac-Toe Board:

{state}

Question: Is there a winner?

Answer: Let's think step by step.

{cot}
'''


# Generate
example_complete_prompt = '''
Example
Tic-Tac-Toe Board:

{state}

Question: Is the board completely filled?

Answer: {yes_or_no}
'''


action_fix_prompt = ''' {action}

[System]
Error: The position {action} is not empty. Please make sure the output is an empty position not occupied by "X" or "O".

Current Tic-Tac-Toe Board:

{state}

Role: {role}

Optimal position:'''


suggestion_fix_prompt = ''' {actions}

[System]
Error: Please make sure the suggested positions are not occupied by "X" or "O". Please choose from the following available positions: {available_actions}

Suggested Positions:'''
