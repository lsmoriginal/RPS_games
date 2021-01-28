from time import time 
import datetime as dt
from helper_competition import *
from helper_general import *
from multiprocessing import Pool

import pandas as pd  
import numpy as np
from tqdm.notebook import tqdm

import matplotlib.pyplot as plt
import seaborn as sns

class Competition():

    def __init__(self):
        '''
        @players: a dictionary of agents as values, and their names as keys
        '''
        self.players = recruit_players()
        self.schedule = competition_schedule(self.players)
        self.result = []
        self.competed = set()
    
    # not neccessary
    @property # getter
    def players(self):
        return self._players
    @players.setter
    def players(self, players):
        self._players =  players
    
    def compete(self, rounds = 5, runner = 'private'):
        '''
        @rounds: int specifying the number of rounds played during each match
        @runner: private or kaggle
        '''
        pool = Pool(10)

        self.players = recruit_players()
        self.schedule = competition_schedule(self.players)
        self.schedule = [each for each in self.schedule if each not in self.competed]

        config = {'rounds': rounds, 'runner': runner}
        run_match_args = [each + (config,) for each in self.schedule]

        results = []
        for result in tqdm(pool.imap_unordered(run_match, run_match_args), 
                        total = len(self.schedule), desc='Competition'):
                        results.append(result)
        pool.close()

        for each in results:
            # [p1, p2, p1.win, p2.win, draw]
            if each[2] != None:
                self.competed.add((each[0], each[1]))
                self.competed.add((each[1], each[0]))

        self.result.extend(results)
    
    def prize_prez(self):
        combined_result = pd.DataFrame(self.result,
                                        columns= ['P1', 'P2', 'P1 Score', 'P2 Score', 'Draw'])
        # combined_result['P1'] = combined_result.P1.apply(lambda x: x[7:-3])
        # combined_result["P2"] = combined_result.P2.apply(lambda x: x[7:-3])
        return combined_result
    
    def match_matrix(self):
        match_results = self.prize_prez()
        players_ranked = self.rank_players().Agent.tolist()
        scores = np.zeros((len(self.players), len(self.players)), dtype=np.int)

        for i, p1 in enumerate(self.players):
            for j, p2 in enumerate(self.players):
                if p1 == p2:
                    continue
                try:
                    scores[i , j] = match_results[(match_results.P1 == p1) & (match_results.P2 == p2)].iloc[0, 2]
                except IndexError:
                    scores[j , i] = scores[i , j] = match_results[(match_results.P1 == p2) & (match_results.P2 == p1)].iloc[0, 3]

        plt.figure(figsize=(6, 6))
        # Generate a mask for the upper triangle
        #mask = np.triu(np.ones_like(scores, dtype=bool),k=1)
        scores = pd.DataFrame(scores, columns=self.players,index=self.players)
        scores = scores.loc[players_ranked,:]
        sns.heatmap(
            scores, 
            annot=True, 
            cbar=False, 
            cmap=sns.light_palette("seagreen", as_cmap=True), 
            linewidths=1, 
            fmt="d",
            square = True,
            vmax=5
            # mask = mask
        )
        plt.xticks(rotation=90, fontsize=15)
        plt.yticks(fontsize=15)
        plt.show()



    def rank_players(self):
        match_results = self.prize_prez()
        players_scores = []

        for player in self.players:
            score = match_results[match_results.P1 == player]['P1 Score'].sum() +\
                match_results[match_results.P2 == player]['P2 Score'].sum()
            draw = match_results[(match_results.P1 == player) | (match_results.P1 == player)]['Draw'].sum()
            players_scores.append([player, score, draw])
        players_scores = pd.DataFrame(players_scores, columns=['Agent', 'Score', 'Draw'])
        return players_scores.sort_values('Score', ascending = 0)
        

""" 
theGame  = Competition()
theGame.compete()
print(theGame.result) 
"""