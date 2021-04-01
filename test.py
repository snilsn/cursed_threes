import pygame
import time

from pygame.locals import(
    K_UP, 
    K_DOWN, 
    K_LEFT, 
    K_RIGHT,
    KEYDOWN)
pygame.init()

width = 1000
height = 1000

screen = pygame.display.set_mode([width, height])

running = True
x = 250
y = 250

dx = 5
dy = 5
f = ((0, 0, 255))

class blob():
    
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        
    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 5)
    
    def move(self, direction):
        
        if direction == 'left':
            if self.x > 0:
                self.x -=10
                
        if direction == 'right':
            if self.x < 1000:
                self.x += 10
        
        if direction == 'up':
            if self.y < 1000:
                self.y += 10
                
        if direction == 'down':
            if self.y > 0:
                self.y -= 10
        
bob = blob(x, y, screen)
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                direction = 'up'
                
            elif event.key == K_UP:
                direction = 'down'

            elif event.key == K_LEFT:
                direction = 'left'
             
            elif event.key == K_RIGHT:
                direction = 'right'
                bob.move(direction)
            
        else:
            direction = ''
    
    
    screen.fill((255, 255, 255))
    bob.move(direction)
    bob.draw()
    pygame.display.flip()
    
    time.sleep(0.1)
pygame.quit()
