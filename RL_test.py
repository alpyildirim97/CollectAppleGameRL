# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:36:53 2023

@author: alp.yildirim
"""

import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from reachTargetGameRL import *

Log_path = os.path.join('Training', 'logs')
PPO_path = os.path.join('Training', 'Saved_models')


env = reachTargetGameEnv()
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log = Log_path, ent_coef=0.07)


stop_callback = StopTrainingOnRewardThreshold(reward_threshold=180, verbose=1)
eval_callback = EvalCallback(env,
                             callback_on_new_best=stop_callback,
                             eval_freq=10000,
                             verbose=1)

env.render_mode = None
model.learn(total_timesteps=50000) 

env.close()

env.render_mode = 'human'
model.learn(total_timesteps=1000)

model.save(PPO_path)