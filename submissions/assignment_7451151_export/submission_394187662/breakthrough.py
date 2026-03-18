
import random
from copy import deepcopy
from tqdm import tqdm
from games import Game

class Breakthrough(Game):
    def initial_state(self): # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",                   # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0}, # Initially, white and black have captured 0 pieces.
            'board': grid,                        # 8x8 grid representing the board.
        } # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):
        return state['to_move']

    def actions(self, state):
        player = state['to_move']
        board = state['board']
        actions = []
        direction = -1 if player == "WHITE" else 1
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    # Forward
                    nr, nc = r + direction, c
                    if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == "EMPTY":
                        actions.append({"from": (r, c), "to": (nr, nc)})
                    # Diagonals
                    for dc in [-1, 1]:
                        nr, nc = r + direction, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8 and (board[nr][nc] == "EMPTY" or board[nr][nc] == enemy):
                            actions.append({"from": (r, c), "to": (nr, nc)})
        return actions

    def result(self, state, action):
        from_r, from_c = action["from"]
        to_r, to_c = action["to"]
        player = state['to_move']
        enemy = "BLACK" if player == "WHITE" else "WHITE"
        new_board = deepcopy(state['board'])
        new_captures = deepcopy(state['captures'])
        if new_board[to_r][to_c] == enemy:
            new_captures[player] += 1
        new_board[to_r][to_c] = player
        new_board[from_r][from_c] = "EMPTY"
        return {"to_move": enemy, "captures": new_captures, "board": new_board}

    def utility(self, state, player):
        board = state['board']
        captures = state['captures']
        winner = None
        if captures['WHITE'] == 16 or "WHITE" in board[0]: winner = "WHITE"
        elif captures['BLACK'] == 16 or "BLACK" in board[7]: winner = "BLACK"
        elif not self.actions(state):
            winner = "BLACK" if state['to_move'] == "WHITE" else "WHITE"

        if winner == player: return 999999
        if winner is not None: return -999999
        my_pieces = sum(row.count(player) for row in board)
        enemy = "BLACK" if player == "WHITE" else "WHITE"
        enemy_pieces = sum(row.count(enemy) for row in board)
        return (my_pieces - enemy_pieces) / 32

    def terminal_test(self, state):
        board = state['board']
        caps = state['captures']
        return caps['WHITE'] == 16 or caps['BLACK'] == 16 or "WHITE" in board[0] or "BLACK" in board[7] or not self.actions(state)

    def display(self, state):
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print("\n".join("".join(chars[state['board'][r][c]] for c in range(8)) for r in range(8)))
        if self.terminal_test(state):
            if self.to_move(state) == "WHITE":
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {state['to_move']}")
        print(f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")

def defensive_eval_1(state, player):
    """
    Evaluation function focusing on retaining own pieces.
    Heuristic = 2 * (My Pieces) + random()
    """
    board = state['board']
    my_pieces = 0
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
                
    return 2 * my_pieces + random.random()


def offensive_eval_1(state, player):
    """
    Evaluation function focusing on attacking and advancing.
    Heuristic = 2 * (30 - Opponent Pieces) + random()
    Note: 30 is just a constant to keep the value positive, 
    but effectively it maximizes capturing enemy pieces.
    """
    board = state['board']
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    enemy_pieces = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == enemy:
                enemy_pieces += 1
                
    return 2 * (30 - enemy_pieces) + random.random()

# Global weights for ML training
#'PieceAlmostWin'                       High priority to closing out the game
#'ColumnHole'                               Penalize leaving open columns
# 'PieceHomeGround'                    Either encourages defense or penalizes it for offense.
# 'PieceDangerValue'                    Reward advancing forward
# 'PieceHighDangerValue'             Reward being very close to winning
# 'PieceUnderAttack'                   Penalize being under attack
# 'PieceCenterControl'                  Encourage controlling the center of the board
# 'PieceConnectHorizontal'           Encourage horizontal connection
# 'PieceConnectVertical'               Encourage vertical connection
# 'PieceTrade'                              Reward trading pieces when ahead on material
# 'OpponentAlmostWin'                Get aggressive when opponent is close to winning
# 'CaptureDiff'                             Reward having more captures than opponent
# 'AggressiveAttack'                   Reward for being able to attack opponent pieces (defensive: how many of your pieces can attack)
# 'EnemyDangerValue'                   Penalize enemy pieces advancing forward
# 'EnemyHighDanger'                   Penalize enemy pieces that are very close to winning
# 'UndefendedHomeRow'              Penalize having undefended home row squares
# 'UndefendedPiece'                   Penalize having pieces that are undefended
# 'PieceBlockEnemy'              Reward for blocking enemy pieces from advancing
# 'EnemyClustered'                  Penalize enemy pieces that are clustered together
# 'EnemyIsolated'                   Reward enemy pieces that are isolated
# 'PieceEscapeRoute'                Penalize leaving open spaces for opponents to escape
# 'TakeUndefendedPiece'             Reward for being able to take an undefended enemy piece
# 'PassedPawn'                        Reward for a piece having a clear path to the end
# 'Phalanx'                           Reward for having two pieces side-by-side
# 'SupportedPiece'                    Reward for having a piece defended from behind
# 'Mobility'                          Reward for having more available moves
# 'ThreatToWin'                       Reward for being able to win on the next move

# Best Score: 4990.0
# Least Mistakes: 1.0
DEF_WEIGHTS = {
    'PieceAlmostWin': -11.5855,
    'ColumnHole': -20.4983,
    'PieceHomeGround': 20.1930,
    'PieceDangerValue': -9.2066,
    'PieceHighDangerValue': 10.2823,
    'PieceUnderAttack': -7.3373,
    'PieceCenterControl': 6.3894,
    'PieceConnectHorizontal': 13.6336,
    'PieceConnectVertical': 8.5181,
    'PieceTrade': 8.6745,
    'OpponentAlmostWin': -18.0850,
    'CaptureDiff': 20.0683,
    'AggressiveAttack': -8.2297,
    'EnemyDangerValue': -3.9859,
    'EnemyHighDanger': -3.9509,
    'UndefendedHomeRow': -7.2297,
    'UndefendedPiece': -19.1406,
    'PieceBlockEnemy': -33.6837,
    'EnemyClustered': -21.2591,
    'EnemyIsolated': 2.5290,
    'PieceEscapeRoute': -1.4194,
    'TakeUndefendedPiece': 6.1722,
    'PassedPawn': 1.5903,
    'Phalanx': 10.9084,
    'SupportedPiece': 15.3991,
    'Mobility': 19.0031,
    'ThreatToWin': 33.0306,
    'ForcedWin': 8.4772,
}

# Best Score: 4990.0
# Least Mistakes: 1.0
OFF_WEIGHTS = {
    'PieceAlmostWin': 6.5298,
    'ColumnHole': -17.8411,
    'PieceHomeGround': -5.8721,
    'PieceDangerValue': 1.2756,
    'PieceHighDangerValue': 40.3467,
    'PieceUnderAttack': -7.0217,
    'PieceCenterControl': 0.0207,
    'PieceConnectHorizontal': 10.9584,
    'PieceConnectVertical': 0.8930,
    'PieceTrade': 14.9031,
    'OpponentAlmostWin': -7.2739,
    'CaptureDiff': 2.6542,
    'AggressiveAttack': -7.4262,
    'EnemyDangerValue': -9.8302,
    'EnemyHighDanger': -5.7407,
    'UndefendedHomeRow': -0.7427,
    'UndefendedPiece': -3.3829,
    'PieceBlockEnemy': -6.7707,
    'EnemyClustered': -7.4300,
    'EnemyIsolated': 11.7655,
    'PieceEscapeRoute': -6.6646,
    'TakeUndefendedPiece': 3.8248,
    'PassedPawn': 23.5752,
    'Phalanx': 12.5299,
    'SupportedPiece': 6.7336,
    'Mobility': 16.5050,
    'ThreatToWin': 15.4544,
    'ForcedWin': 6.7648,
}

def defensive_eval_2(state, player, weights=None, return_features=False):
    """
    Improved Defensive View: Uses unified features with defensive weight bias.
    """
    game = Breakthrough()
    if game.terminal_test(state): 
        score = game.utility(state, player)
        return (score, {}) if return_features else score

    # Check for immediate win (1 move away)
    f = _get_feature_counts(state, player)
    if f['ThreatToWin'] > 0:
        return (900000, f) if return_features else 900000

    W = weights if weights else DEF_WEIGHTS
    score = sum(f[k] * W.get(k, 0) for k in f if k in W)
    
    return (score, f) if return_features else score

def offensive_eval_2(state, player, weights=None, return_features=False):
    """
    Improved Offensive View: Uses unified features with offensive weight bias.
    """
    game = Breakthrough()
    if game.terminal_test(state):
        score = game.utility(state, player)
        return (score, {}) if return_features else score

    # Check for immediate win (1 move away)
    f = _get_feature_counts(state, player)
    if f['ThreatToWin'] > 0:
        return (900000, f) if return_features else 900000

    W = weights if weights else OFF_WEIGHTS
    score = sum(f[k] * W.get(k, 0) for k in f if k in W)
    
    return (score, f) if return_features else score

def _get_feature_counts(state, player):
    board = state['board']
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    direction = -1 if player == "WHITE" else 1
    goal_row = 0 if player == "WHITE" else 7
    pen_row = 1 if player == "WHITE" else 6
    prep_row = 2 if player == "WHITE" else 5
    
    f = {
        'PieceAlmostWin': 0,
        'ForcedWin': 0,
        'ColumnHole': 0,
        'OpponentAlmostWin': 0,
        'AggressiveAttack': 0,
        'PieceBlockEnemy': 0,
        'ThreatToWin': 0,
        'PieceHomeGround': 0,
        'PieceDangerValue': 0,
        'PieceHighDangerValue': 0,
        'PieceUnderAttack': 0,
        'PieceCenterControl': 0,
        'PieceConnectHorizontal': 0,
        'PieceConnectVertical': 0,
        'PieceTrade': 0,
        'CaptureDiff': 0,
        'EnemyDangerValue': 0,
        'EnemyHighDanger': 0,
        'UndefendedHomeRow': 0,
        'UndefendedPiece': 0,
        'EnemyClustered': 0,
        'EnemyIsolated': 0,
        'PieceEscapeRoute': 0,
        'TakeUndefendedPiece': 0,
        'PassedPawn': 0,
        'Phalanx': 0,
        'SupportedPiece': 0,
        'Mobility': 0,
    }

    threat_columns = set()
    
    for r in range(8):
        for c in range(8):
            cell = board[r][c]
            if cell == "EMPTY": continue
            
            if cell == player:
                dist_from_start = abs(r - (7 if player == "WHITE" else 0))
                f['PieceDangerValue'] += dist_from_start
                
                if r == pen_row:
                    f['PieceAlmostWin'] += 1
                    for dc in [-1, 0, 1]:
                        if 0 <= c+dc < 8:
                            target = board[goal_row][c+dc]
                            if target == "EMPTY" or target == enemy:
                                f['ThreatToWin'] += 1
                                threat_columns.add(c+dc)

                if c in [3, 4]:
                    f['PieceCenterControl'] += 1
                
                for dc in [-1, 1]:
                    enemy_r = r - direction 
                    enemy_c = c + dc
                    if 0 <= enemy_r < 8 and 0 <= enemy_c < 8:
                        if board[enemy_r][enemy_c] == enemy:
                            f['PieceUnderAttack'] += 1

            elif cell == enemy:
                e_dist_from_start = abs(r - (0 if player == "WHITE" else 7))
                f['EnemyDangerValue'] += e_dist_from_start
                
                if e_dist_from_start >= 6: 
                    f['OpponentAlmostWin'] += 1

    f['CaptureDiff'] = state['captures'][player] - state['captures'][enemy]
    
    f['Mobility'] = len(board.actions(state)) if hasattr(board, 'actions') else 0

    if len(threat_columns) >= 2:
        f['ForcedWin'] += 5.0

    return f

def adaptive_eval(state, player, move_history=[]):
    game = Breakthrough()
    if game.terminal_test(state): 
        return game.utility(state, player)

    board = state['board']
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    
    my_start = 7 if player == "WHITE" else 0
    enemy_start = 0 if player == "WHITE" else 7
    
    my_pieces = 0
    enemy_pieces = 0
    max_my_dist = 0
    max_enemy_dist = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
                dist = abs(r - my_start)
                if dist > max_my_dist: max_my_dist = dist
            elif board[r][c] == enemy:
                enemy_pieces += 1
                dist = abs(r - enemy_start)
                if dist > max_enemy_dist: max_enemy_dist = dist

    # Determine "Stance" (0.0 = Pure Defense, 1.0 = Pure Offense)
    stance = 0.5 

    # Material Advantage If we have more pieces, we can afford to be offensive and trade
    material_ratio = my_pieces / max(1, enemy_pieces)
    stance += (material_ratio - 1.0) * 0.2

    # If we are further ahead, push for the win
    if max_my_dist > max_enemy_dist:
        stance += 0.15
    elif max_enemy_dist > max_my_dist:
        stance -= 0.15

    # If enemy is 3 or more moves from winning, FORCE defensive behavior
    if max_enemy_dist >= 5:
        stance = 0.1
    
    # If we are 1 or 2 moves from winning, FORCE offensive behavior
    if max_my_dist >= 6:
        stance = 0.9 

    stance = max(0.0, min(1.0, stance))

    f = _get_feature_counts(state, player)
    
    # If a forced win is detected, switch to 100% offense.
    if f.get('ThreatToWin', 0) > 0 or f.get('ForcedWin', 0) > 2:
        stance = 1.0 
    elif f.get('OpponentAlmostWin', 0) > 0:
        stance = 0.0
    else:
        # Standard dynamic stance based on piece count
        my_pieces = sum(row.count(player) for row in state['board'])
        en_pieces = sum(row.count("BLACK" if player == "WHITE" else "WHITE") for row in state['board'])
        stance = 0.6 if my_pieces >= en_pieces else 0.4

    # Interpolate using the new stance
    score = 0
    for k in f:
        w_def = DEF_WEIGHTS.get(k, 0)
        w_off = OFF_WEIGHTS.get(k, 0)
        blended_weight = (1 - stance) * w_def + (stance) * w_off
        score += f[k] * blended_weight
        
    return score

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = adaptive_eval  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.

    :param white_agent: An agent that plays white.
    :param black_agent: An agent that plays black.
    :param max_moves: The maximum number of moves to play.
    :param display: Whether to display the game state during play.
    :param progress: Whether to show a progress bar.
    :return: The statistic of the game play.
    """
    game = Breakthrough()

    state = game.initial_state()
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game, state)
        state = game.result(state, move)
        if display:
            game.display(state)
        move_count += 1
        if progress:
            pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break
    if progress:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = (sum(white_agent.time_per_move) / len(white_agent.time_per_move))
    black_time_per_move = (sum(black_agent.time_per_move) / len(black_agent.time_per_move))
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state["captures"]["WHITE"]
    black_captures = state["captures"]["BLACK"]
    if display:
        game.display(state)
    return {
        'winner': 'white' if winner == "WHITE" else 'black' if winner == "BLACK" else None,
        'white_name': white_agent.name,
        'black_name': black_agent.name,
        'total_moves': move_count,
        'white_nodes': white_nodes,
        'black_nodes': black_nodes,
        'white_nodes_per_move': white_nodes_per_move,
        'black_nodes_per_move': black_nodes_per_move,
        'white_time_per_move': white_time_per_move,
        'black_time_per_move': black_time_per_move,
        'white_captures': white_captures,
        'black_captures': black_captures,
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
