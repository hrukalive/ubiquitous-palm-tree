# CS 4341: Introduction to AI — Individual Project Assignment 2
### Playing Breakthrough

**Name:** Shawn Patel  
**WPI ID:** 901002838

---

## 1. Breakthrough Game Formulation and Implementation

### State Representation

The game state is a Python dictionary with three fields:

```python
{
    'to_move': "WHITE" | "BLACK",
    'captures': {"WHITE": 0, "BLACK": 0},
    'board': [[...]]  # 8x8 grid of "WHITE", "BLACK", or "EMPTY"
}
```

BLACK occupies rows 0–1 at the start, WHITE occupies rows 6–7. WHITE moves first.

### Actions

Each piece can:
- Move **forward one square** (decreasing row for WHITE, increasing row for BLACK) if that square is empty.
- Move **diagonally forward one square** to capture an opponent piece if one is present there.

A piece may **not** capture an opponent piece directly in front of it.

```python
def actions(self, state):
    direction = -1 if player == "WHITE" else 1
    # forward move if empty
    if board[r + direction][c] == "EMPTY":
        moves.append({"from": (r, c), "to": (r + direction, c)})
    # diagonal capture if opponent present
    for dc in [-1, 1]:
        if board[r + direction][c + dc] == opponent:
            moves.append({"from": (r, c), "to": (r + direction, c + dc)})
```

### Transition Model (`result`)

A deep copy of the board is made. The piece is moved from its source square to the destination. If the destination held an opponent piece, the capture counter is incremented. The `to_move` field alternates.

### Terminal Test

