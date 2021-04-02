import pygame
import time
import numpy as np

from pygame.locals import(
    K_UP, 
    K_DOWN, 
    K_LEFT, 
    K_RIGHT,
    K_ESCAPE,
    K_n,
    KEYDOWN)

class board():
    
    def __init__(self, height, width, number):
        
        pygame.init()
        
        self.font_name = pygame.font.get_default_font()
        self.size = 40
        self.font = pygame.font.Font(self.font_name, self.size)
        
        self.colors = {3*2 ** i: (100, 100, 100) for i in range (0, 10)}
        self.colors.update({0: (255, 255, 255)})
        self.colors.update({1:(0, 0, 255)})
        self.colors.update({2:(255, 0, 0)})
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height + 100])
        self.screen.fill((255, 255, 255))
        self.number = number
        self.values = np.zeros((number, number))
        
        self.rng = np.random.default_rng()
        self.spawn_numbers = [1, 2, 3, 6, 12, 24]
        self.weights = [0.4, 0.4, 0.1, 0.06, 0.02, 0.02]
        
        for n in range(9):
            
            i = self.rng.integers(0, self.number)
            j = self.rng.integers(0, self.number)
            
            self.values[i, j] = self.rng.choice(self.spawn_numbers, p = self.weights)
        
        self.generate_next_number()
        self.show()
    
    def generate_next_number(self):
        
        self.next = self.rng.choice(self.spawn_numbers, p = self.weights)
    
    def shift_left(self):
        
        copy = np.copy(self.values)
        spawn_index_list = []
            
        for j in range(self.number):
            for i in range(self.number):
                if i < self.number - 1:
                    
                    if self.values[i, j] == 0:
                        
                        if self.values[i + 1, j] != 0:
                            spawn_index_list.append(j)
                            
                            for k in range(self.number - i):
                            
                                if i+k+1 == self.number:
                                    self.values[i + k, j] = 0
                                
                                else:
                                    self.values[i + k, j] = copy[(i+k+1), j]
                            break
                    
                    if self.values[i, j] == self.values[i+1, j] and self.values[i, j] != 1 and self.values[i, j] != 2:
                        
                        spawn_index_list.append(j) 
                        self.values[i, j] *=2
                        
                        for k in range(self.number - (i + 1)):
                        
                            if i+k+2 == self.number:
                                self.values[i + k + 1, j] = 0
                            
                            else:
                                self.values[i+k+1, j] = copy[(i+k+2), j]
                                           
                        break
                    
                    if self.values[i, j] == 1 and self.values[i+1, j] == 2:
                        
                        spawn_index_list.append(j) 
                        self.values[i, j] = 3
                        
                        for k in range(self.number - (i + 1)):
                        
                            if i+k+2 == self.number:
                                self.values[i + k + 1, j] = 0
                            
                            else:
                                self.values[i+k+1, j] = copy[(i+k+2), j]
                                           
                        break
                    
                    if self.values[i, j] == 2 and self.values[i+1, j] == 1:
                        
                        spawn_index_list.append(j) 
                        self.values[i, j] = 3
                        
                        for k in range(self.number - (i + 1)):
                        
                            if i+k+2 == self.number:
                                self.values[i + k + 1, j] = 0
                            
                            else:
                                self.values[i+k+1, j] = copy[(i+k+2), j]
                                           
                        break
                    
        if len(spawn_index_list) != 0:
            index = np.random.choice(spawn_index_list)
            self.values[self.number-1, index] = self.next
            self.generate_next_number()
    
    def input(self, key):
        
        if key == 'left':
            
            self.shift_left()
            
        if key == 'right':
            
            self.values = np.flip(self.values, axis=0)
            self.shift_left()
            self.values = np.flip(self.values, axis=0)
                    
        if key == 'up':
            
            self.values = np.transpose(self.values)
            self.shift_left()
            self.values = np.transpose(self.values)
                    
        if key == 'down':
        
            self.values = np.transpose(self.values)
            self.values = np.flip(self.values, axis=0)
            self.shift_left()
            self.values = np.flip(self.values, axis=0)
            self.values = np.transpose(self.values)            
                    
        self.show()
    
    def points(self):
        return(int(np.sum(self.values)))
    
    def show(self):

        width_ratio = self.width/self.number
        height_ratio = self.height/self.number
        
        for i in range(self.number):
            for j in range(self.number):
        
                    rect = pygame.Rect(i*width_ratio, j*height_ratio, width_ratio-2, height_ratio-2)
                    pygame.draw.rect(self.screen, self.colors[self.values[i, j]], rect)
                    number = self.font.render(str(int(self.values[i, j])), True, (0, 0, 0))
                    self.screen.blit(number, (i*width_ratio + 1, j*height_ratio+ 1))
        
        points_rect = pygame.Rect(0, self.height , self.width, 100)
        points = self.points()      
        points_img = self.font.render('Points:' + str(points), True, (0, 0, 0))
        next_img = self.font.render('Next: ' + str(self.next), True, (0, 0, 0))
        
        pygame.draw.rect(self.screen, (255, 255, 255), points_rect)
        self.screen.blit(points_img, (1, self.height + 5))
        self.screen.blit(next_img, (1, self.height + 45))
         
        pygame.display.flip()

if __name__ == '__main__':
    
    test = board(500, 300, 4)
    running = True

    while running:
    
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYDOWN:
            
                if event.key == K_ESCAPE:
                    running = False
                
                elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                    name = pygame.key.name(event.key)
                    test.input(name)
                
                elif event.key == K_n:
                    test = board(500, 300, 4)
            
            time.sleep(0.1)
    
    pygame.quit() 
