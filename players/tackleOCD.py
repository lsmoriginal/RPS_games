from collections import Counter

def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

opp_moves = []
# assumes that player likes to balance his move
def most_frequent(observation, configuration):
    if observation.step == 0:
        return 0
    
    opp_moves.append(observation.lastOpponentAction)
    fav_move = Counter(opp_moves).most_common()[-1][0]
    
    return win_action(fav_move)
