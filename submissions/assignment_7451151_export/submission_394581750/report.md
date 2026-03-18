# CS 4341 – Individual Project Assignment 2  
## Playing Breakthrough with Minimax and Alpha-Beta  

**Name:** Evan Demas 
**WPI ID:** 901008824  

---

# 1. Breakthrough Game Formulation and Implementation  

## 1.1 Problem Formulation  

Breakthrough is modeled as a two-player deterministic zero-sum game.

### State Representation  

The board is represented as an 8 × 8 grid.  
Each square contains:

- `0` for empty  
- `1` for White piece  
- `-1` for Black piece  

The state includes:
- The board configuration  
- The current player (White or Black)  

---

### Actions  

From a given state, legal actions consist of:

- Moving a piece one square forward  
- Moving diagonally forward left  
- Moving diagonally forward right  
- Capturing diagonally forward if an opponent piece exists  

Backward and lateral moves are not allowed.

---

### Transition Model  

The transition function:

1. Creates a copy of the current board  
2. Applies the selected move  
3. Removes the captured piece if applicable  
4. Switches the active player  

---

### Terminal Test  

A state is terminal if:

1. A piece reaches the opponent’s home row  
2. All opponent pieces are captured  

---

### Utility Function  

If the state is terminal:

- `+∞` for win  
- `-∞` for loss  

If non-terminal at depth limit:

- Return evaluation function value  

---

# 2. Search Algorithms  

## 2.1 Minimax  

I implemented standard depth-limited minimax:

- Alternates max and min layers  
- Recursively explores children  
- Returns best utility  

**Depth used:** 2–3  

---

## 2.2 Alpha-Beta Pruning  

Alpha-beta pruning improves minimax by:

- Maintaining `alpha` (best max so far)  
- Maintaining `beta` (best min so far)  
- Pruning branches when `beta ≤ alpha`  

**Depth used:** 4–5  

Alpha-beta consistently expands fewer nodes than minimax.

---

# 3. Evaluation Functions  

## 3.1 Defensive Evaluation 1  
