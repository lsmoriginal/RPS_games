# learning checker

from random import randint

x = [randint(0,2) for i in range(10)]
move = [-1]

def agent(obs, config):
    move[0] += 1

    if move[0] == 10:
        move[0] = 0
    return x[move[0]]