import numpy as np
import time

# Constants for directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Agent():
    def __init__(self, env, start):
        self.env = env
        self.start = start
        self.x = start[0]
        self.y = start[1]
        self.env.world[self.y][self.x].marker = "x"
        
    def move(self, action):
        if action == UP:
            if self.y > 0:
                self.y -= 1
        elif action == DOWN:
            if self.y < self.env.height - 1:
                self.y += 1
        elif action == LEFT:
            if self.x > 0:
                self.x -= 1
        elif action == RIGHT:
            if self.x < self.env.width - 1:
                self.x += 1
    
    def reset(self):
        self.x = self.start[0]
        self.y = self.start[1]
        self.env.world[self.y][self.x].marker = "x"
        self.env.reset()
    
class QLearning():
    def __init__(self, agent, epsilon, gamma, alpha):
        self.agent = agent
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
    
    def get_qvalue(self, x, y, action):
        return self.agent.env.world[y][x].qValues[action]
    
    def set_qvalue(self, x, y, action, Q):
        self.agent.env.world[y][x].qValues[action] = Q
    
    def max_state_value(self, x, y):
        values = []
        for action in range(4):
            values.append(self.get_qvalue(x, y, action))
        max_state_value = np.max(values)
        return max_state_value

    def update_qvalue(self, x, y, next_x, next_y, action, reward):
        Q = self.get_qvalue(x, y, action)
        Q += self.alpha * (reward + (self.gamma * self.max_state_value(next_x, next_y)) - Q)
        self.set_qvalue(x, y, action, Q)
    
    def get_best_action(self, x, y):
        values = []
        for action in range(4):
            values.append(self.get_qvalue(x, y, action))
        best_action = np.argmax(values)
        return best_action
    
    def get_action(self, x, y, epsilon_decay, episode):
        if epsilon_decay == True:
            epsilon = self.epsilon / np.sqrt(episode + 1)
        else:
            epsilon = self.epsilon
        
        if np.random.rand() < epsilon:
            action = np.random.randint(4)
        else:
            action = self.get_best_action(x, y)
        return action
    
    def train(self, episodes, display_world, epsilon_decay):
        episode_rewards = np.zeros(episodes)
        for episode in range(episodes):
            episode_reward = 0
            if display_world  == True: self.agent.env.printWorld()
            reached_goal = False
            while reached_goal == False:
                # Determine agents action
                action = self.get_action(self.agent.x, self.agent.y, epsilon_decay, episode)
                
                # Take the current state of the agent
                cur_x = self.agent.x
                cur_y = self.agent.y
                
                # Perform the action
                self.agent.move(action)
                
                # Determine the reward from this action
                reward = self.agent.env.reward(self.agent.x, self.agent.y)
                episode_reward += reward
                
                # Update the Q Values
                self.update_qvalue(cur_x, cur_y, self.agent.x, self.agent.y, action, reward)
                            
                # Update the world
                self.agent.env.update(cur_x, cur_y, action, self.agent.x, self.agent.y)
                
                if display_world == True:
                    print("[EPISODE " + str(episode + 1) + "] Action " + str(action) + " resulted in reward " + str(reward) + "\nTotal reward for this episode " + str(episode_reward))
                    # Print the updated world
                    self.agent.env.printWorld()
                
                # Check if new position is a cliff, if it is we reset the agent
                if self.agent.env.world[self.agent.y][self.agent.x].type == "cliff":
                    print("ERROR: Hit cliff")
                    self.agent.reset()
                    # time.sleep(.25)
                # Check if the new position is the goal, if it is we're done with this episode
                elif self.agent.env.world[self.agent.y][self.agent.x].type == "goal":
                    print("[EPSIODE " + str(episode + 1) + "] GOAL REACHED! Total reward: " + str(episode_reward))
                    self.agent.reset()
                    reached_goal = True
                    # time.sleep(1)
                    
            episode_rewards[episode] += episode_reward
            
#    if display_world == True:
        print("################")
        print("# OPTIMAL PATH #")
        print("################")
        self.agent.env.printEndWorld()
            
        return episode_rewards