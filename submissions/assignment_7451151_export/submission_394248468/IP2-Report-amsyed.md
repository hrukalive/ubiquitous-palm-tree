
**Name**: Adeel Syed
**WPI ID**: 901034262

#### Discuss the Breakthrough game formulation and implementation.

The board is a matrix with each cell either container WHITE BLACK or EMPTY to represent the state of everything in there. The rest of the game formulation is decently straight forward. Actions would return the list of valid actions in the form of a list of dicts {"From":(row,col),"To": (row,col)}. Result updates the state with the new board, changes the turn, and updates the capture vals if any. 

#### Write out the definition and discuss your design of Offensive and Defensive Evaluation 2

**Offense**:
**Formula**
**(10 * closestProgress) - (12 * threatenedPenalty) + (2 * captureComponent)**
The idea with this formula is to not really care if you get captured but to care a lot if you get close to the back rank.

*ClosestProgress*: This is just how close you are to the back rank. I wanted to make it so the closer you are the more likely you are to keep moving forward so I took the distance and I squared it.

*ThreatenedPenalty*: This is if a penalty is a pawn is threatened so if you can be taken in one move you are threatened. HOWEVER, I also added a canTakeBack feature where if a pawn can take back it's less of a penalty.

*Capture Component*: this is js offensive eval 1

This won all the matchups it was in so that's cool

**Defense**:
**Formula**
**(2.5protectedCount) + allyComp**
The idea with formula is to make sure all of your pieces are protected and you have everyone

*protectedCount*: This is how many pawns are protected so this should encourage pawns to move together

*AllyComp*: This is just defensive eval1 so this is how many allies / pawns you have times a scalar

*For both of these I didn't include a random because they all included eval1 and eval2 which has the randomness embedded in it*

#### For matchups 1-6, report the following
1. Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
{
  "winner": "black",
  "white_name": "White-Offensive1",
  "black_name": "Black-Offensive1",
  "total_moves": 90,
  "white_nodes": 19148,
  "black_nodes": 19743,
  "white_nodes_per_move": 425.5111111111111,
  "black_nodes_per_move": 438.73333333333335,
  "white_time_per_move": 0.13861539996125632,
  "black_time_per_move": 0.10099428232578146,
  "white_captures": 8,
  "black_captures": 15
}
2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
{
  "winner": "white",
  "white_name": "White-Offensive2",
  "black_name": "Black-Defensive1",
  "total_moves": 29,
  "white_nodes": 76133,
  "black_nodes": 60395,
  "white_nodes_per_move": 5075.533333333334,
  "black_nodes_per_move": 4313.928571428572,
  "white_time_per_move": 1.5742954027373344,
  "black_time_per_move": 0.8726440356320901,
  "white_captures": 1,
  "black_captures": 1
}
3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
{
  "winner": "white",
  "white_name": "White-Defensive2",
  "black_name": "Black-Offensive1",
  "total_moves": 77,
  "white_nodes": 293518,
  "black_nodes": 200749,
  "white_nodes_per_move": 7526.102564102564,
  "black_nodes_per_move": 5282.868421052632,
  "white_time_per_move": 1.7637187276477329,
  "black_time_per_move": 1.087776944153072,
  "white_captures": 12,
  "black_captures": 4
}
4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
{
  "winner": "white",
  "white_name": "White-Offensive2",
  "black_name": "Black-Offensive1",
  "total_moves": 55,
  "white_nodes": 138409,
  "black_nodes": 268082,
  "white_nodes_per_move": 4943.178571428572,
  "black_nodes_per_move": 9928.962962962964,
  "white_time_per_move": 1.2115041889566263,
  "black_time_per_move": 2.11406213573732,
  "white_captures": 7,
  "black_captures": 4
}
5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
{
  "winner": "black",
  "white_name": "White-Defensive2",
  "black_name": "Black-Defensive1",
  "total_moves": 70,
  "white_nodes": 238733,
  "black_nodes": 193114,
  "white_nodes_per_move": 6820.942857142857,
  "black_nodes_per_move": 5517.542857142857,
  "white_time_per_move": 1.8785815749949377,
  "black_time_per_move": 0.9129690819985367,
  "white_captures": 4,
  "black_captures": 5
}
6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
{
  "winner": "white",
  "white_name": "White-Offensive2",
  "black_name": "Black-Defensive2",
  "total_moves": 35,
  "white_nodes": 73045,
  "black_nodes": 42544,
  "white_nodes_per_move": 4058.0555555555557,
  "black_nodes_per_move": 2502.5882352941176,
  "white_time_per_move": 0.8842462338830551,
  "black_time_per_move": 0.4687991839395288,
  "white_captures": 0,
  "black_captures": 2
}


#### Summarize any general trends or conclusions that you have observed. 

Firstly Minimax is obv slower than alpha beta. Nodes expanded is more alpha beta is just more efficient. 
Secondly, I noticed my customized offense agent is super aggressive. Its games end on average way quicker than other games. Additionally, I notice that offensive bots typically win games more than defensive bots. I can't tell if my defensive eval 2 is bad or not because I added more complexity yet it performs worse than the simple defensive algorithm. I put a lot of effort into my offensive one, but I also learned that the more complex it got the more minimal the changes were kind of like the law of diminishing returns.




