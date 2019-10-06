import numpy as np

# Constants for directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
markers = { UP: '^', DOWN: 'v', LEFT: '<', RIGHT: '>' }

# Holds information for each tile in the grid
class Tile():
    def __init__(self, x, y):
        self.state = (x, y)
        self.type = ""
        self.marker = ""
        self.qValues = { UP: 0, DOWN: 0, LEFT: 0, RIGHT: 0 }

# The world that our agent will interaction with
class GridWorld:
    def __init__(self, width, height, start, goal, cliff):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.cliff = cliff
        
        # Create grid for the world
        self.world = [[Tile(x, y) for x in range(self.width)] for y in range(self.height)]
        
        # Render the gridworld
        self._render()

    def _render(self):
        for y in range(self.height):
            for x in range(self.width):
                state = self.world[y][x].state
                if state == self.start:
                    self.world[y][x].type = "start"
                    self.world[y][x].marker = "S"
                elif state == self.goal:
                    self.world[y][x].type = "goal"
                    self.world[y][x].marker = "G"
                elif state in self.cliff:
                    self.world[y][x].type = "cliff"
                    self.world[y][x].marker = "C"
                else:
                    self.world[y][x].type = "tile"
                    self.world[y][x].marker = "o"
    
    def update(self, x, y, action, new_x, new_y):
        self.world[y][x].marker = markers[action]
        self.world[new_y][new_x].marker = "x"
       
    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                type = self.world[y][x].type
                if type == "start":
                    self.world[y][x].marker = "S"
                elif type == "goal":
                    self.world[y][x].marker = "G"
                elif type == "cliff":
                    self.world[y][x].marker = "C"
                else:
                    self.world[y][x].marker = "o"
    
    def reward(self, x, y):
        if self.world[y][x].type == "cliff":
            reward = -100
        else:
            reward = -1
        return reward

    def printWorld(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.world[y][x]
                print(tile.marker, end=" ")
            print()
        print()
    
    def printEndWorld(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.world[y][x].type == "cliff":
                    print("C", end=" ")
                elif self.world[y][x].type == "start":
                    print("S", end=" ")
                elif self.world[y][x].type == "goal":
                    print("G", end=" ")
                else:
                    values = []
                    for action in range(4):
                        values.append(self.world[y][x].qValues[action])
                    action = np.argmax(values)
                    print(markers[action], end=" ")
            print()
        print()