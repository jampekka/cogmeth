import sys
from collections import Counter
import random
import math

from copy import deepcopy

EMPTY = '.'
NOUGHT = 'O'
CROSS = 'X'

TIE = 'Tie'
CROSS_WINS = "X wins"
NOUGHT_WINS = "O wins"

class EndOfGame(BaseException):
    def __init__(self, result):
        self.result = result

def print_board(board, out=sys.stdout):
    for row in board:
        for col in row:
            out.write(col)
        out.write('\n')
    out.flush()

def other_mark(mark):
    if mark == CROSS: return NOUGHT
    if mark == NOUGHT: return CROSS
    raise AssertionError(f"Unknown mark {mark}")

def outcome_score(player, outcome):
    assert outcome in (TIE, CROSS_WINS, NOUGHT_WINS)
    if outcome == TIE: return 0
    if player == CROSS and outcome == CROSS_WINS: return 1
    if player == NOUGHT and outcome == NOUGHT_WINS: return 1

    return -1

MAX_SCORE = 1
MIN_SCORE = -MAX_SCORE

def check_triple(triple):
    uniques = set(triple)
    if len(uniques) != 1: return
    unique = next(iter(uniques))
    if unique == EMPTY: return

    if unique == CROSS:
        raise EndOfGame(CROSS_WINS)
    elif unique == NOUGHT:
        raise EndOfGame(NOUGHT_WINS)
    else:
        raise AssertionError(f"Unknown symbol on board: {unique}")

def check_result(board):
    N = len(board)
    # Check rows
    for row in board:
        check_triple(row)
    
    # Check columns
    for col_i in range(N):
        col = (row[col_i] for row in board)
        check_triple(col)

    # Check left-to-right diagonal
    left_diag = (board[i][i] for i in range(N))
    check_triple(left_diag)

    right_diag = (board[i][N - i - 1] for i in range(N))
    check_triple(right_diag)
    
    # Check full board
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return
    raise EndOfGame(TIE)

def get_result(board):
    try:
        check_result(board)
    except EndOfGame as e:
        return e.result
    return None

def new_board():
    return [[EMPTY]*3 for row in range(3)]

def play_game(crosser, noughter, on_move=lambda board, next_mark: None):
    board = new_board()
    
    while True:
        try:
            # Cross moves first
            on_move(board, CROSS)
            row, col = crosser(board, CROSS)
            assert board[row][col] == EMPTY
            board[row][col] = CROSS
            check_result(board)
            
            # Nought after
            on_move(board, CROSS)
            row, col = noughter(board, NOUGHT)
            assert board[row][col] == EMPTY
            board[row][col] = NOUGHT
            check_result(board)
        except EndOfGame as e:
            return e.result

def play_move(board, turn, move):
    row, col = move
    assert board[row][col] == EMPTY
    board[row][col] = turn
    result = get_result(board)
    return board, result   

def play_turn(board, turn, player):
    move = player(board, turn)
    return play_move(board, turn, move)

def greedy_player(board, mark):
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                move = (row, col)
                return move
    return move

def empty_squares(board):
    N = len(board)
    for row in range(N):
        for col in range(N):
            if board[row][col] == EMPTY:
                yield row, col


def random_player(board, turn):
    move = random.choice(list(empty_squares(board)))
    return move

def move_outcomes(board, mark, move):
    hypothesis = deepcopy(board)
    row, col = move
    hypothesis[row][col] = mark
    result = get_result(hypothesis)

    outcomes = Counter()
    if result is not None:
        outcomes[result] += 1
        return outcomes
    
    for move in empty_squares(hypothesis):
        outcomes += move_outcomes(hypothesis, other_mark(mark), move)
    return outcomes

def brutal_player(board, mark):
    best_outcome = -1
    print("Brutalizing!?!")
    for move in empty_squares(board):
        outcomes[move] = move_outcomes(board, mark, move)
    
    print(outcomes)

def least_bad_outcome(player, board, turn, move):
    hypothesis = deepcopy(board)
    row, col = move
    hypothesis[row][col] = turn
    result = get_result(hypothesis)
    
    # If this move ends the game, return the result's score
    if result is not None:
        return outcome_score(player, result)
    
    # Simulate the next turn, where the turn switches
    turn = other_mark(turn)
    moves = empty_squares(hypothesis)
    outcomes = (least_bad_outcome(player, hypothesis, turn, move) for move in moves)

    # If it's "our" turn, find the best certain value
    if player == turn:
        # Could do just return max(outcomes) but it's a lot slower due to not having
        # the early exit on max score
        value = MIN_SCORE
        for outcome in outcomes:
            if outcome >= value:
                value = outcome
                if value == MAX_SCORE: break
        return value
    # If it's "their" turn, find the worst certain value (best certain for them)
    else:
        # Could do min(outcomes) here
        value = MAX_SCORE
        for outcome in outcomes:
            if outcome <= value:
                value = outcome
                if value == MIN_SCORE: break
        return value

        return min(outcomes)


def least_bad_player(board, mark):
    # Cache for the first move, otherwise way too slow
    # for browser.
    moves = list(empty_squares(board))
    if len(moves) == 9:
        return (0, 0)

    best_outcome = -math.inf
    best_move = None

    for move in moves:
        outcome = least_bad_outcome(mark, board, mark, move)
        if outcome > best_outcome:
            best_outcome = outcome
            best_move = move
    
    return best_move
    
def greedy_game():
    result = play_game(greedy_player, greedy_player)
    print(result)

def random_game():
    results = Counter()
    for game in range(1):
        result = play_game(random_player, random_player)
        results[result] += 1
    print(results)

if __name__ == '__main__':
    #print("I'm main!?!")
    import inspect
    print(inspect.getsource(least_bad_outcome))
    random_game()
