IP2 Report: Breakthrough
Name: Shriya Kulkarni
WPI ID: 901013680

1) Breakthrough game formulation and implementation
State representation:
- to_move: "WHITE" or "BLACK"
- captures: {"WHITE": int, "BLACK": int}
- board: 8x8 grid with "WHITE", "BLACK", "EMPTY"

Actions:
- A worker moves one square forward to an empty square.
- A worker captures one square diagonally forward if an opponent worker is present.

Transition model:
- Apply a legal move, update board and captures, and switch player turn.

Terminal test:
- A worker reaches the opponent home row, or
- One side has no workers left, or
- Current player has no legal moves.

Utility:
- +1 for a win, -1 for a loss, 0 otherwise from a given player perspective.

Search:
- Minimax (depth-limited)
- Alpha-Beta pruning (depth-limited, typically deeper than minimax)

2) Offensive Evaluation 2 and Defensive Evaluation 2
Defensive Evaluation 2 (designed to beat Offensive Eval 1):
Def2 = 7.0*own_count - 5.0*own_under_attack + 2.5*own_home + 1.5*own_connections - 1.5*opp_count + random_noise

Feature definitions:
- own_count: number of own workers remaining
- own_under_attack: own workers threatened by opponent diagonal captures
- own_home: own workers still on the home row
- own_connections: number of adjacent own pairs (horizontal/vertical)
- opp_count: number of opponent workers remaining

Design rationale:
- Prioritizes survival, structure, and limiting opponent threats.

Offensive Evaluation 2 (designed to beat Defensive Eval 1):
Off2 = 6.0*(16 - opp_count) + 1.2*advancement + 4.5*capture_chances + 8.0*almost_win + 0.8*own_count + random_noise

Feature definitions:
- 16 - opp_count: number of opponent workers captured
- advancement: total forward progress of own workers
- capture_chances: immediate diagonal capture opportunities
- almost_win: own workers one row from goal
- own_count: number of own workers remaining

Design rationale:
- Prioritizes pressure, tactical captures, and immediate winning threats.

3) Matchups 1-6 results
For each matchup, report:
A) Final board ownership and winner
B) Total game-tree nodes expanded by each player
C) Average nodes expanded per move and average time per move
D) Captures by each player and total moves to win

Matchup 1: Minimax(Offensive Eval 1) vs Alpha-Beta(Offensive Eval 1)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Matchup 2: Alpha-Beta(Offensive Eval 2) vs Alpha-Beta(Defensive Eval 1)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Matchup 3: Alpha-Beta(Defensive Eval 2) vs Alpha-Beta(Offensive Eval 1)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Matchup 4: Alpha-Beta(Offensive Eval 2) vs Alpha-Beta(Offensive Eval 1)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Matchup 5: Alpha-Beta(Defensive Eval 2) vs Alpha-Beta(Defensive Eval 1)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Matchup 6: Alpha-Beta(Offensive Eval 2) vs Alpha-Beta(Defensive Eval 2)
A) Final board + winner: [fill]
B) Total nodes (White / Black): [fill]
C) Avg nodes per move (White / Black): [fill]
   Avg time per move (White / Black): [fill]
D) Captures (White / Black): [fill]
   Total moves: [fill]

Optional repeated-trial note:
- [fill: run count and whether random tie-breaking changed winners or metrics]

4) Trends and conclusions
- Alpha-Beta vs Minimax trend: [fill]
- Offensive vs Defensive style trend: [fill]
- Strongest pairing observed: [fill]
- Overall conclusion: [fill]
