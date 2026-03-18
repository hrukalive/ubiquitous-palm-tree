<h3>Game Formulation & Implementation</h2>

<li>State Representation: A dictionary tracking to_move ("WHITE" or "BLACK"), a captures tally for each player, and an 8×8 board matrix (cells hold "WHITE", "BLACK", or "EMPTY").</li>
<li>Actions: White pieces move upward (decreasing row index) and Black pieces move downward. A piece can move straight forward to an empty square, or diagonally forward to an empty square or to capture an opponent.</li>
<li>Transition Model: Deep-copies the state, moves the piece, removes captured pieces, increments the capture count, and flips the turn to the other player.</li>
<li>Terminal Test & Utility: The game ends if a player reaches the opposite end of the board, loses all their pieces, or has no legal moves. The utility function returns +1 for a win and -1 for a loss.</li>

<h3>Evaluation Function Design</h3>

<b>Defensive Evaluation 1:</b>
<p><ol>Formula: 2 * (own pieces remaining) + random(0,1)</ol></p>
<p><ol>Reasoning: Keeping more pieces alive is simplest defensive metric. Player with more pieces has more options and is usually harder to defeat. Random noise breaks ties and prevents repetitive play.</ol></p>

<b>Offensive Evaluation 1:</b>
<p><ol>Formula: 2 * (32 - opponent pieces remaining) + random(0,1)</ol></p>
<p><ol>Reasoning: Rewarding removal of opponent pieces makes agent capture more aggressively. Expression (32 - opponent pieces) grows as more opponent pieces are captured, so scale matches Defensive Eval 1</ol></p>

<b> Defensive Evaluation 2:</b>
<p>Defensive Eval 2 extends baseline with positional awareness</p>
<p><ol>Formula: Score = 2 * (own_count) - 0.3 * (opp_advancement_threat) - 0.2 * (own_exposure_penalty) + random(0,1)</ol></p>
<p><ol>Where: <ol><li>own_count is the number of the agent's remaining pieces (survival bonus)</li><li>opp_advancement_threat is the sum of opponent advancement values: for each opponent piece, advancement = row index (BLACK) or 7 - row index (WHITE). Higher values mean opponent is close to agent's home row which is dangerous</li><li>own_exposure_penalty counts the agent's own pieces with advancement >= 6 (close to opponent's home). Pieces this far forward are isolated and likely to be captured so small penalty should reduce reckless advancements.</li></ol></ol></p>
<p><ol>Design Intent: The agent should prioritize survival and prevent opponents from advancing, not rushing its own pieces into dangerous situations. Intended to defeat Offensive Eval 1 which doesn't account for opponent position.</ol></p>

<b>Offensive Evaluation 2:</b>

<p>Offensive Evaluation 2 rewards forward advancement of own pieces and proximity to goal row.</p>
<p><ol>Formula: score = own_advancement + 3 * (pieces_captured) + close_to_goal_bonus + own_count + random(0,1)</ol></p>
<p><ol>Where: <ol><li>own_advancement is the sum of advancement values for all of agent's pieces. Each pieces's advancement = (7 - row) for WHITE or row for BLACK</li><li>pieces_captured = 16 - opponent_count, scaled by 3 to incentivise captures strongly</li><li>close_to_goal_bonus adds +5 for pieces with advancement >= 6 and +2 for advancement >= 5, creating a strong pull toward the goal</li><li>own_count is included as a small secondary survival term</li></ol></ol></p>
<p><ol>Design Intent: Push pieces forward aggressively and prioritize winning by reaching goal row, intended to beat Defensive Eval 1.</ol></p>

