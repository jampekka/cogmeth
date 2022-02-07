# Brython seems to have buggy inspect. Let's precompute
# the algos here

import tictactoe
from inspect import getsource
from pprint import pprint
#source = getsource
from copy import copy
import re

# Megahack!
def source(func):
    func = copy(func)
    src = getsource(func)
    src = re.sub(r"def\s+[^(]*", "def get_move", src)
    print(src)
    #src = '\n'.join(src)
    return src

algos = {
        "Minimax": source(tictactoe.least_bad_player),
        "Monte carlo": source(tictactoe.pure_mcts_player),
        "Random": source(tictactoe.random_player),
        "Stupid": source(tictactoe.greedy_player),
        "Custom": source(tictactoe.random_player),
        }

out = open("algos_gen.py", 'w')
out.write("algorithms = ")
out.write(repr(algos))
