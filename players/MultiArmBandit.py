def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3

class PerformanceTracker():

    def __init__(self):
        self.my_moves = []
        self.opp_moves = []
        self.score_hist = []
        # win,lose, draw
        self.scores = {'win':0, 'lose':0, 'draw':0}

    def performance_update(self):
        '''
        win == 1
        lose == -1
        draw == 0
        '''
        status = 0
        if self.my_moves[-1] == self.opp_moves[-1]:
            status = 0
            self.scores['draw'] += 1
        elif self.my_moves[-1] == win_action(self.opp_moves[-1]):
            status = 1
            self.scores['win'] += 1
        else:
            # lost the previous game
            status = -1
            self.scores['lose'] += 1
        
    def record_move(self, move):
        '''
        agent's own move is always recorded first,
        followed by the recording of the move in the next round
        '''
        if len(self.my_moves) == len(self.opp_moves):
            self.my_moves.append(move)
            # exit the game
            return
        else:
            self.opp_moves.append(move)

        # performance update
        self.performance_update()


class Agent(PerformanceTracker)