<h3>Experiment Results (Run 2)</h3>
<table>
<tr>
<th>#</th><th>White vs Black</th><th>Winner</th><th>Moves</th><th>W Captures</th><th>B Captures</th><th>White Average Time</th><th>Black Average Time</th><th>White Nodes Expanded</th><th>Black Nodes Expanded</th><th>White Avg Nodes/Move</th><th>Black Avg Nodes/Move</th>
</tr>
<tr>
<td>1</td> <td>Minimax(Off1) vs AB(Off1)</td><td>Black</td><td>90</td><td>5</td><td>15</td><td>0.3713s</td><td>0.9551s</td><td>347,152</td><td>881,232</td><td>7,714.5</td><td>19,582.9</td>
</tr>
<tr>
<td>2</td> <td>AB(Off2) vs AB(Def1)</td><td>White</td><td>97</td><td>15</td><td>2</td><td>1.7391s</td><td>0.6091s</td><td>1,629,421</td><td>591,003</td><td>33,253.5</td><td>12,312.6</td>
</tr>
<tr>
<td>3</td> <td>AB(Def2) vs AB(Off1)</td><td>White</td><td>83</td><td>15</td><td>1</td><td>1.691s</td><td>0.6049s</td><td>1,395,197</td><td>508,869</td><td>33,219</td><td>12,411.4</td>
</tr>
<tr>
<td>4</td> <td>AB(Off2) vs AB(Off1)</td><td>White</td><td>91</td><td>13</td><td>2</td><td>1.3065s</td><td>0.8834s</td><td>1,184,121</td><td>831,135</td><td>25,741.8</td><td>18,469.7</td>
</tr>
<tr>
<td>5</td> <td>AB(Def2) vs AB(Def1)</td><td>Black</td><td>82</td><td>7</td><td>7</td><td>2.5618s</td><td>0.9037s</td><td>2,048,085</td><td>760,262</td><td>49,953.3</td><td>18,543</td>
</tr>
<tr>
<td>6</td> <td>AB(Off2) vs AB(Def2)</td><td>Black</td><td>91</td><td>3</td><td>3</td><td>4.2755s</td><td>0.8889s</td><td>2,710,351</td><td>572,697</td><td>82,131.8</td><td>17,354.5</td>
</tr>
</table>
In Run 1, White won 5/6 matchups. The only Black win was #1, where AB beat Minimax, showing search depth advantage. All other tests were Alpha-beta vs itself at equal depth.
In Run 2, White won 4/6 matchups. Matchups 1-4 were consistent across both runs. Match 5 and 6 flipped, indicating random noise determined the winner.

<h3>Matchup 1: White: Minimax (Off1) vs Black: Alpha-Beta (Off1)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<th>1</th><td></td><td></td><td>B</td><td></td><td>W</td><td>B</td><td></td><td></td>
</tr>
<tr>
<th>2</th><td>B</td><td>B</td><td></td><td>B</td><td></td><td></td><td>B</td><td>B</td>
</tr>
<tr>
<th>3</th><td></td><td></td><td></td><td></td><td>B</td><td></td><td></td><td></td>
</tr>
<tr>
<th>4</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<th>5</th><td></td><td>B</td><td>B</td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<th>6</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<th>7</th><td>B</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
</table>

<h3>Matchup 2: White: Alpha-Beta (Off2) vs Black: Alpha-Beta (Def1)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>1</th> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td>W</td> <td></td> <td>W</td>
</tr>
<tr>
<th>2</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>3</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>4</th> <td>W</td> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td>W</td>
</tr>
<tr>
<th>5</th> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td>W</td> <td>B</td> <td></td>
</tr>
<tr>
<th>6</th> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td>W</td>
</tr>
<tr>
<th>7</th> <td></td> <td></td> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
</table>

<h3>Matchup 3: White: Alpha-Beta (Def2) vs Black: Alpha-Beta (Off1)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td>W</td> <td></td>
</tr>
<tr>
<th>1</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>2</th> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>3</th> <td></td> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td>W</td> <td></td>
</tr>
<tr>
<th>4</th> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td></td>
</tr>
<tr>
<th>5</th> <td>W</td> <td></td> <td>W</td> <td></td> <td></td> <td></td> <td>W</td> <td>B</td>
</tr>
<tr>
<th>6</th> <td>W</td> <td></td> <td>W</td> <td></td> <td>W</td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>7</th> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
</table>


