import numpy as np
import matplotlib.pyplot as plt
import time
from gridworld import *
from qlearningagent import *
from sarsalearningagent import *

def moving_avg(x, N):
    '''
    Moving average function by AE
    '''
    
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def main():    
    # World settings
    width = 12
    height = 4
    start = (0, 3) # Coordinates of the start point
    goal = (11, 3) # Coordinates of the finish point
    cliff = [(i+1, 3) for i in range(10)] # Coordinates for the cliff
    
    # Learning rates
    exploration_rates = [0.1] # Values of epsilon
    gamma = 1
    alpha = 0.1
    
    # Set epsilon_decay to some real number between zero and one,
    # this will cause epsilon to decay per epoch
    epsilon_decay = False
    
    # Miscellaneous settings
    runs = 1 # Number of times to run the problems
    episodes = 500 # Number of episodes per run
    n_mavg = 10 # How many episodes should we calculate moving average over?
    display_world = False # Show text visualisation of agent moving around the world
    save_graphs = True # Save an output of the graph
    
    for i, epsilon in enumerate(exploration_rates):
        # Lists to store results of the runs
        qlearning_rewards = np.zeros(episodes)
        sarsa_rewards = np.zeros(episodes)
        
        for run in range(runs):
            print("#### RUN " + str(run) + "####")
            
            # Sarsa implementation
            sEnv = GridWorld(width, height, start, goal, cliff)
            sAgent = Agent(sEnv, start)
            sarsa = SARSA(sAgent, epsilon, gamma, alpha)
            SARSA_episode_rewards = sarsa.train(episodes, display_world, epsilon_decay)
            
            # QLearning implementation
            qEnv = GridWorld(width, height, start, goal, cliff)
            qAgent = Agent(qEnv, start)
            qLearning = QLearning(qAgent, epsilon, gamma, alpha)
            qLearning_episode_rewards = qLearning.train(episodes, display_world, epsilon_decay)
            
            # Append this runs results
            for episode in range(episodes):
                qlearning_rewards[episode] += qLearning_episode_rewards[episode]
                sarsa_rewards[episode] += SARSA_episode_rewards[episode]
        
        # Normalise the rewards
        qlearning_rewards /= runs
        sarsa_rewards /= runs
        
        # Calculate moving average for each implementation reward
        qLearning_mavg = moving_avg(qLearning_episode_rewards, n_mavg)
        SARSA_mavg = moving_avg(SARSA_episode_rewards, n_mavg)
        
        # Add these values to plots
        plt.figure(1)
        plt.plot(range(len(qLearning_mavg)), qLearning_mavg, label="Ɛ: " + str(epsilon))
        
        plt.figure(2)
        plt.plot(range(len(SARSA_mavg)), SARSA_mavg, label="Ɛ: " + str(epsilon))
        
        # Recreate the graph from the textbook
        if epsilon == 0.1:
            plt.figure(3)
            plt.plot(range(len(qLearning_mavg)), qLearning_mavg, label="Q-Learning")
            plt.plot(range(len(SARSA_mavg)), SARSA_mavg, label="SARSA")
      
    # Settings for plot 1
    plt.figure(1)
    plt.title("Analysis of Q-Learning for a range of Epsilons")
    plt.xlabel("Episodes")
    plt.ylabel("Sum of Rewards During Episode")
    plt.legend(loc="lower right", prop={'size': 10})
    if save_graphs: plt.savefig("./graphs/qlearning_analysis.png")
    
    # Settings for plot 2
    plt.figure(2)
    plt.title("Analysis of SARSA for a range of Epsilons")
    plt.xlabel("Episodes")
    plt.ylabel("Sum of Rewards During Episode")
    plt.legend(loc="lower right", prop={'size': 10})
    if save_graphs: plt.savefig("./graphs/sarsa_analysis.png")
    
    # Settings for plot 3
    plt.figure(3)
    plt.title("Q-Learning vs SARSA with Ɛ = 0.1")
    plt.xlabel("Episodes")
    plt.ylabel("Sum of Rewards During Episode")
    plt.legend(loc="lower right", prop={'size': 10})
    if save_graphs: plt.savefig("./graphs/qlearning_vs_sarsa.png")
    
    # Show the plots
    plt.show()
    
if __name__ == "__main__":
    main()