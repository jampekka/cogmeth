import tictactoe
from browser import window, document
import editor
import json
from collections import defaultdict
from copy import deepcopy

board_element = document.getElementById("board")
status_element = document.getElementById("status")
ai_move_element = document.getElementById("ai_move")

rls = {
        "10k iters": "values_10000.json",
        "100 iters": "values_100.json",
        "1k iters": "values_1000.json",
        "100k iters": "values_100000.json",
        }
rls_el = document.getElementById("rl")

for name, src in rls.items():
    el = document.createElement("option")
    el.innerHTML = name
    rls_el.appendChild(el)


board = None
board_values = None
def update_board():
    global board, turn
    if board is None: return
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
            
            hypothesis = deepcopy(board)
            hypothesis[row_i][col_i] = turn
            try:
                value = board_values[repr(hypothesis)]
                color = window.d3.interpolatePiYG((value + 1)/2)
                if turn == tictactoe.CROSS:
                    cell_element.style.backgroundColor = color
            except KeyError:
                pass
            row_element.appendChild(cell_element)

def update_values():
    global board_values
    f = rls[rls_el.value]
    board_values = json.load(open(f, "r"))
    board_values = {repr(k): v for k, v in board_values}
    update_board()
update_values()
rls_el.bind("change", lambda ev: update_values())

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

import inspect
from algos_gen import algorithms
default_algo = next(iter(algorithms.keys()))
editor.editor.setValue(algorithms[default_algo])
algos_el = document.getElementById("algos")
for name, src in algorithms.items():
    el = document.createElement("option")
    el.innerHTML = name
    algos_el.appendChild(el)

def set_algo(ev):
    editor.editor.setValue(algorithms[algos_el.value])
algos_el.bind("change", set_algo)

def new_game():
    global turn, board
    turn = tictactoe.CROSS
    board = tictactoe.new_board()
    update_board()
document.getElementById("new_game").bind("click", lambda *args: new_game())



new_game()
#tictactoe.random_game()
