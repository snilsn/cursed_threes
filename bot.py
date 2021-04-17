import threes
import pygame
import time
import tensorflow as tf
import numpy as np

board = threes.board(600, 300, 4)

model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(units = 17),
    tf.keras.layers.Dense(units = 17),
    tf.keras.layers.Dense(units = 4, activation=None)
    ])

class memory():
    
    def __init__(self):
        self.clear()
        
    def clear(self):
        
        self.observations = []
        self.actions = []
        self.rewards = []

    def update(self, obs, action, reward):
        
        self.observations.append(obs)
        self.actions.append(action)
        self.rewards.append(reward)

def discount_rewards(rewards):
    
    discounted_rewards = np.zeros_like(rewards)

def choose_action(model, observation):
    
    logits = model.predict(obs)
    
    action_tensor = tf.random.categorical(logits, num_samples = 1)
    
    action_number = action_tensor[0].numpy()[0]
    
    if action_number == 0:
        action = 'left', 
    
    elif action_number == 1:
        action =  'right'
    
    elif action_number == 2:
        action =  'up'

    elif action_number == 3:
        action =  'down'
        
    return action, action_number

board_memory = memory()
i = 0
while board.running:
    
    obs = board.create_observation()
    obs = np.expand_dims(obs, axis = 0)
    
    action, action_number = choose_action(model, obs)
    board.input(action)
    reward = board.reward
    
    board_memory.update(obs, action_number, reward)
    
    i +=1
    
    if i == 250:
        board.running = False
    
    time.sleep(0.01)
    
pygame.quit()