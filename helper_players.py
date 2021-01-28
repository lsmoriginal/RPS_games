from helper_general import *

def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

def match_result(player1_action, player2_action):
    '''
    1 for player 1
    2 for player 2
    0 for draw
    '''
    if player1_action == player2_action:
        return 0
    elif player1_action == win_action(player2_action):
        return 1
    else:
        return 2
    