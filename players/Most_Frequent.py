
from helper_players import *
from collections import Counter

opp_moves = []
# play according to 
def most_frequent(observation, configuration):
    if observation.step == 0:
        return 0
    
    opp_moves.append(observation.lastOpponentAction)
    fav_move = Counter(opp_moves).most_common()[0][0]
    
    return win_action(fav_move)
