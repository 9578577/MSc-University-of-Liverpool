import numpy as np
import matplotlib.pyplot as plt

# Colours for plots
colours = ['g', 'r', 'b']

# Paramters 
k = 10 # The number of bandits in the problem
exploration_rates = [0, 0.01, 0.1] ## IF YOU ADD MORE VALUES, ADJUST COLOURS ABOVE ## 
runs = 2000 # The number of times to run the problem
steps = 1000 # The number of steps to take per run
save_graphs = True # Set to True to save the graph

# Start the K-Bandit problem
for i, epsilon in enumerate(exploration_rates):
    print("Starting the k-arm bandit problem with Ɛ = " + str(epsilon))
    
    # Lists to store average a optimal rewards over n runs
    average_rewards = np.zeros(steps)
    optimal_actions = np.zeros(steps)
    
    for run in range(runs):
        # Set Qstar values and initialise Q (estimates) and N (number of times each action is taken)
        Qstar = np.random.randn(k)
        Q = np.zeros(k)
        N = np.zeros(k)

        for step in range(steps):
            
            # Determine which action to takerzrrarra
            if (np.random.rand() < epsilon):
                # Explore the available options
                action = np.random.randint(k)
            else:
                # Exploit the best action
                action = np.argmax(Q)
            
            # Calculate the reward
            reward = np.random.normal(Qstar[action], 1)
            
            # Update values for N and Q
            N[action] += 1
            Q[action] += (1 / (N[action] + 1)) * (reward - Q[action])
            
            # Update our average_rewards
            average_rewards[step] += reward
            
            # Check if our action was optimal
            if (action == np.argmax(Qstar)):
                optimal_actions[step] += 1

    # Normalise average_rewards and optimal_rewards over n runs
    average_rewards /= runs
    optimal_actions /= runs
    optimal_actions *= 100
    
    # Append these results to our graphs
    plt.figure(1)
    plt.plot(range(steps), average_rewards, color=colours[i], label="Ɛ: " + str(exploration_rates[i]))
    plt.figure(2)
    plt.plot(range(steps), optimal_actions, color=colours[i], label="Ɛ: " + str(exploration_rates[i]))

# Plot Figure 1 - Average Reward
plt.figure(1)
plt.xlabel("Steps")
plt.ylabel("Average Reward")
plt.legend(loc="lower right", prop={'size': 10})
if save_graphs == True: plt.savefig("average_reward.png")

# Plot Figure 2 - % Optimal Reward
plt.figure(2)
plt.xlabel("Steps")
plt.ylabel("% Optimal Action")
plt.legend(loc="lower right", prop={'size': 10})
if save_graphs == True: plt.savefig("pct_optimal_reward.png")
plt.show()