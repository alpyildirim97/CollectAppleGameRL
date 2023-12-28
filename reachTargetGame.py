# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 21:58:01 2023

@author: alp.yildirim
"""

import pygame
import random
import time
from stable_baselines3 import PPO


WIDTH, HEIGHT = 630, 480
FPS = 60
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
BLUE = (0, 0, 255)
RED  = (255, 0, 0)

human_pos = []
target_pos = []

times_up = False
score = 0
gameOver = False



class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width): 
        super().__init__() 
  
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR) 
  
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height)) 
  
        self.rect = self.image.get_rect()
    
    def moveRight(self, pixels):
        if not self.rect.x >= 630 - self.image.get_size()[0]:
            self.rect.x += pixels

    def moveLeft(self, pixels):
        if not self.rect.x <= 0:
            self.rect.x -= pixels

    def moveUp(self, pixels):
        if not self.rect.y <= 0:
            self.rect.y -= pixels

    def moveDown(self, pixels):
        if not self.rect.y >= 480 - self.image.get_size()[1]:
            self.rect.y += pixels
            
    def detectCollision(self, targetRect):
        return self.rect.colliderect(targetRect)
        

def generateHuman():
    human = Sprite(BLUE, 30, 30) 
    human.rect.x = random.randint(50, 600)
    human.rect.y = random.randint(50, 400)
    return human

def generateApple():
    apple = Sprite(RED, 10, 10) 
    apple.rect.x = random.randint(50, 600)
    apple.rect.y = random.randint(50, 400)
    return apple
     

def update_apple():
    apple.rect.x = random.randint(50, 600)
    apple.rect.y = random.randint(50, 400) 
    
    

pygame.init()


pygame.display.set_caption('Find the Target')
display = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
all_sprites_list = pygame.sprite.Group() 
clock = pygame.time.Clock()

human = generateHuman()
apple = generateApple()


font = pygame.font.SysFont(None, 25)
def message_to_screen(msg):
    screen_text = font.render(msg, True, (255,255,255))
    display.blit(screen_text,(0,0))


  
all_sprites_list.add(human)
all_sprites_list.add(apple)
start_time = time.time()

while running:
    

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            break
        
    keys = pygame.key.get_pressed()       
    if keys[pygame.K_ESCAPE]:
        running = False
        break
    
    if keys[pygame.K_RIGHT]:
        human.moveRight(5)
        
            
    if keys[pygame.K_LEFT]:
        human.moveLeft(5)
            
    if keys[pygame.K_UP]:
        human.moveUp(5)
        
            
    if keys[pygame.K_DOWN]:
        human.moveDown(5)
                
    
    if human.detectCollision(apple):
        score = score + 1
        
        if score == 10:
            gameOver = True
        
        update_apple()
            
        pygame.display.update()
        
                
    #draw
    display.fill((67,70,75))
    message_to_screen(str(score))
    all_sprites_list.update()
    all_sprites_list.draw(display)
    
    if gameOver or time.time() - start_time >= 10:
        message_to_screen("Game is Over!")
        running = False
        
    pygame.display.update()
    clock.tick(FPS)
        
        
        
pygame.quit()        
        
        