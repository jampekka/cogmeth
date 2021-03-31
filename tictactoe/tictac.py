from copy import copy

EMPTY = 'E'
board = [EMPTY]*3
marks = ['X', 'O']
turn = 'X'

def free_squares(board):
    for i in range(len(board)):
        if board[i] == EMPTY: yield i

def other_turn(turn):
    if turn == 'X': return 'O'
    if turn == 'O': return 'X'


def get_result(board):
    board = ''.join(board)
    if 'XX' in board: return 'X'
    if 'OO' in board: return 'O'
    if EMPTY not in board: return EMPTY
    return None

def build_tree(board, turn, move):
    hypo = copy(board)
    hypo[move] = turn
    level = len(list(free_squares(hypo)))
    
    #name = ''.join(board)
    #label = board.replace(EMPTY, '-')
    #print(f"{name} [label={label}];")
    print(f"{''.join(board)} -> {''.join(hypo)};")
    result = get_result(board)
    if result is not None:
        return
        
    turn = other_turn(turn)
    for move in free_squares(hypo):
        build_tree(hypo, turn, move)

print("digraph {")
for move in free_squares(board):
    build_tree(board, turn, move)
print("}")
