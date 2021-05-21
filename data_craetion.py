import numpy as np
import threes
import pygame

from pygame.locals import(
    K_UP, 
    K_DOWN, 
    K_LEFT, 
    K_RIGHT,
    K_ESCAPE,
    K_n,
    KEYDOWN)

board = threes.board(600, 300, 4)

running = True

while running:
    
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            
            if event.key in  [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                name = pygame.key.name(event.key)
                
                if name == 'left':
                    action = 0 
                elif name == 'right':
                    action =  1
                elif name == 'up':
                    action = 2
                elif name ==  'down':
                    action = 4
                
                obs = board.create_observation()
                new_entry = np.array([obs, action])
                
                with open('data.dat', 'a') as f:
                    
                    f.write("\n")
                    np.savetxt(f, new_entry, delimiter=',')
                
                board.input(name)
                
            elif event.key == K_n:
                
                board = threes.board(600, 300, 4)
                
            elif event.key == K_ESCAPE:
                
                running = False
                
pygame.quit()