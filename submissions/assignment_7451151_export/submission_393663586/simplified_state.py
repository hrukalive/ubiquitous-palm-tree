def simplify_state(state):
    '''Converts dict state to a tuple[int, int] state'''
    white = 0
    black = 0
    for i, s in enumerate(s for r in state['board'] for s in r):
        if s == "WHITE":
            white |= 1 << i
        if s == "BLACK":
            black |= 1 << i
    return (white, black)


def dict_state(state, to_move):
    white, black = state
    white_count = 0
    black_count = 0
    grid = [["EMPTY"] * 8 for _ in range(8)]
    while white:
        lsb = white & -white
        i = lsb.bit_length() - 1
        grid[i >> 3][i & 7] = "WHITE"
        white_count += 1
        white ^= lsb
    while black:
        lsb = black & -black
        i = lsb.bit_length() - 1
        grid[i >> 3][i & 7] = "BLACK"
        black_count += 1
        black ^= lsb
    return {
        'to_move': to_move,
        'board': grid,
        'captures': {"WHITE": 16 - white_count, "BLACK": 16 - black_count}
    } 


def action_from_simple_states(from_state, to_state):
    '''Determines the dict action for a transition between two tuple[int, int] states'''
    from_white, from_black = from_state
    to_white, to_black = to_state    
    white_changed = from_white ^ to_white
    black_changed = from_black ^ to_black
    if white_changed.bit_count() == 2:
        i_from = (white_changed & from_white).bit_length() - 1
        i_to = (white_changed & to_white).bit_length() - 1
    else:
        i_from = (black_changed & from_black).bit_length() - 1
        i_to = (black_changed & to_black).bit_length() - 1 
    return {
        "from": (i_from // 8, i_from % 8),
        "to": (i_to // 8, i_to % 8),
    }

def expand_white(state):
    '''Returns a list of all possible states after a white move.'''
    potential_states = []
    append = potential_states.append
    white, black = state
    forward_moves = (white >> 8) &~ (black | white)
    while forward_moves:
        dest = forward_moves & -forward_moves
        append((white ^ (dest | (dest << 8)), black))
        forward_moves &= forward_moves - 1
    left_diag_moves = ((white & 0xFEFEFEFEFEFEFEFE) >> 9) &~ white
    while left_diag_moves:
        dest = left_diag_moves & -left_diag_moves
        append((white ^ (dest | dest << 9), black &~ dest))
        left_diag_moves &= left_diag_moves - 1
    right_diag_moves = ((white & 0x7F7F7F7F7F7F7F7F) >> 7) &~ white
    while right_diag_moves:
        dest = right_diag_moves & -right_diag_moves
        append((white ^ (dest | dest << 7), black &~ dest))
        right_diag_moves &= right_diag_moves - 1
    assert all((w | b) < (1 << 64) for w, b in potential_states)
    return potential_states


def expand_black(state):
    '''Returns a list of all possible states after a black move.'''
    potential_states = []
    append = potential_states.append
    white, black = state
    forward_moves = (black << 8) &~ (black | white)
    while forward_moves:
        dest = forward_moves & -forward_moves
        append((white, black ^ (dest | (dest >> 8))))
        forward_moves &= forward_moves - 1
    left_diag_moves = ((black & 0xFEFEFEFEFEFEFEFE) << 7) &~ black
    while left_diag_moves:
        dest = left_diag_moves & -left_diag_moves
        append((white &~ dest, black ^ (dest | dest >> 7)))
        left_diag_moves &= left_diag_moves - 1
    right_diag_moves = ((black & 0x7F7F7F7F7F7F7F7F) << 9) &~ black
    while right_diag_moves:
        dest = right_diag_moves & -right_diag_moves
        append((white &~ dest, black ^ (dest | dest >> 9)))
        right_diag_moves &= right_diag_moves - 1
    assert all((w | b) < (1 << 64) for w, b in potential_states)
    return potential_states


def terminal_state(state):
    return (state[0] == 0) or (state[1] == 0) or (state[0] & 0xFF) or (state[1] & 0xFF00000000000000)

def display_simplified_state(state):
    white, black = state
    row = "   "
    for i in range(64):
        s = 1 << i
        if white & s:
            row += 'W'
        elif black & s:
            row += 'B'
        else:
            row += '.'
        if i % 8 == 7:
            print(row)
            row = "   "

