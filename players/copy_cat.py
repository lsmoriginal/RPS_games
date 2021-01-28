def copy_cat(observation, configuration):
    if observation.step == 0:
        return 1
    return observation.lastOpponentAction