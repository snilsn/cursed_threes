import threes
import random as rd
import pygame
import time
import tensorflow as tf

board = threes.board(600, 300, 4)

for i in range(100):
    board.input(rd.choice(['left', 'right', 'up', 'down'] ))
    time.sleep(0.01)
    
pygame.quit()