The game ends when:
1. A WHITE piece reaches row 0 (BLACK's home row) — WHITE wins.
2. A BLACK piece reaches row 7 (WHITE's home row) — BLACK wins.
3. All pieces of one player are captured.
4. The current player has no legal moves.

### Utility Function

Returns `+1` if the calling player has won, `-1` if they have lost. Only called on terminal states.

---

## 2. Evaluation Functions

### Defensive Evaluation 1 (Given)

Rewards having more of your own pieces remaining:

```
score = 2 * own_pieces_remaining + random()
```

### Offensive Evaluation 1 (Given)

Rewards having fewer opponent pieces remaining:

```
score = 2 * (32 - opponent_pieces_remaining) + random()
```

> `random()` adds uniform noise in [0, 1) to break ties between equally valued moves.

---

### Defensive Evaluation 2

**Definition:**

```
score = 2.5 * own_pieces
      + 0.5 * (horizontally connected pairs)
      + 1.0 * (pieces on home rows 6-7 for WHITE, 0-1 for BLACK)
      - 1.5 * (own pieces under diagonal attack)
      - 1.5 * (opponent advancement depth / 7.0) per opponent piece
      + random()
```

**Design Reasoning:**

The goal of Defensive Evaluation 2 is to hold ground and prevent the opponent from advancing. The key additions over Defensive Evaluation 1 are:

- **Horizontal connectivity bonus:** Pieces next to each other are harder to capture because capturing one exposes the attacker. This rewards formation play.
- **Home row bonus:** Keeping pieces near your home rows creates a defensive wall that slows opponent breakthrough attempts.
- **Under-attack penalty:** A piece that can be captured diagonally on the opponent's next move is penalized, encouraging the agent to move pieces out of danger.
- **Opponent advancement penalty:** The deeper an opponent piece is in your territory, the larger the penalty. This directly punishes allowing breakthroughs and forces the agent to address advancing threats.

---

### Offensive Evaluation 2 (Competition Version)

**Definition:**

```
score = 2.0 * advancement_per_piece
      + 15.0 * (safe pieces on penultimate row) OR 8.0 * (attacked pieces on penultimate row)
      - 20.0 * (uncapturable opponent pieces on their penultimate row) OR -5.0 * (capturable)
      + 1.0 * (pieces threatening diagonal capture)
      + 2.5 * (16 - opponent_pieces_remaining)
      + 1.5 * own_captures
      + 0.5 * own_piece_count
      + random()
```

Where `advancement = (7 - row)` for WHITE and `row` for BLACK.

**Design Reasoning:**

The goal of Offensive Evaluation 2 is to win as quickly as possible by racing pieces to the opponent's home row while neutralising any counter-threats. Key design decisions:

- **Advancement weight (2.0):** Higher than Defensive Evaluation 2's piece count weight, so the agent prefers moving pieces forward over simply surviving.
- **Penultimate row bonus (+15 safe / +8 attacked):** A piece one move away from winning is extremely valuable. The large bonus forces the agent to prioritise getting a piece to row 1 (WHITE) or row 6 (BLACK) above almost everything else.
- **Emergency blocker (-20 uncapturable / -5 capturable):** This is the most important defensive addition. If the opponent has a piece one step from winning that we cannot capture, the -20 penalty forces the agent to block or race. Without this, a purely offensive agent can lose because it ignores opponent near-wins.
- **Threat bonus (+1.0):** Rewarding diagonal threats maintains board pressure and creates capture opportunities.
- **Survival bonus (+0.5 * own pieces):** Prevents the agent from trading pieces so recklessly that it runs out of pieces to advance.

---

## 3. Search Algorithms

### Minimax with Cutoff

Standard minimax search that alternates between MAX (current player) and MIN (opponent) nodes. The search terminates at terminal states (using `utility()`) or at the depth cutoff (using the evaluation function). Depth used: **3**.

```
function max_value(state, depth):
    if terminal: return utility(state, player)
    if depth == 0: return eval_fn(state, player)
    return max over actions of min_value(result(state, a), depth - 1)

function min_value(state, depth):
    if terminal: return utility(state, player)
    if depth == 0: return eval_fn(state, player)
    return min over actions of max_value(result(state, a), depth - 1)
```

### Alpha-Beta Pruning with Cutoff

Extends minimax by maintaining a window `[alpha, beta]`. Branches that cannot improve the current best are pruned, allowing deeper search at the same cost. Depth used: **4**.

```
function max_value(state, alpha, beta, depth):
    ...
    for each action:
        v = max(v, min_value(result(state, a), alpha, beta, depth - 1))
        if v >= beta: return v   # beta cutoff
        alpha = max(alpha, v)
    return v

function min_value(state, alpha, beta, depth):
    ...
    for each action:
        v = min(v, max_value(result(state, a), alpha, beta, depth - 1))
        if v <= alpha: return v  # alpha cutoff
        beta = min(beta, v)
    return v
```

---

## 4. Matchup Results

> **Note:** Each matchup was run once. The `random()` noise in the evaluation functions means results may vary slightly across runs.

---

### Matchup 1: Minimax (Off1) vs Alpha-Beta (Off1)

**A. Final Board State and Winner**

```
Winner: Black (AlphaBeta Off1)

Final Board:
........
.....W..
BBB.B.B.
BB.B..BB
WW.WWBWB
WW.W.W.W
.....W.W
..B.....
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|--|
| White (Minimax Off1) | 55730 |
| Black (AlphaBeta Off1) | 78366 |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|--|-------------------|
| White (Minimax Off1) | 1428.97 | 0.075             |
| Black (AlphaBeta Off1) | 2009.38 | 0.105             |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 3             | 3     |

### Total Moves: 78

---

### Matchup 2: Alpha-Beta (Off2) vs Alpha-Beta (Def1)

**A. Final Board State and Winner**

```
Winner: White (Alpha-Beta Off2)

Final Board:
.W......
....W.W.
.W......
...B..W.
B..W.W..
W....W.B
........
........
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|--|
| White (AlphaBeta Off2) | 166214 |
| Black (AlphaBeta Def1) | 55452 |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|--------------|--|
| White (AlphaBeta Off2) | 3259.10      | 0.269 |
| Black (AlphaBeta Def1) | 1109.04  | 0.083 |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 13            | 7     |

### Total Moves: 101

---

### Matchup 3: Alpha-Beta (Def2) vs Alpha-Beta (Off1)

**A. Final Board State and Winner**

```
Winner: White (Alpha-Beta Def2)

Final Board:
..W.....
B..W.W.W
W......W
........
.W......
......B.
.WBWW...
..W.WW..
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|--|
| White (AlphaBeta Def2) | 39659 |
| Black (AlphaBeta Off1) | 53723 |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|----------------|-------------------|
| White (AlphaBeta Def2) | 922.30         | 0.079             |
| Black (AlphaBeta Off1) | 1279.12        | 0.095             |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 13            | 3     |

### Total Moves: 85

---

### Matchup 4: Alpha-Beta (Off2) vs Alpha-Beta (Off1)

**A. Final Board State and Winner**

```
Winner: White (Alpha-Beta Off2)

Final Board:
.W......
...W..WB
.......B
.....W.W
........
WBW..W..
....W.W.
W.WW.W..
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|--|
| White (AlphaBeta Off2) | 112520 |
| Black (AlphaBeta Off1) | 63511 |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|--------------|-------------------|
| White (AlphaBeta Off2) | 3214.86      | 0.239             |
| Black (AlphaBeta Off1) | 1867.97  | 0.128             |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 13            | 2     |

### Total Moves: 69

---

### Matchup 5: Alpha-Beta (Def2) vs Alpha-Beta (Def1)

**A. Final Board State and Winner**

```
Winner: Black (Alpha-Beta Def 1)

Final Board:
B.......
B.W...B.
W...B.BB
W....B.B
...B.W.W
.....W.W
....WW..
.B..W...
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|------------|
| White (AlphaBeta Def2) | 29576           |
| Black (AlphaBeta Def1) | 41134 |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|----------------|-------------------|
| White (AlphaBeta Def2) | 758.36         | 0.061             |
| Black (AlphaBeta Def1) | 1054.72        | 0.076             |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 6             | 6     |

### Total Moves: 78

---

### Matchup 6: Alpha-Beta (Off2) vs Alpha-Beta (Def2)

**A. Final Board State and Winner**

```
Winner: White (Alpha-Beta Off2)

Final Board:
.....W..
......W.
B..W....
WB.....W
.WB.W...
B.WB..W.
W......W
........
```

**B. Total Nodes Expanded**

| Player | Total Nodes |
|---|----------|
| White (AlphaBeta Off2) | 119764   |
| Black (AlphaBeta Def2) | 31591         |

**C. Avg Nodes/Move and Avg Time/Move**

| Player | Avg Nodes/Move | Avg Time/Move (s) |
|---|--|-----------------|
| White (AlphaBeta Off2) | 2548.17 | 0.193           |
| Black (AlphaBeta Def2) | 686.76 | 0.056     |

**D. Captures and Total Moves**

| | White         | Black |
|---|---------------|-------|
| Pieces Captured | 11            | 5     |

### Total Moves: 93

---

## 5. General Trends and Conclusions

### Minimax vs Alpha-Beta (Matchup 1)

Matchup 1 pitted Minimax (Off1, depth 3) as White against Alpha-Beta (Off1, depth 4) as Black, with both using the same evaluation function. Black won in 78 moves. Although Black expanded more total nodes (78,366 vs 55,730), this is expected — Alpha-Beta searched one level deeper. The per-move averages (2,009 nodes/move for Black vs 1,429 for White) show that Alpha-Beta's pruning let it explore a deeper tree while spending only ~40% more time per move than Minimax at depth 3. The deeper lookahead gave Black a decisive strategic advantage despite identical evaluation logic.

### Offensive vs Defensive Evaluation Functions

The results show a clear pattern: offensive evaluation functions dominate in Breakthrough. Off2 won every matchup it played (Matchups 2, 4, and 6), and in each case it captured significantly more pieces than its opponent — 13 captures in Matchups 2 and 4, and 11 in Matchup 6. This makes sense given Breakthrough's win condition: reaching the opponent's home row requires moving forward aggressively, and an agent that values advancement above survival creates threats that defensive agents cannot easily respond to.

Defensive agents, by contrast, prioritise surviving over advancing. This works to an extent — Def2 beat Off1 in Matchup 3 (13 captures to 3) — but failed against the more sophisticated Off2, which combines aggressive advancement with the emergency blocker to handle near-win threats.

### Evaluation Function Combinations

- **Off2 vs Def1 (Matchup 2):** The clearest dominant performance. Off2 won in 101 moves with 13 captures to Def1's 7. Def1's simple piece-counting gave it no ability to anticipate Off2's advancing threats, and Off2 broke through before Def1 could respond.

- **Def2 vs Off1 (Matchup 3):** A surprising result — the defensive agent won. Def2's territory-awareness and under-attack penalties meant it avoided losing pieces recklessly and penalised Off1's advancing pieces heavily. Off1's simple piece-count offensive failed to break through Def2's formation. Def2 captured 13 pieces to Off1's 3, showing the defensive agent was far more aggressive in eliminating threats than Off1 was in advancing.

- **Off2 vs Off1 (Matchup 4):** Off2 won decisively in just 69 moves — the fastest game of any matchup. Off2 captured 13 pieces to Off1's 2. The emergency blocker and penultimate row bonuses in Off2 gave it a significant edge over Off1's simpler piece-count offensive; Off2 knew when to race and when to block, Off1 did not.

- **Def2 vs Def1 (Matchup 5):** The only matchup where the "weaker" evaluation won — Def1 beat Def2 in 78 moves with equal captures (6 each). This is the most likely matchup to be affected by random noise, as both agents are similarly passive. Neither actively seeks a quick win, making small random differences in move selection influential. Def2's more complex scoring may have occasionally misevaluated positions compared to Def1's simpler but consistent piece count.

- **Off2 vs Def2 (Matchup 6):** Off2 won in 93 moves with 11 captures to Def2's 5. This was the most competitive matchup for Off2, as Def2's territorial awareness posed a stronger challenge than Def1. However, Off2's advancement scoring and penultimate row bonuses ultimately outpaced Def2's blocking capability.

### Effect of Random Noise

The `random()` tiebreaker meaningfully influenced Matchup 5 (Def2 vs Def1), where both agents have similar passive strategies and neither strongly dominates. In all other matchups the stronger evaluation function won consistently, suggesting that for clearly asymmetric matchups the noise has minimal impact on the final outcome. Running each matchup multiple times would be most valuable for Matchup 5 to determine whether Def1 reliably beats Def2 or whether that result was noise-driven.

### Alpha-Beta Efficiency

Across all Alpha-Beta matchups at depth 4, nodes per move ranged from ~687 (Def2, Matchup 6) to ~3,259 (Off2, Matchup 2). The more complex evaluation functions (Off2, Def2) expanded more nodes per move than the simpler ones (Off1, Def1) at the same depth, because their richer scoring creates more diverse value distributions that reduce pruning effectiveness. Despite this, all Alpha-Beta agents outperformed the Minimax depth-3 agent in Matchup 1 in terms of decision quality, confirming that deeper search with pruning is more effective than shallower exhaustive search.