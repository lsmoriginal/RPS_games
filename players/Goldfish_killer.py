
def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

my_moves = [0]
def agent(observation, configuration):
    
    opp_move = win_action(my_moves[-1])
    my_moves.append(win_action(opp_move))
    return my_moves[-1]
