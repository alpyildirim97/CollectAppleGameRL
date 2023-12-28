# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:06:10 2023

@author: alp.yildirim
"""

import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from reachTargetGameRL import *



PPO_path = os.path.join('Training', 'Saved_models')

env = reachTargetGameEnv()

model = PPO.load(PPO_path, env=env)

env.render_mode = 'human'
model.learn(total_timesteps=10000)

env.close()