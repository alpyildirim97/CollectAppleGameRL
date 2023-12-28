# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 22:09:05 2023

@author: alp.yildirim
"""

import random
import time
import pygame
import gym
from gym import spaces
import numpy as np
from stable_baselines3 import PPO


WIDTH, HEIGHT = 300, 300
ROW, COLUMN = 21, 16
FPS = 30
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
BLUE = (0, 0, 255)
RED  = (255, 0, 0)



class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width): 
        super().__init__() 
  
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR)
        self.punishMe = False
  
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height)) 
  
        self.rect = self.image.get_rect()
    
    def moveRight(self, pixels):
        if not self.rect.x >= WIDTH - self.image.get_size()[0]:
            self.rect.x += pixels
        else:
            self.punishMe = True

    def moveLeft(self, pixels):
        if not self.rect.x <= 0:
            self.rect.x -= pixels
        else:
            self.punishMe = True

    def moveUp(self, pixels):
        if not self.rect.y <= 0:
            self.rect.y -= pixels
        else:
            self.punishMe = True

    def moveDown(self, pixels):
        if not self.rect.y >= HEIGHT - self.image.get_size()[1]:
            self.rect.y += pixels
        else:
            self.punishMe = True
            
    def detectCollision(self, targetRect):
        return self.rect.colliderect(targetRect)


def generateHuman():
    human = Sprite(BLUE, 30, 30) 
    human.rect.x = random.randint(50, WIDTH - 50)
    human.rect.y = random.randint(50, HEIGHT -50)
    return human

def generateApple():
    apple = Sprite(RED, 10, 10) 
    apple.rect.x = random.randint(50, WIDTH - 50)
    apple.rect.y = random.randint(50, HEIGHT -50)
    return apple

def update_apple(appleSprite):
    appleSprite.rect.x = random.randint(50, WIDTH - 50)
    appleSprite.rect.y = random.randint(50, HEIGHT -50)



class reachTargetGameEnv(gym.Env):
    
    def __init__(self):
        self.render_mode = None
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=300, shape=(4,), dtype=np.float32)    
    
    
    def step(self, action):
        if self.human.detectCollision(self.apple):
            self.score = self.score + 1
                     
            update_apple(self.apple)
                                    
        if self.score == 10 or time.time() - self.startTime >= 10:
            self.done = True
            
  
        
        if action == 0:
           self.human.moveUp(10)
        elif action == 1:
            self.human.moveDown(10)
        elif action == 2:
            self.human.moveRight(10)
        elif action == 3:
            self.human.moveLeft(10)
                     
        self.observation = [self.human.rect.x, self.human.rect.y, self.apple.rect.x, self.apple.rect.y]
        self.observation = np.array(self.observation)    
        
        
        #Reward Function
        
        if self.done and self.score == 10:
            reward_a = 100
        elif self.done and self.score < 1:
            reward_a = -5
        else:
            reward_a = 0
            
        if self.prev_score < self.score:
            reward_b = 10
            self.prev_score = self.score
            self.timestep_passed_eating = 0
            self.valid_timestep_to_eat += 1
        else:
            reward_b = 0
            self.timestep_passed_eating += 1
            
            
        self.dist = abs(self.human.rect.x - self.apple.rect.x) + abs(self.human.rect.y - self.apple.rect.y)
        if self.dist > self.prev_dist:
            reward_c = -1
        elif self.dist < self.prev_dist:
            reward_c = 1
        else:
            reward_c = 0
        self.prev_dist = self.dist
        
        reward_d = -self.timestep_passed_eating // self.valid_timestep_to_eat
        
        if self.human.punishMe:
            reward_e = -2
            self.human.punishMe = False
        else:
            reward_e = 0
            
            
        self.reward = reward_a + reward_b + reward_c + reward_d + reward_e
        
        self.info = {}
        
        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, self.done, self.info
    
    def reset(self):
        self.human_pos = []
        self.target_pos = []
        self.score = 0
        self.prev_score = 0
        self.done = False
        self.startTime = time.time()
        
        self.all_sprites_list = pygame.sprite.Group()
        self.human = generateHuman()
        self.apple = generateApple()
        self.all_sprites_list.add(self.human)
        self.all_sprites_list.add(self.apple)
        
        self.observation = [self.human.rect.x, self.human.rect.y, self.apple.rect.x, self.apple.rect.y]
        self.observation = np.array(self.observation)
        
        
        self.dist = abs(self.human.rect.x - self.apple.rect.x) + abs(self.human.rect.y - self.apple.rect.y)
        self.prev_dist = self.dist
        self.valid_timestep_to_eat = ROW + COLUMN + 5
        self.timestep_passed_eating = 0
        
        
        if self.render_mode == 'human':
            pygame.init()
            pygame.display.set_caption('Snake RL')
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('Arial_bold', 25)
        
            self.render()
        
        return self.observation
    
    def render(self, render_mode='human'):
        
        self.display.fill((67,70,75))
        
        if self.done:
            self.message_to_screen("Game Over!")
        else:
            self.message_to_screen(str(self.score))
        
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.display)       
        pygame.display.update()
        self.clock.tick(FPS)

        # optional
        if self.done:
            time.sleep(0.5)
    
    def close(self):
        pygame.quit()
    
    def message_to_screen(self,msg):
        self.screen_text = self.font.render(msg, True, (255,255,255))
        self.display.blit(self.screen_text,(0,0))
