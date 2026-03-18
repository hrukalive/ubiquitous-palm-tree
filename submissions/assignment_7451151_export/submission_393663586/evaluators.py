from simplified_state import *

# Final Evaluation Function
def evaluator_4(state):
    white, black = simplify_state(state) 
    if white & 0x00000000000000FF: return 100000
    if black & 0xFF00000000000000: return -100000
    whites_turn = 1 if state['to_move'] == "WHITE" else 0
    table = [
        857, 857, 857, 857, 857, 857, 857, 857,
        750, 821, 821, 821, 821, 821, 821, 750,
        500, 786, 786, 786, 786, 786, 786, 500,
        321, 536, 750, 750, 750, 750, 750, 321,
        214, 321, 571, 571, 571, 571, 321, 214,
        107, 179, 357, 357, 357, 357, 179, 107,
         71, 107, 107, 107, 107, 107, 107,  71,
        179,1000,1000, 429, 429,1000,1000, 179,
    ]
    white_left = ((white & 0xFEFEFEFEFEFEFEFE) >> 9)
    white_right = ((white & 0x7F7F7F7F7F7F7F7F) >> 7)
    black_left = ((black & 0xFEFEFEFEFEFEFEFE) << 7)
    black_right = ((black & 0x7F7F7F7F7F7F7F7F) << 9)

    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_control = (white_any &~ black_any) | (white_both &~ black_both)
    black_control = (black_any &~ white_any) | (black_both &~ white_both)
    
    white_friends = ((white & 0xFEFEFEFEFEFEFEFE) >> 1) | ((white & 0x7F7F7F7F7F7F7F7F) << 1)
    black_friends = ((black & 0xFEFEFEFEFEFEFEFE) >> 1) | ((black & 0x7F7F7F7F7F7F7F7F) << 1)
  
    if whites_turn: 
        if white & 0x000000000000FF00:
            return 100000.0
        if black & 0x00FF000000000000 &~ white_control:
            return -100000.0
        if white_control & 0x000000000000FF00:
            return 100000.0
    else: 
        if black & 0x00FF000000000000:
            return -100000.0
        if white & 0x000000000000FF00 &~ black_control:
            return 100000.0
        if black_control & 0x00FF000000000000:
            return -100000.0

    white_table = [
        0x0000000000000001, 0x0000000000000002, 0x0000000000000004, 0x0000000000000008,
        0x0000000000000010, 0x0000000000000020, 0x0000000000000040, 0x0000000000000080,
        
        0x0000000000000103, 0x0000000000000207, 0x000000000000040E, 0x000000000000081C,
        0x0000000000001038, 0x0000000000002070, 0x00000000000040E0, 0x00000000000080C0,
        
        0x0000000000010307, 0x000000000002070F, 0x0000000000040E1F, 0x0000000000081C3E,
        0x000000000010387C, 0x00000000002070F8, 0x000000000040E0F0, 0x000000000080C0E0,
        
        0x000000000103070F, 0x0000000002070F1F, 0x00000000040E1F3F, 0x00000000081C3E7F,
        0x0000000010387CFE, 0x000000002070F8FC, 0x0000000040E0F0F8, 0x0000000080C0E0F0,
        
        0x0000000103070F1F, 0x00000002070F1F3F, 0x000000040E1F3F7F, 0x000000081C3E7FFF,
        0x00000010387CFEFF, 0x0000002070F8FCFE, 0x00000040E0F0F8FC, 0x00000080C0E0F0F8,
        
        0x00000103070F1F3F, 0x000002070F1F3F7F, 0x0000040E1F3F7FFF, 0x0000081C3E7FFFFF,
        0x000010387CFEFFFF, 0x00002070F8FCFEFF, 0x000040E0F0F8FCFE, 0x000080C0E0F0F8FC,
        
        0x000103070F1F3F7F, 0x0002070F1F3F7FFF, 0x00040E1F3F7FFFFF, 0x00081C3E7FFFFFFF,
        0x0010387CFEFFFFFF, 0x002070F8FCFEFFFF, 0x0040E0F0F8FCFEFF, 0x0080C0E0F0F8FCFE,
        
        0x0103070F1F3F7FFF, 0x02070F1F3F7FFFFF, 0x040E1F3F7FFFFFFF, 0x081C3E7FFFFFFFFF,
        0x10387CFEFFFFFFFF, 0x2070F8FCFEFFFFFF, 0x40E0F0F8FCFEFFFF, 0x80C0E0F0F8FCFEFF,
    ]
    black_table = [
        0xFF7F3F1F0F070301, 0xFFFF7F3F1F0F0702, 0xFFFFFF7F3F1F0E04, 0xFFFFFFFF7F3E1C08,
        0xFFFFFFFFFE7C3810, 0xFFFFFFFEFCF87020, 0xFFFFFEFCF8F0E040, 0xFFFEFCF8F0E0C080,
        
        0x7F3F1F0F07030100, 0xFF7F3F1F0F070200, 0xFFFF7F3F1F0E0400, 0xFFFFFF7F3E1C0800,
        0xFFFFFFFE7C381000, 0xFFFFFEFCF8702000, 0xFFFEFCF8F0E04000, 0xFEFCF8F0E0C08000,

        0x3F1F0F0703010000, 0x7F3F1F0F07020000, 0xFF7F3F1F0E040000, 0xFFFF7F3E1C080000,
        0xFFFFFE7C38100000, 0xFFFEFCF870200000, 0xFEFCF8F0E0400000, 0xFCF8F0E0C0800000,

        0x1F0F070301000000, 0x3F1F0F0702000000, 0x7F3F1F0E04000000, 0xFF7F3E1C08000000,
        0xFFFE7C3810000000, 0xFEFCF87020000000, 0xFCF8F0E040000000, 0xF8F0E0C080000000,

        0x0F07030100000000, 0x1F0F070200000000, 0x3F1F0E0400000000, 0x7F3E1C0800000000,
        0xFE7C381000000000, 0xFCF8702000000000, 0xF8F0E04000000000, 0xF0E0C08000000000,

        0x0703010000000000, 0x0F07020000000000, 0x1F0E040000000000, 0x3E1C080000000000,
        0x7C38100000000000, 0xF870200000000000, 0xF0E0400000000000, 0xE0C0800000000000,

        0x0301000000000000, 0x0702000000000000, 0x0E04000000000000, 0x1C08000000000000,
        0x3810000000000000, 0x7020000000000000, 0xE040000000000000, 0xC080000000000000,

        0x0100000000000000, 0x0200000000000000, 0x0400000000000000, 0x0800000000000000,
        0x1000000000000000, 0x2000000000000000, 0x4000000000000000, 0x8000000000000000,
    ] 
    
    val = 0
    white_end = 10
    black_end = 10
    w = white
    b = black
    while w:
        i = (w & -w).bit_length() - 1
        cone = white_table[i] & black
        w_cone = white_table[i] & white
        b_cone = white_table[i] & black
        val += 20 * (w_cone.bit_count() - b_cone.bit_count()) 
        if (1 << i) & 0x0000000000810000:
            if cone == 0:
                white_end = min(white_end, 7 - (i // 8))
        elif (cone & (cone - 1)) == 0:
            white_end = min(white_end, 7 - (i // 8))
        val += 20000 + table[i]
        if (1 << i) &~ black_control:
            val += 0.5 * table[i]
        if (1 << i) &~ white_friends:
            val -= 300
        w &= w - 1
    while b:
        i = (b & -b).bit_length() - 1 
        cone = black_table[i] & white
        w_cone = black_table[i] & white
        b_cone = black_table[i] & black
        val += 20 * (w_cone.bit_count() - b_cone.bit_count())
        if (1 << i) & 0x0000810000000000:
            if cone == 0:
                black_end = min(black_end, i // 8)
        elif (cone & (cone - 1)) == 0:
            black_end = min(black_end, i // 8)
        val -= 20000 + table[63 - i]
        if (1 << i) &~ white_control:
            val -= 0.5 * table[63 - i]
        if (1 << i) &~ black_friends:
            val += 300
        b &= b - 1
    
    if white_end < 10 or black_end < 10:
        if whites_turn:
            if white_end <= black_end:
                return 100000.0 + val
            else:
                return -100000.0 + val
        else:
            if black_end <= white_end:
                return -100000.0 + val
            else:
                return 100000.0 + val
    return val



#================ different versions used in testing ==========================
def evaluator_1(state):
    white, black = simplify_state(state) 
    if white & 0x00000000000000FF: return 100000
    if black & 0xFF00000000000000: return -100000
    whites_turn = 1 if state['to_move'] == "WHITE" else 0  
    val = 0.0
    table = [
        857, 857, 857, 857, 857, 857, 857, 857,
        750, 821, 821, 821, 821, 821, 821, 750,
        500, 786, 786, 786, 786, 786, 786, 500,
        321, 536, 750, 750, 750, 750, 750, 321,
        214, 321, 571, 571, 571, 571, 321, 214,
        107, 179, 357, 357, 357, 357, 179, 107,
         71, 107, 107, 107, 107, 107, 107,  71,
        179,1000,1000, 429, 429,1000,1000, 179,
    ]
    white_left = ((white & 0xFEFEFEFEFEFEFEFE) >> 9)
    white_right = ((white & 0x7F7F7F7F7F7F7F7F) >> 7)
    black_left = ((black & 0xFEFEFEFEFEFEFEFE) << 7)
    black_right = ((black & 0x7F7F7F7F7F7F7F7F) << 9)

    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_control = (white_any &~ black_any) | (white_both &~ black_both)
    black_control = (black_any &~ white_any) | (black_both &~ white_both)
    safe_white = 0xFFFFFFFFFFFFFFFF &~ black_control
    safe_black = 0xFFFFFFFFFFFFFFFF &~ white_control
  
    white_table = [
        0x0000000000000001, 0x0000000000000002, 0x0000000000000004, 0x0000000000000008,
        0x0000000000000010, 0x0000000000000020, 0x0000000000000040, 0x0000000000000080,
        
        0x0000000000000103, 0x0000000000000207, 0x000000000000040E, 0x000000000000081C,
        0x0000000000001038, 0x0000000000002070, 0x00000000000040E0, 0x00000000000080C0,
        
        0x0000000000010307, 0x000000000002070F, 0x0000000000040E1F, 0x0000000000081C3E,
        0x000000000010387C, 0x00000000002070F8, 0x000000000040E0F0, 0x000000000080C0E0,
        
        0x000000000103070F, 0x0000000002070F1F, 0x00000000040E1F3F, 0x00000000081C3E7F,
        0x0000000010387CFE, 0x000000002070F8FC, 0x0000000040E0F0F8, 0x0000000080C0E0F0,
        
        0x0000000103070F1F, 0x00000002070F1F3F, 0x000000040E1F3F7F, 0x000000081C3E7FFF,
        0x00000010387CFEFF, 0x0000002070F8FCFE, 0x00000040E0F0F8FC, 0x00000080C0E0F0F8,
        
        0x00000103070F1F3F, 0x000002070F1F3F7F, 0x0000040E1F3F7FFF, 0x0000081C3E7FFFFF,
        0x000010387CFEFFFF, 0x00002070F8FCFEFF, 0x000040E0F0F8FCFE, 0x000080C0E0F0F8FC,
        
        0x000103070F1F3F7F, 0x0002070F1F3F7FFF, 0x00040E1F3F7FFFFF, 0x00081C3E7FFFFFFF,
        0x0010387CFEFFFFFF, 0x002070F8FCFEFFFF, 0x0040E0F0F8FCFEFF, 0x0080C0E0F0F8FCFE,
        
        0x0103070F1F3F7FFF, 0x02070F1F3F7FFFFF, 0x040E1F3F7FFFFFFF, 0x081C3E7FFFFFFFFF,
        0x10387CFEFFFFFFFF, 0x2070F8FCFEFFFFFF, 0x40E0F0F8FCFEFFFF, 0x80C0E0F0F8FCFEFF,
    ]
    black_table = [
        0xFF7F3F1F0F070301, 0xFFFF7F3F1F0F0702, 0xFFFFFF7F3F1F0E04, 0xFFFFFFFF7F3E1C08,
        0xFFFFFFFFFE7C3810, 0xFFFFFFFEFCF87020, 0xFFFFFEFCF8F0E040, 0xFFFEFCF8F0E0C080,
        
        0x7F3F1F0F07030100, 0xFF7F3F1F0F070200, 0xFFFF7F3F1F0E0400, 0xFFFFFF7F3E1C0800,
        0xFFFFFFFE7C381000, 0xFFFFFEFCF8702000, 0xFFFEFCF8F0E04000, 0xFEFCF8F0E0C08000,

        0x3F1F0F0703010000, 0x7F3F1F0F07020000, 0xFF7F3F1F0E040000, 0xFFFF7F3E1C080000,
        0xFFFFFE7C38100000, 0xFFFEFCF870200000, 0xFEFCF8F0E0400000, 0xFCF8F0E0C0800000,

        0x1F0F070301000000, 0x3F1F0F0702000000, 0x7F3F1F0E04000000, 0xFF7F3E1C08000000,
        0xFFFE7C3810000000, 0xFEFCF87020000000, 0xFCF8F0E040000000, 0xF8F0E0C080000000,

        0x0F07030100000000, 0x1F0F070200000000, 0x3F1F0E0400000000, 0x7F3E1C0800000000,
        0xFE7C381000000000, 0xFCF8702000000000, 0xF8F0E04000000000, 0xF0E0C08000000000,

        0x0703010000000000, 0x0F07020000000000, 0x1F0E040000000000, 0x3E1C080000000000,
        0x7C38100000000000, 0xF870200000000000, 0xF0E0400000000000, 0xE0C0800000000000,

        0x0301000000000000, 0x0702000000000000, 0x0E04000000000000, 0x1C08000000000000,
        0x3810000000000000, 0x7020000000000000, 0xE040000000000000, 0xC080000000000000,

        0x0100000000000000, 0x0200000000000000, 0x0400000000000000, 0x0800000000000000,
        0x1000000000000000, 0x2000000000000000, 0x4000000000000000, 0x8000000000000000,
    ] 
    
    white_end = 10
    black_end = 10
    w = white
    b = black
    while w:
        i = (w & -w).bit_length() - 1
        cone = white_table[i] & (black | 0x0081000000000000)
        if (cone & (cone - 1)) == 0:
            white_end = min(white_end, 7 - (i // 8))
        val += 9000 + table[i]
        if (1 << i) &~ black_control:
            val += 0.5 * table[i]
        w &= w - 1
    while b:
        i = (b & -b).bit_length() - 1 
        cone = black_table[i] & (white | 0x0000000000008100)
        if (cone & (cone - 1)) == 0:
            black_end = min(black_end, i // 8)
        val -= 9000 + table[63 - i]
        if (1 << i) &~ white_control:
            val -= 0.5 * table[i]
        b &= b - 1
    
    if white_end < 10 or black_end < 10:
        if whites_turn:
            if white_end <= black_end:
                return 100000.0 + val
            else:
                return -100000.0 + val
        else:
            if black_end <= white_end:
                return -100000.0 + val
            else:
                return 100000.0 + val
    return val


def evaluator_2(state):
    white, black = simplify_state(state) 
    if white & 0x00000000000000FF: return 100000
    if black & 0xFF00000000000000: return -100000
    whites_turn = 1 if state['to_move'] == "WHITE" else 0  
    val = 0.0
    table = [
        857, 857, 857, 857, 857, 857, 857, 857,
        750, 821, 821, 821, 821, 821, 821, 750,
        500, 786, 786, 786, 786, 786, 786, 500,
        321, 536, 750, 750, 750, 750, 750, 321,
        214, 321, 571, 571, 571, 571, 321, 214,
        107, 179, 357, 357, 357, 357, 179, 107,
         71, 107, 107, 107, 107, 107, 107,  71,
        179,1000,1000, 429, 429,1000,1000, 179,
    ]
    white_left = ((white & 0xFEFEFEFEFEFEFEFE) >> 9)
    white_right = ((white & 0x7F7F7F7F7F7F7F7F) >> 7)
    black_left = ((black & 0xFEFEFEFEFEFEFEFE) << 7)
    black_right = ((black & 0x7F7F7F7F7F7F7F7F) << 9)

    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_control = (white_any &~ black_any) | (white_both &~ black_both)
    black_control = (black_any &~ white_any) | (black_both &~ white_both)
    safe_white = 0xFFFFFFFFFFFFFFFF &~ black_control
    safe_black = 0xFFFFFFFFFFFFFFFF &~ white_control
    
    white_friends = ((white & 0xFEFEFEFEFEFEFEFE) >> 1) | ((white & 0x7F7F7F7F7F7F7F7F) << 1)
    black_friends = ((black & 0xFEFEFEFEFEFEFEFE) >> 1) | ((black & 0x7F7F7F7F7F7F7F7F) << 1)
  
    if whites_turn: 
        if white & 0x000000000000FF00:
            return 100000.0
        if safe_black & black & 0x00FF000000000000:
            return -100000.0
    else: 
        if black & 0x00FF000000000000:
            return -100000.0
        if safe_white & white & 0x000000000000FF00:
            return 100000.0 
  
    white_table = [
        0x0000000000000001, 0x0000000000000002, 0x0000000000000004, 0x0000000000000008,
        0x0000000000000010, 0x0000000000000020, 0x0000000000000040, 0x0000000000000080,
        
        0x0000000000000103, 0x0000000000000207, 0x000000000000040E, 0x000000000000081C,
        0x0000000000001038, 0x0000000000002070, 0x00000000000040E0, 0x00000000000080C0,
        
        0x0000000000010307, 0x000000000002070F, 0x0000000000040E1F, 0x0000000000081C3E,
        0x000000000010387C, 0x00000000002070F8, 0x000000000040E0F0, 0x000000000080C0E0,
        
        0x000000000103070F, 0x0000000002070F1F, 0x00000000040E1F3F, 0x00000000081C3E7F,
        0x0000000010387CFE, 0x000000002070F8FC, 0x0000000040E0F0F8, 0x0000000080C0E0F0,
        
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,

        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,

        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
    ]
    black_table = [
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,

        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,

        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF,

        0x0F07030100000000, 0x1F0F070200000000, 0x3F1F0E0400000000, 0x7F3E1C0800000000,
        0xFE7C381000000000, 0xFCF8702000000000, 0xF8F0E04000000000, 0xF0E0C08000000000,

        0x0703010000000000, 0x0F07020000000000, 0x1F0E040000000000, 0x3E1C080000000000,
        0x7C38100000000000, 0xF870200000000000, 0xF0E0400000000000, 0xE0C0800000000000,

        0x0301000000000000, 0x0702000000000000, 0x0E04000000000000, 0x1C08000000000000,
        0x3810000000000000, 0x7020000000000000, 0xE040000000000000, 0xC080000000000000,

        0x0100000000000000, 0x0200000000000000, 0x0400000000000000, 0x0800000000000000,
        0x1000000000000000, 0x2000000000000000, 0x4000000000000000, 0x8000000000000000,
    ] 
    
    white_end = 10
    black_end = 10
    w = white
    b = black

    def ending(state, whites_turn):
        if (state[0] & 0xFF) or (state[1] == 0):
            return 1
        if (state[0] == 0) or (state[1] & 0xFF00000000000000):
            return 0
        if whites_turn:
            return max(ending(s, 0) for s in expand_white(state))
        else:
            return min(ending(s, 1) for s in expand_black(state))

    while w:
        i = (w & -w).bit_length() - 1
        s = (1 << i, white_table[i] & black)
        if s[1].bit_count() <= 2 and ending(s, whites_turn):
            white_end = min(white_end, 7 - (i // 8))
        val += 10000 + table[i]
        if (1 << i) &~ black_control:
            val += 0.8 * table[i]
        if (1 << i) &~ white_friends:
            val -= 300
        w &= w - 1
    while b:
        i = (b & -b).bit_length() - 1 
        s = (black_table[i] & white, 1 << i)
        if s[0].bit_count() <= 2 and not ending(s, whites_turn):
            black_end = min(black_end, i // 8)
        val -= 10000 + table[63 - i]
        if (1 << i) &~ white_control:
            val -= 0.8 * table[63 - i]
        if (1 << i) &~ black_friends:
            val += 300
        b &= b - 1
    
    if white_end < 10 or black_end < 10:
        if whites_turn:
            if white_end <= black_end:
                return 1000000.0 + val
            else:
                return -1000000.0 + val
        else:
            if black_end <= white_end:
                return -1000000.0 + val
            else:
                return 1000000.0 + val
    return val

def evaluator_3(state):
    white, black = simplify_state(state) 
    if white & 0x00000000000000FF: return 100000
    if black & 0xFF00000000000000: return -100000
    whites_turn = 1 if state['to_move'] == "WHITE" else 0  
    val = 0.0
    table = [
        857, 857, 857, 857, 857, 857, 857, 857,
        750, 821, 821, 821, 821, 821, 821, 750,
        500, 786, 786, 786, 786, 786, 786, 500,
        321, 536, 750, 750, 750, 750, 750, 321,
        214, 321, 571, 571, 571, 571, 321, 214,
        107, 179, 357, 357, 357, 357, 179, 107,
         71, 107, 107, 107, 107, 107, 107,  71,
        179,1000,1000, 429, 429,1000,1000, 179,
    ]
    white_left = ((white & 0xFEFEFEFEFEFEFEFE) >> 9)
    white_right = ((white & 0x7F7F7F7F7F7F7F7F) >> 7)
    black_left = ((black & 0xFEFEFEFEFEFEFEFE) << 7)
    black_right = ((black & 0x7F7F7F7F7F7F7F7F) << 9)

    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_control = (white_any &~ black_any) | (white_both &~ black_both)
    black_control = (black_any &~ white_any) | (black_both &~ white_both)
    safe_white = 0xFFFFFFFFFFFFFFFF &~ black_control
    safe_black = 0xFFFFFFFFFFFFFFFF &~ white_control
    
    white_friends = ((white & 0xFEFEFEFEFEFEFEFE) >> 1) | ((white & 0x7F7F7F7F7F7F7F7F) << 1)
    black_friends = ((black & 0xFEFEFEFEFEFEFEFE) >> 1) | ((black & 0x7F7F7F7F7F7F7F7F) << 1)
  
    if whites_turn: 
        if white & 0x000000000000FF00:
            return 100000.0
        if safe_black & black & 0x00FF000000000000:
            return -100000.0
    else: 
        if black & 0x00FF000000000000:
            return -100000.0
        if safe_white & white & 0x000000000000FF00:
            return 100000.0 
    
    white_table = [
        0x0000000000000001, 0x0000000000000002, 0x0000000000000004, 0x0000000000000008,
        0x0000000000000010, 0x0000000000000020, 0x0000000000000040, 0x0000000000000080,

        0x0000000000000103, 0x0000000000000207, 0x000000000000040E, 0x000000000000081C,
        0x0000000000001038, 0x0000000000002070, 0x00000000000040E0, 0x00000000000080C0,
        
        0x0000000000010307, 0x000000000002070F, 0x0000000000040E1F, 0x0000000000081C3E,
        0x000000000010387C, 0x00000000002070F8, 0x000000000040E0F0, 0x000000000080C0E0,
        
        0x000000000103070F, 0x0000000002070F1F, 0x00000000040E1F3F, 0x00000000081C3E7F,
        0x0000000010387CFE, 0x000000002070F8FC, 0x0000000040E0F0F8, 0x0000000080C0E0F0,
        
        0x0000000103070F1F, 0x00000002070F1F3F, 0x000000040E1F3F7F, 0x000000081C3E7FFF,
        0x00000010387CFEFF, 0x0000002070F8FCFE, 0x00000040E0F0F8FC, 0x00000080C0E0F0F8,
        
        0x00000103070F1F3F, 0x000002070F1F3F7F, 0x0000040E1F3F7FFF, 0x0000081C3E7FFFFF,
        0x000010387CFEFFFF, 0x00002070F8FCFEFF, 0x000040E0F0F8FCFE, 0x000080C0E0F0F8FC,
        
        0x000103070F1F3F7F, 0x0002070F1F3F7FFF, 0x00040E1F3F7FFFFF, 0x00081C3E7FFFFFFF,
        0x0010387CFEFFFFFF, 0x002070F8FCFEFFFF, 0x0040E0F0F8FCFEFF, 0x0080C0E0F0F8FCFE,
        
        0x0103070F1F3F7FFF, 0x02070F1F3F7FFFFF, 0x040E1F3F7FFFFFFF, 0x081C3E7FFFFFFFFF,
        0x10387CFEFFFFFFFF, 0x2070F8FCFEFFFFFF, 0x40E0F0F8FCFEFFFF, 0x80C0E0F0F8FCFEFF,
    ]
    black_table = [
        0xFF7F3F1F0F070301, 0xFFFF7F3F1F0F0702, 0xFFFFFF7F3F1F0E04, 0xFFFFFFFF7F3E1C08,
        0xFFFFFFFFFE7C3810, 0xFFFFFFFEFCF87020, 0xFFFFFEFCF8F0E040, 0xFFFEFCF8F0E0C080,
        
        0x7F3F1F0F07030100, 0xFF7F3F1F0F070200, 0xFFFF7F3F1F0E0400, 0xFFFFFF7F3E1C0800,
        0xFFFFFFFE7C381000, 0xFFFFFEFCF8702000, 0xFFFEFCF8F0E04000, 0xFEFCF8F0E0C08000,

        0x3F1F0F0703010000, 0x7F3F1F0F07020000, 0xFF7F3F1F0E040000, 0xFFFF7F3E1C080000,
        0xFFFFFE7C38100000, 0xFFFEFCF870200000, 0xFEFCF8F0E0400000, 0xFCF8F0E0C0800000,

        0x1F0F070301000000, 0x3F1F0F0702000000, 0x7F3F1F0E04000000, 0xFF7F3E1C08000000,
        0xFFFE7C3810000000, 0xFEFCF87020000000, 0xFCF8F0E040000000, 0xF8F0E0C080000000,

        0x0F07030100000000, 0x1F0F070200000000, 0x3F1F0E0400000000, 0x7F3E1C0800000000,
        0xFE7C381000000000, 0xFCF8702000000000, 0xF8F0E04000000000, 0xF0E0C08000000000,

        0x0703010000000000, 0x0F07020000000000, 0x1F0E040000000000, 0x3E1C080000000000,
        0x7C38100000000000, 0xF870200000000000, 0xF0E0400000000000, 0xE0C0800000000000,

        0x0301000000000000, 0x0702000000000000, 0x0E04000000000000, 0x1C08000000000000,
        0x3810000000000000, 0x7020000000000000, 0xE040000000000000, 0xC080000000000000,

        0x0100000000000000, 0x0200000000000000, 0x0400000000000000, 0x0800000000000000,
        0x1000000000000000, 0x2000000000000000, 0x4000000000000000, 0x8000000000000000,
    ] 
    
    white_end = 10
    black_end = 10
    w = white
    b = black
    while w:
        i = (w & -w).bit_length() - 1
        cone = white_table[i] & (black | 0x0081000000000000)
        if (cone & (cone - 1)) == 0:
            white_end = min(white_end, 7 - (i // 8))
        val += 20000 + table[i]
        if (1 << i) &~ black_control:
            val += 0.5 * table[i]
        if (1 << i) &~ white_friends:
            val -= 300
        w &= w - 1
    while b:
        i = (b & -b).bit_length() - 1 
        cone = black_table[i] & (white | 0x0000000000008100)
        if (cone & (cone - 1)) == 0:
            black_end = min(black_end, i // 8)
        val -= 20000 + table[63 - i]
        if (1 << i) &~ white_control:
            val -= 0.5 * table[63 - i]
        if (1 << i) &~ black_friends:
            val += 300
        b &= b - 1
    
    if white_end < 10 or black_end < 10:
        if whites_turn:
            if white_end <= black_end:
                return 100000.0 + val
            else:
                return -100000.0 + val
        else:
            if black_end <= white_end:
                return -100000.0 + val
            else:
                return 100000.0 + val
    return val

