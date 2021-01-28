from random import randint
from time import sleep
from kaggle_environments.agent import build_agent
import pandas as pd
from time import perf_counter
import matplotlib.pyplot as plt

def get_agent(raw):
    return build_agent(raw, [],[])[0]

def win_action(action):
    '''
    return the action that would win the given action
    '''
    return (action + 1)%3


class observation():
    def __init__(self):
        self.step = 0
        self.lastOpponentAction = None
        
class configurations():
    def __init__(self):
        self.signs = 3

game_signs = {
    0: 'Rock',
    1: 'Paper',
    2: 'Scissors',
}


def pvp(p1_name, p2_name, episodes = 1000):
    p1 = get_agent(p1_name)
    p2 = get_agent(p2_name)

    p1_obs = observation()
    p2_obs = observation()
    config = configurations()

    # p1_move, p2_move, p1_time, p2_time p1_score, p2_score, draw
    results = [
        [1,1,1,1,1,1,1]
    ]
    
    for ithGame in range(episodes):
        data = [0,0,0,0,0,0,0]
        
        p1_start = perf_counter()
        p1_move = p1(p1_obs, config)
        p1_time = perf_counter() - p1_start
        p2_start = perf_counter()
        p2_move = p2(p2_obs, config)
        p2_time = perf_counter() - p2_start
        
        data[2] = p1_time
        data[3] = p2_time

        p1_obs.step += 1
        p1_obs.lastOpponentAction = p2_move
        data[0] = p1_move

        p2_obs.step += 1
        p2_obs.lastOpponentAction = p1_move
        data[1] = p2_move

        if p1_move == p2_move:
            data[6] = 1
        elif p1_move == win_action(p2_move):
            data[4] = 1
        else:
            data[5] = 1
        results.append(data)
    
    results = pd.DataFrame(results, columns = ["p1_mve", "p2_move","p1_time", "p2_time", "p1_score","p2_score","draw"])
    results['p1_total'] = results.p1_score.cumsum()
    results['p2_total'] = results.p2_score.cumsum()
    results['draw_total'] = results.draw.cumsum()
    results['total'] = results.p1_total + results.p2_total + results.draw_total 
    results['p1_score_perc'] = 100 * results.p1_total/results.total
    results['p2_score_perc'] = 100 * results.p2_total/results.total
    results['draw_score_perc'] = 100 * results.draw_total/results.total
    results['score_ratio'] = 100 * results.p1_total / (results.p1_total + results.p2_total)
    
    return results

def visualise_results(results):
    fig, ax = plt.subplots()
    results.p1_score_perc.plot()
    results.p2_score_perc.plot(color = 'red', alpha = 0.2)
    results.draw_score_perc.plot(color = 'green')
    results.score_ratio.plot(color = 'purple')
    ax.legend(['P1','P2', 'Draw', "Score Ratio"])
    display(results.iloc[-1,-8:])

def evaluate(method = 'rps', agents =  [], configuration = {"episodeSteps": 1000}):
    results = pvp(agents[0], agents[1], configuration["episodeSteps"]) 
    p1_score =  results.p1_score.sum()
    p2_score =  results.p2_score.sum()
    scores = [p1_score,p2_score]
    base = min(scores)
    scores = [score - base for score in scores]
    base = max(scores)
    for i in range(2):
        if scores[i] == 0:
            scores[i] = -base

    return [list(scores),]
