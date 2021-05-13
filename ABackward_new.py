import numpy as np
import random as rr
import matplotlib.pyplot as plt
import sys
import timeit
from heapq import heapify, heappush, heappop

class Node():
    def __init__(self, y, x, value):
        self.value = 0 #search value
        self.position = [y, x]  
        self.parent = None
        self.next = None
        self.g = 0  
        self.h = 0
        self.closed = 0
    def priority(self):
        return ((100000 * (self.g + self.h)) - self.g)
    def f(self):
        return self.g + self.h
    def __lt__(self, other): # override less than for priority queue
        self_p = self.priority()
        other_p = other.priority()
        return self_p < other_p


class A_Backward:
    def __init__(self, maze, width, height):
        self.maze = maze
        self.height = height
        self.width = width

        self.start_position = None
        self.goal_position = None

    # Takes the txt files from backTracker and randGrid and converts it to numpy array
    def parseMaze(self): 
        self.maze = self.maze.strip().replace(' ', '').replace('\n', '')
        self.maze = np.array(list(self.maze), dtype=np.uint8)
        self.maze = self.maze.reshape((self.height, self.width))

    # Sets the start and goal positions for the maze, has options for randomly generated or hard coded
    def createAgentandTarget(self):
        self.parseMaze()

        counter = 0

        while counter != 2:

            y = rr.randint(0, self.height - 1)
            x = rr.randint(0, self.width - 1)
            
            if self.maze[y][x] == 0 and counter == 0:
                #this our start
                self.start_position = [y, x]
                self.maze[y][x] = 2
                counter += 1
                
            if self.maze[y][x] == 0 and counter == 1:
                #this is our goal
                self.goal_position = [y, x]
                self.maze[y][x] = 3
                counter += 1
        # Uncomment below and comment above (except for parseMaze) for predetermined start and goal points        
