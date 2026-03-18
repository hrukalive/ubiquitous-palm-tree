# Breakthrough game report
Author: Brycen Pina

## Game implementation & discussion
Within my game implementation I've decided to treat the state of the game as given, through subscripting the 8x8 board configuration as a two dimensional list array to avoid extra computation, or pre-calculated transformations. Here's each implementation of the functions I've created.
### to_move(state)
Simply checks the state for the `to_move` object by indexation and returns that value
### actions(state)
This one is a little tricky, it first:
- Grabs which user will go next (**Black/White**).
- Defines the `forward_direction` and `end_location` according to which player's turn it is.
- Checks the legal moves for each pawn in play.
  - This uses a x-directional scanner to scan the direction going forward to the left, middle, and right for each pawn.
- Returns all the legal actions a player can make.
### result(state, action)
The result of the given state if taken an legal state
> Note: this doesn't have to check legality but takes precaution to not rely on the actions' method.
### utility(state, player)
Returns the difference in the closest pawn to the goal through the eyes of the player given.
> **Example**
> > Black is 3 moves away from goal.
>
> > White is 2 moves away from goal.
> 
> > Utility Black: `black_progress - white_progress = 1`
>
> > Utility White: `white_progress - black_progress = -1`
### terminal_test(state)
Verifies whether the state given determines the win of a player.

This succeeds by taking the first and last row of the board, for black; we want to check for white. and for white; vice versa

## Evaluation functions discussion
### defensive_eval_2(state, player)
This evaluation function considers the concern of how close the opposing play is to reaching the goal (Considers all opponents pawns.)

**Evaluation**: `-sum(all_opponents_pawns_distances_to_goal)`
### offensive_eval_2(state, player)
Works by building a sum for each alive pawn the player has, and adding that to the closest pawn to goal with a pressure rate to avoid tunnel vision

**Evaluation**: `sum(alive_eval) + (distance_eval * pressure_rate)`

## Matchup results
> **Agent Notation**
> 
> > mmo1 -> MiniMax Offensive 1
>
> > abo1 -> AlphaBeta Offensive 1
> 
> > abo1 -> AlphaBeta Offensive 1
> 
> > abo2 -> AlphaBeta Offensive 2
>
> > abd1 -> AlphaBeta Defensive 1
> 
> > abd2 -> AlphaBeta Defensive 2
### Match 1 : (mmo1, abo1)

Board:
```
W.......
..WWW...
........
....W...
...W.W..
.B...W..
B.......
........
```
Stats:
- Winning player: white.<br>
-  Captures: White captured 2 pieces, Black captured 16 pieces<br>
-  White player nodes expanded: 1125.<br>
-  Black player nodes expanded: 1055.<br>
-  White player average number of nodes expanded per move: 21.634615384615383. avr. time: 0.02753978461537197.<br>
-  Black player average number of nodes expanded per move: 20.686274509803923. avr. time: 0.011331856862736958.<br>

### Match 2 : (abo2, abd1)
Board:
```
........
WB.B.B..
B.BBB.BB
......B.
.WWW..W.
WW..B.BB
........
.B..WWWW
```
Stats:
- Winning player: black.
- Captures: White captured 2 pieces, Black captured 5 pieces
- White player nodes expanded: 1037.
- Black player nodes expanded: 958.
- White player average number of nodes expanded per move: 28.805555555555557. avr. time: 0.017559358333301134.
- Black player average number of nodes expanded per move: 26.61111111111111. avr. time: 0.015116202777815287.

### Match 3 : (abd2, abo1)
Board:
```
........
.B...B.B
.BB.....
.......B
..B...B.
B....B..
..B.....
........
```
Stats:
- Winning player: black.
- Captures: White captured 5 pieces, Black captured 16 pieces
- White player nodes expanded: 949.
- Black player nodes expanded: 2522.
- White player average number of nodes expanded per move: 2.7114285714285713. avr. time: 0.0005863131428564624.
- Black player average number of nodes expanded per move: 27.714285714285715. avr. time: 0.012866394505521045.

### Match 4 : (abo2, abo1)
Board:
```
W.......
.WWW....
WWW.....
WW......
......BB
..B.BBBB
B....W..
.......W
```
Stats:
- Winning player: white.
- Captures: White captured 8 pieces, Black captured 5 pieces
- White player nodes expanded: 2351.
- Black player nodes expanded: 4072.
- White player average number of nodes expanded per move: 24.237113402061855. avr. time: 0.012379772164919261.
- Black player average number of nodes expanded per move: 26.966887417218544. avr. time: 0.011926273509972503.

### Match 5 : (abd2, abd1)
Board:
```
B.......
...B.B.B
BB.....B
...B...B
......B.
.B......
BBB.BB..
........
```
Stats:
- Winning player: black.
- Captures: White captured 0 pieces, Black captured 16 pieces
- White player nodes expanded: 1854.
- Black player nodes expanded: 2389.
- White player average number of nodes expanded per move: 2.633522727272727. avr. time: 0.0005803863636424984.
- Black player average number of nodes expanded per move: 29.134146341463413. avr. time: 0.013879840243900128.

### Match 6 : (abo2, abd2)
Board:
```
W.......
.WWWW...
...W....
........
..BBB.B.
BB..B...
........
........
```
Stats:
- Winning player: white.
- Captures: White captured 9 pieces, Black captured 10 pieces
- White player nodes expanded: 3659.
- Black player nodes expanded: 3100.
- White player average number of nodes expanded per move: 23.75974025974026. avr. time: 0.011610387012993882.
- Black player average number of nodes expanded per move: 4.078947368421052. avr. time: 0.0010276464473738661.

## Matchup conclusion

- **Offensive evaluations** search more, take longer, and aim for captures and board control.
- **Defensive evaluations** search less, play conservatively, and can win by exploiting opponent overextension.
- **Alpha-Beta > MiniMax**: Alpha-Beta pruning consistently performs better than plain MiniMax.
- **Offense vs Defense**: Results depend on efficiency—strong offense beats defense, but inefficient offense loses.
- **Same-style matchups** are decided mainly by search efficiency and heuristic quality, not play style.