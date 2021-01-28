import os
from kaggle_environments import evaluate as kaggle_eval
from OneVOne import evaluate as private_eval
from tqdm.notebook import tqdm

def recruit_players():
    players = os.listdir("players/")
    # players = list(player for player in players if player[:6] == 'player')
    players = list(player for player in players if player[-3:] == '.py')
    return players

def competition_schedule(players):
    '''
    @players: list of players

    return a list a tuples,
    each a tuple of two players
    '''
    players = players.copy()
    schedule = []

    while len(players) > 1:
        player1 = players.pop()
        for player2 in players:
            schedule.append((player1, player2))
    return schedule

evaluator = {
    'private': private_eval,
    'kaggle': kaggle_eval
}

def run_match(players):
    '''
    return score in [p1, p2, p1.win, p2.win, draw] format
    '''
    player1, player2, config = players 
    scores = [0,0,0]
    evaluate = config['runner']

    location = "players/"
    for game in tqdm(range(config['rounds']), leave = False):
        result =  evaluate(
            "rps", 
            [location + player1, location + player2],
            configuration={"episodeSteps": 1000})
        
        result = result[0][0]
        try:
            if abs(result) < 20:
                scores[2] += 1
            elif result > 0:
                scores[0] += 1
            else:
                scores[1] += 1
        except TypeError:
            scores = (-1, -1, -1)
    

    result = players[:-1] + tuple(scores)
    return result