##        self.start_position = [14,25]
##        self.goal_position = [69,44]


    # Outputs the maze in an image.
    # Dark purple and black are unseen blocked and unblocked cells.
    # Orange cells are cells that the agent traverses through.
    # Light purple cells are the various start points
    # Pale yellow cells are the discovered blocked cells
    # Burnt orange cell is the goal
    def outputMaze(self):
        print(self.start_position)
        print(self.goal_position)
        plt.figure()
        plt.imshow(self.maze, cmap=plt.cm.magma, interpolation='nearest')
        plt.xticks([]), plt.yticks([])

        plt.savefig("solutions/maze_solution{0:0=2d}.png".format(50))

        plt.show()

    # The main for the Repeated A*
    def A_star(self):
        counter = 0

    # Set up 2D array to keep track of each cell using a Node object
        rows, cols = (self.height, self.width)
        nodes = [[0 for i in range(cols)] for j in range(rows)]
        
        yy = [-1, 1, 0, 0]  #down, up
        xx = [0, 0, 1, -1]  #right, left 

        y = self.start_position[0]
        x = self.start_position[1]

    # Creating start and goal nodes
        start = Node(y, x, 0)   
        print("start")
        print(start.position)
        nodes[y][x] = start

        y = self.goal_position[0]
        x = self.goal_position[1]

        goal = Node(y, x, 0)
        print("goal")
        print(goal.position)
        nodes[y][x] = goal
        
        goal.h = self.manhattan_distance(goal, start)

    # Identify any blocked cells adjacent to the starting position
        for s in range(4): #traverse the arrays yy and xx 
            new_y = start.position[0] + yy[s]  
            new_x = start.position[1] + xx[s]

            if new_y >= 0 and new_y < self.height and new_x >= 0 and new_x < self.width:
                if self.maze[new_y][new_x] == 1:
                    self.maze[new_y][new_x] = 5
                    
     # Main loop for Repeated A*               
        while start.position != goal.position: 
            counter += 1
            start.g = sys.maxsize 
            start.value = counter
            goal.g = 0 
            goal.value = counter
            
            opens = [] 
            heapify(opens)
            heappush(opens, goal)

            self.ComputePath(start, goal, opens, counter, nodes)

    # If the open list is empty, than we failed to find the goal
            if not opens:
                print("no path")
                return

    # Traverse the path found, checking for adjacent walls at each step, until we smack into a wall or hit goal, when we smack, change starting position
            while start.position != goal.position:
                for s in range(4): 
                    new_y = start.position[0] + yy[s]  
                    new_x = start.position[1] + xx[s]
                    if new_y >= 0 and new_y < self.height and new_x >= 0 and new_x < self.width:

                        if self.maze[new_y][new_x] == 1:
                            self.maze[new_y][new_x] = 5
    
                if self.maze[start.parent.position[0]][start.parent.position[1]] != 5:
                    start = start.parent
                    if self.maze[start.position[0]][start.position[1]] != 2:
                        self.maze[start.position[0]][start.position[1]] = 4

                else:
                    self.maze[start.position[0]][start.position[1]] = 2
                    break
    # When we break out of the loop we have succeeded
        print('poggers ' + str(counter))


    # Performs a Backward A* search         
    def ComputePath(self, start_point, goal_point, opens, counter, nodes):

        while opens and start_point.g > min(opens).f(): 
            s = heappop(opens)  
            if s.closed == counter: # checks to make sure not in closed list
                continue
            s.closed = counter # insert it into closed list
            expanded_list = self.new_succ(s, counter, nodes, start_point) #adds new successors to expanded list

    # Check if each successor should be added to the open list
            for a in range(len(expanded_list)):
                o = 0 # checks if it has been opened in this run yet
                if expanded_list[a].value < counter:
                    expanded_list[a].g = sys.maxsize
                    expanded_list[a].value = counter
                else:
                    o = 1
                if expanded_list[a].g > s.g + 1:
                    expanded_list[a].g = s.g + 1
                    expanded_list[a].parent = s
                    if o:
                        heapify(opens)
                    else:
                        heappush(opens, expanded_list[a])

    # Finds new successors and returns a list of them
    def new_succ(self, state, counter, nodes, start): 

        expanded = []  

        yy = [-1, 1, 0, 0]  #down, up
        xx = [0, 0, 1, -1]  #right, left
        
        for s in range(4):
            new_y = state.position[0] + yy[s]
            new_x = state.position[1] + xx[s]

            if new_y >= 0 and new_y < self.height and new_x >= 0 and new_x < self.width: ####check for inside maze border

                if self.maze[new_y][new_x] != 5: # checks if the cell is known to be blocked
                    if not nodes[new_y][new_x]: # if the node for the cell does not exist yet, we make it
                        expanded_point = Node(new_y, new_x, counter)
                        expanded_point.h = self.manhattan_distance(expanded_point, start)
                        nodes[new_y][new_x] = expanded_point
                    else:
                        expanded_point = nodes[new_y][new_x]

                    if expanded_point.closed < counter: # if the cell has already been expanded do not consider it
                        expanded.append(expanded_point)
        
        return expanded
    
    # Finds the Manhattan distance between two cells 
    def manhattan_distance(self, start_state, goal_state): 
        
        x0 = start_state.position[1]
        y0 = start_state.position[0]
        x = goal_state.position[1]
        y = goal_state.position[0]
        
        dx = abs(x0 - x)  
        dy = abs(y0 - y) 
        
        manhattan_distance = int(abs(dx + dy))
        
        return manhattan_distance
    

if __name__ == '__main__':


    height = 101
    width = 101


    with open('arrs/randGrid/00.txt', 'r') as my_file:
        maze = my_file.read()

    A_Backward_Maze = A_Backward(maze, height, width)

    A_Backward_Maze.createAgentandTarget()
    
    start = timeit.default_timer()
    
    A_Backward_Maze.A_star()
    
    A_Backward_Maze.outputMaze()
    
    stop = timeit.default_timer()

    print('Time: ', stop - start)
