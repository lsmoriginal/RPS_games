
def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

mymoves = [0]
oppmoves  = []

def psycholoy_method(observation, configuration):
    opp_last_act = observation.lastOpponentAction if observation.step != 0 else 0
    oppmoves.append(opp_last_act)
    
    if win_action(oppmoves[-1]) == mymoves[-1]:
        # if you win the previous round
        mymoves.append(win_action(mymoves[-1]))
        # win yourself the next round
        return win_action(mymoves[-1])
    else:
        mymoves.append(win_action(opp_last_act))
        return win_action(opp_last_act)
