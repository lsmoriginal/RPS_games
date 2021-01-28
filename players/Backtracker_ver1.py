my_moves = []
opp_moves = []

# myaction: reaction
action_reaction = {
    (0,): {0:0, 1:1, 2:0},
    (1,): {0:0, 1:0, 2:1},
    (2,): {0:1, 1:0, 2:0},
}

def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

def get_reaction(action) -> int:
    '''
    gets the reaction of the opponent, given my action history
    the input action is my action history
    '''
    reaction = action_reaction.get(action, None)
    while reaction == None:
        # remove the ealiest action
        action = action[1:]
        reaction = action_reaction.get(action, None)
        

    # return the most frequently played hand
    return max(reaction, key = reaction.get)
    

def update_actions(lastOpponentAction):
    opp_moves.append(lastOpponentAction)

    for i in range(len(my_moves) -1):
        move_combi = tuple(my_moves[i:-1])

        if move_combi not in action_reaction:
            action_reaction[move_combi] = {0:0, 1:0, 2:0}
        action_reaction[move_combi][lastOpponentAction] += 1
        

'''
opponent made actions based on my actions,
hence, record all permutation of my actions and the corresponding reactions
predict the next action using the most frequently played hand
'''

def agent(obs, config):
    if obs.step == 0:
        my_moves.append(0)
        return 0

    update_actions(obs.lastOpponentAction)
    opp_reaction = get_reaction(tuple(my_moves))

    my_moves.append(win_action(opp_reaction))
    return win_action(opp_reaction)