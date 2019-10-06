# K-Arm Bandit

This is an implementation of the Cliff Walking problem in Python.

## Prerequisites

Implementation was developed using Python 3.7.1

### Modules
* Numpy
* Matplotlib

## Running

Simply run the file *main.py*, you can modify the environment with the variables explained below

## Environment Variables
### World Settings
* width - how many squares wide is the gridworld
* height - how many squares tall is the gridworld
* start - A tuple stating the starting position of the agent (x, y)
* goal - A tupe stating the goal for the agent (x, y)
* cliff - A list of tuples stating the cliff positions

### Learning rates
* exploration_rates - A list containing values of epsilon
* gamma - Constant
* alpha - Constant

### Epsilon Decay
* epsilon_decay - Set this to true to cause epsilon to decay at each episode (Q-Learning only)

### Miscellaneous Settings
* runs - How many times should we run the problem?
* n_episodes - How many episodes should occur per run?
* n_mavg - How many episodes should we calculate the moving average over?
* display_world - Set to True to display a text output of the world after the agent moves
* save_graphs - Set to True to save the graphs