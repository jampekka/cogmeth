import tictactoe
from browser import window, document
import editor

board_element = document.getElementById("board")
status_element = document.getElementById("status")
ai_move_element = document.getElementById("ai_move")

def update_board():
    global board, turn
    board_element.innerHTML = ''
    result = tictactoe.get_result(board)
    if result is None:
        status_element.innerHTML = f"{turn} to move"
    else:
        status_element.innerHTML = result
    for row_i, row in enumerate(board):
        row_element = document.createElement("tr")
        board_element.appendChild(row_element)
        for col_i, cell in enumerate(row):
            cell_element = document.createElement("td")
            if cell != tictactoe.EMPTY:
                cell_element.innerHTML = cell
            elif result is None:
                cell_element.bind("click", lambda *args, row=row_i, col=col_i: manual_move((row, col)))
            row_element.appendChild(cell_element)


def manual_move(move):
    global turn, board
    board, result = tictactoe.play_move(board, turn, move)
    turn = tictactoe.other_mark(turn)
    update_board()

def ai_move():
    global turn, board
    if tictactoe.get_result(board) is not None: return
    code = editor.editor.getValue()
    wtf = exec(code, tictactoe.__dict__, locals())
    move = get_move(board, turn)
    #board, result = tictactoe.play_turn(board, turn, tictactoe.least_bad_player)
    board, result = tictactoe.play_move(board, turn, move)
    turn = tictactoe.other_mark(turn)
    update_board()
ai_move_element.bind("click", lambda *args: ai_move())

def new_game():
    global turn, board
    turn = tictactoe.CROSS
    board = tictactoe.new_board()
    update_board()
document.getElementById("new_game").bind("click", lambda *args: new_game())

import inspect
from algos_gen import algorithms
default_algo = next(iter(algorithms.keys()))
editor.editor.setValue(algorithms[default_algo])
algos_el = document.getElementById("algos")
for name, src in algorithms.items():
    el = document.createElement("option")
    el.innerHTML = name
    algos_el.appendChild(el)
new_game()
#tictactoe.random_game()