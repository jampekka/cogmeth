from copy import deepcopy
from collections import defaultdict
import random

import tictactoe

def temporal_difference(values, prev_state, new_state, reward):
    predicted_value = values[prev_state]
    if new_state is not None:
        observed_value = values[new_state] + reward
    else:
        observed_value = reward

    prediction_error = observed_value - predicted_value
    return prediction_error

def update_values(values, prev_state, new_state, reward, learning_rate):
    difference = temporal_difference(values, prev_state, new_state, reward)
    update = learning_rate*difference
    assert prev_state is not None
    values[prev_state] += update
    return values

class TemporalDifferencePlayer:
    def __init__(self, values, learning_rate=1.0, exploration_prob=0.0):
        self.learning_rate = learning_rate
        self.exploration_prob = exploration_prob
        self.values = values
        self.last_seen_state = None

    def __call__(self, board, turn):
        predicted_values = []
        for move in tictactoe.empty_squares(board):
            hypothesis = deepcopy(board)
            row, col = move
            hypothesis[row][col] = turn
            hypothesis = tuple(map(tuple, hypothesis))
            predicted_value = self.values[hypothesis]
            predicted_values.append((predicted_value, hypothesis, move))
        
        #random.shuffle(predicted_values)
        if random.random() > self.exploration_prob:
            predicted_value, new_board, move = max(predicted_values, key=lambda x: x[0])
        else:
            predicted_value, new_board, move = random.choice(predicted_values)
        
        reward = 0
        board_tuple = tuple(map(tuple, board))
        if self.last_seen_state is not None:
            self.values = update_values(self.values, self.last_seen_state,
                    new_board, reward, self.learning_rate)

        self.last_seen_state = new_board
         
        return move
    
    def game_over(self, player, result):
        reward = tictactoe.outcome_score(player, result)
        self.values = update_values(self.values, self.last_seen_state, None, reward, self.learning_rate)
        return self.values

def td_vs_random():
    random.seed(1)
    n_games = 100
    values = defaultdict(lambda: 0.0)
    #td_player = TemporalDifferencePlayer()
    random_player = tictactoe.random_player
    results = []
    for i in range(n_games):
        crosser = TemporalDifferencePlayer(values, learning_rate=0.1, exploration_prob=0.1)
        noughter = random_player
        
        result = tictactoe.play_game(crosser, noughter)
        
        reward = tictactoe.outcome_score(tictactoe.CROSS, result)
        results.append(reward)
        values = crosser.game_over(tictactoe.CROSS, result)
    
    board = tictactoe.new_board()
    turn = tictactoe.CROSS
    for move in tictactoe.empty_squares(board):
            hypothesis = deepcopy(board)
            row, col = move
            hypothesis[row][col] = turn
            hypothesis = tuple(map(tuple, hypothesis))
            predicted_value = values[hypothesis]
            print(predicted_value, hypothesis)
    import json
    with open(f"values_{n_games}.json", 'w') as f:
        json.dump(list(values.items()), f)
    print(sum(results)/len(results))
    
    
if __name__ == "__main__":
    td_vs_random()
