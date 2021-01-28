from tqdm import tqdm
from time import sleep

from kaggle_environments import make, evaluate


x = evaluate(
    "rps", 
    ["player_paper_lover.py", 
    "player_random_player.py"],
    configuration={"episodeSteps": 1000}
)

print(x)

# import os
# print(os.listdir())