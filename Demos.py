# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 15:18:03 2023

@author: alp.yildirim
"""

import gym


env = gym.make("Blackjack-v1", render_mode="human")
env.action_space.seed(42)

print(env.action_space)
print(env.observation_space)

observation, info = env.reset(seed=42)

for _ in range(1000):
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
    if terminated or truncated:
        observation, info = env.reset()

env.close()





