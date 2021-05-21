import threes
import numpy as np
import matplotlib.pyplot as plt
import pygame
from tqdm import tqdm

epochs = 1000
point_list = []

for i in tqdm(range(epochs)):
    
    board = threes.board(600, 300, 4)

    while True:
        
        action = np.random.choice(['left', 'right', 'up', 'down'])
        board.input(action)
        
        if board.running == False:
            
            point_list.append(board.points)
            break

pygame.quit()
plt.plot(np.array(point_list))
np.savetxt('random_points.dat', np.array(point_list))

    