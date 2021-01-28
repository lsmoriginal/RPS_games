from random import randint
my_moves = []
opp_moves = []
memory_len = 20
losing_history = []
score_board = [0, 0]

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
    action = action[-memory_len:]

    reaction = action_reaction.get(action, None)
    while reaction == None:
        # remove the ealiest action
        action = action[1:]
        reaction = action_reaction.get(action, None)
        

    # return the most frequently played hand
    return max(reaction, key = reaction.get)
    

def update_actions(lastOpponentAction):
    opp_moves.append(lastOpponentAction)

    # update the lost_history
    losing_history.append(1 if win_action(my_moves[-1]) == opp_moves[-1] else 0)
    if win_action(my_moves[-1]) == opp_moves[-1]:
        score_board[1] += 1
    elif win_action(opp_moves[-1]) == my_moves[-1]:
        score_board[0] += 1

    for i in range(len(my_moves) -1):
        move_combi = tuple(my_moves[i:-1])

        if move_combi not in action_reaction:
            action_reaction[move_combi] = {0:0, 1:0, 2:0}
        action_reaction[move_combi][lastOpponentAction] += 1

        if win_action(my_moves[-1]) == opp_moves[-1]:
            # if I lost last round
            # the opp is less likely to play the same move a again
            # extra award to use this action
            action_reaction[move_combi][win_action(lastOpponentAction)] += 2



def agent(obs, config):
    '''
    strategy changer is build upon Backtracker

    but mornitor's its own performance
    if its score drop to certain difference, then agent starts to play 
    randomly to balance the score.  
    '''
    if obs.step == 0:
        my_moves.append(0)
        return 0
    if len(my_moves) > memory_len:
        del my_moves[0]
    update_actions(obs.lastOpponentAction)

    if score_board[0] < score_board[1]:
        opp_reaction = randint(0,2)
    else:
        opp_reaction = get_reaction(tuple(my_moves))

    my_moves.append(win_action(opp_reaction))
    return win_action(opp_reaction)
