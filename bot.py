import threes
import pygame
import time
import tensorflow as tf
import numpy as np

board = threes.board(600, 300, 4)

model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(units = 32),
    tf.keras.layers.Dense(units = 4, activation=None)
    ])

def choose_action(model, observation):
    
    logits = model.predict(obs)
    
    action_tensor = tf.random.categorical(logits, num_samples = 1)
    
    action_number = action_tensor[0].numpy()[0]
    
    if action_number == 0:
        return 'left'
    
    elif action_number == 1:
        return 'right'
    
    elif action_number == 2:
        return 'up'

    elif action_number == 3:
        return 'down'

for i in range(10):
    
    obs = board.create_observation()
    obs = np.expand_dims(obs, axis = 0)
    
    action = choose_action(model, obs)
    print(action)
    board.move(action)
    time.sleep(0.1)
    
pygame.quit()