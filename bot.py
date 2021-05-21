import threes
import pygame
import time
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(units = 182, activation = None),
    tf.keras.layers.Dense(units = 32, activation = 'relu'),
    tf.keras.layers.Dense(units = 4, activation= 'relu')
    
    ])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

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

def normalize(x):
    x = x.astype(np.float32)
    x -= np.mean(x)
    x /= np.std(x)
    return x.astype(np.float32)

def discount_rewards(rewards):
    
    discounted_rewards = np.zeros_like(rewards)
    R = 0
    gamma = 0.8
    
    for i in reversed(range(len(rewards))):
        R = R*gamma + rewards[i]
        discounted_rewards[i] = R
        
    return normalize(discounted_rewards)
        
def choose_action(model, observation):
    
    logits = model(obs.astype(np.float32))
    
    action_tensor = tf.random.categorical(logits, num_samples = 1)
    action_number = action_tensor[0].numpy()[0]
    
    if action_number == 0:
        action = 'left' 
    
    elif action_number == 1:
        action =  'right'
    
    elif action_number == 2:
        action =  'up'

    elif action_number == 3:
        action =  'down'
        
    return action, action_number

def compute_loss(observations, actions, discounted_rewards):
    
    logits = model(observations.astype(np.float32))
    
    neg_logprop = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits = logits, labels = actions)
    
    loss = tf.reduce_mean(neg_logprop * discounted_rewards)
    
    return loss

def train(model, optimizer, obs, actions, discounted_rewards):
    
    with tf.GradientTape() as tape:
        
        loss = compute_loss(obs, actions, discounted_rewards)
        
    grads = tape.gradient(loss, model.trainable_variables)

    optimizer.apply_gradients(zip(grads, model.trainable_variables))
        
epochs = 30000
max_N = 1000
point_list = []
rewars_list = []

for j in tqdm(range(epochs)):
    
    board_memory = memory()
    board = threes.board(600, 300, 4)
    
    i = 0
    
    while True:
    
        obs = board.create_observation()
        
        obs = obs / (3*2 ** 4)
        obs = np.expand_dims(obs, axis = 0)
    
        action, action_number = choose_action(model, obs)
        board.input(action)
        reward = board.reward
    
        board_memory.update(obs, action_number, reward)
    
        i +=1
    
        if i == max_N:
            board.running = False
    
        if board.running == False:
        
            total_reward = np.sum(board_memory.rewards)
            discounted = discount_rewards(board_memory.rewards)
        
            train(model, optimizer, np.vstack(board_memory.observations), np.array(board_memory.actions), discounted)
            
            point_list.append(board.points)
            rewars_list.append(total_reward)
            
            break
        
pygame.quit()

random_data = np.loadtxt('random_points.dat')

plt.plot(np.linspace(0, epochs, epochs), np.mean(random_data)*np.ones(epochs))            
plt.plot(np.convolve(np.array(point_list), np.ones(1000)/1000, mode='valid'))
plt.show()   

   

    