<h3>Matchup 4: White: Alpha-Beta (Off2) vs Black: Alpha-Beta (Off1)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>1</th> <td></td> <td>W</td> <td>W</td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>2</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td></td>
</tr>
<tr>
<th>3</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td>W</td> <td></td>
</tr>
<tr>
<th>4</th> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td>W</td> <td>B</td> <td>B</td>
</tr>
<tr>
<th>5</th> <td>B</td> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>6</th> <td></td> <td></td> <td>W</td> <td>W</td> <td></td> <td>W</td> <td>W</td> <td>W</td>
</tr>
<tr>
<th>7</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
</table>


<h3>Matchup 5 (Run 1): White: Alpha-Beta (Def2) vs Black: Alpha-Beta (Def1)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>1</th> <td></td> <td>W</td> <td></td> <td>B</td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>2</th> <td>B</td> <td></td> <td>B</td> <td>B</td> <td>B</td> <td>B</td> <td>B</td> <td>B</td>
</tr>
<tr>
<th>3</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>4</th> <td></td> <td></td> <td></td> <td>W</td> <td>W</td> <td>W</td> <td>W</td> <td>W</td>
</tr>
<tr>
<th>5</th> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td>W</td> <td></td> <td>W</td>
</tr>
<tr>
<th>6</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>7</th> <td></td> <td></td> <td>B</td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
</table>

<h3>Matchup 6: White: Alpha-Beta (Off2) vs Black: Alpha-Beta (Def2)</h3>
<table>
<th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
<tr>
<th>0</th> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
<tr>
<th>1</th> <td>W</td> <td></td> <td>B</td> <td></td> <td>B</td> <td></td> <td>B</td> <td></td>
</tr>
<tr>
<th>2</th> <td></td> <td></td> <td>B</td> <td>B</td> <td>B</td> <td>B</td> <td>B</td> <td>B</td>
</tr>
<tr>
<th>3</th> <td></td> <td></td> <td></td> <td>B</td> <td></td> <td>B</td> <td></td> <td>B</td>
</tr>
<tr>
<th>4</th> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td>W</td> <td></td> <td>W</td>
</tr>
<tr>
<th>5</th> <td>W</td> <td></td> <td>W</td> <td>W</td> <td>W</td> <td>W</td> <td>W</td> <td>W</td>
</tr>
<tr>
<th>6</th> <td></td> <td></td> <td></td> <td>W</td> <td></td> <td></td> <td></td> <td>W</td>
</tr>
<tr>
<th>7</th> <td></td> <td>B</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>
</tr>
</table>

<h3>Conclusions and Observations</h3>

1. Search Depth is Decisive:
   - Alpha-Beta at depth 4 beat Minimax at depth 3 with the same evaluation function in both runs. Black expanded ~55x more nodes per move. Depth advantage translates to stronger play.
2. Off2 is the Strongest Evaluation:
   - Offensive Eval 2 won all of its matchups in run 1 (Match 2,4,6) and all but one in run 2 (match 6 flipped). Its advancement bonus and goal-proximity reward make for a good strategy that outperforms both baseline functions consistently. Rewarding advancement is more effective than purely counting pieces.
3. Def2 Beats Off1 Consistently:
   - Matchup 3 (Def2 vs Off1) produced the same winner both runs. Def2's opponent advancement penalty disrupts Off1's straightforward capture strategy by giving it the spatial awarness that Off1 does not have.
4. Noise determines closely-matched matches:
   - Matchups 5 and 6 flipped between runs. These pairings are strategically close enough that the random() tie-breaking term can influence decisions and turn into a different outcome. Running and reporting multiple times would give a more reliable estimate of true winners.
5. Node expansion patterns:
   - The winning agent almost always expanded more nodes per move.
6. Overall ranking:
   - Considering both runs, the evaluation functions rank as: Off2 >= Def2 > Off1 > Def1. 
   - Off2 and Def2 are closely matched (1-1).