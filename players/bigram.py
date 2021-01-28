
from helper_players import *
from collections import Counter

opp_move = [0, 1, 2]
# likes to play a 0 after a [0, 0]
bigram = {(0,0): [0]}

def agent(observation, configuration):
    if observation.step == 0:
        return 0
    
    opp_move.append(observation.lastOpponentAction)
    
    tuple_move = tuple(opp_move[-3:-1])
    if tuple_move in bigram:
        bigram[tuple_move].append(opp_move[-1])
    else:
        bigram[tuple_move] = [opp_move[-1]]
        
    tuple_move = tuple(opp_move[-2:])
    move_history = bigram.get(tuple_move, None)
    
    if move_history:
        return Counter(move_history).most_common()[0][0]
    else:
        return Counter(opp_move).most_common()[0][0]    
