def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

def revenge_goldfish(observation, configuration):
    '''only retailiate the previous action'''

    if observation.step == 0:
        return 1
    return win_action(observation.lastOpponentAction)