import copy
import math
import os
import sys

"""
Changes by Erika Feb 25
    - added Path List to Node Class
    - changed calculate_function operation from * to +
    - removed distance variable (bcs cost is counted from degree variable)
    - removed new_moves list (created path instead to track prev)
    - corrected adjacent moves
Changes by Jeremy Feb 25:
    - fixed final path bug (where code won't terminate)
Changes by MJ Feb 25:
    - [line 110] added goal coordinates to the final path
Changes by Gleezell Feb 25:
    - fixed path file of "maze.txt"

"""
directions = [[0,1],[1,0],[0,-1],[-1,0]]
class Node(object):
    def __init__(self, parent=None, moves=None, path=None):
        self.parent = parent
        self.moves = moves

        if path is None:
            self.path = list()
        else:
            self.path = path
    
        self.function = 0
        self.degree = 0
        self.heuristic = 0
    
    def calculate_function(self):
        return self.degree + self.heuristic

def is_wall(maze, x, y):
    if(maze[x][y] == "#"):
        return True
    return False

def is_goal(maze, x, y):
    if(maze[x][y] == "G"):
        return True
    return False

def check_bounds(x, y, maze_size):
    if(x < 0 or x >= maze_size):
        return False
    
    if(y >= maze_size or y < 0):
        return False
    
    return True

def find_start(maze_size, maze):
    for x in range(maze_size):
        for y in range(maze_size):
            if(maze[x][y] == 'S'):
                return [x, y]
            
def find_end(maze_size, maze):
    for x in range(maze_size):
        for y in range(maze_size):
            if(maze[x][y] == 'G'):
                return [x, y]

def manhattan_distance(current_position, end_position):
    x = end_position[0] - current_position[0]
    y = end_position[1] - current_position[1]
    
    return abs(x) + abs(y)

def possible_moves(node, maze_size, maze):
    possible_nodes = list()

    current_position = node.moves
    end_position = find_end(maze_size, maze)

    for direction in directions:
        #gives adjacent moves
        new_x = current_position[0] + direction[0]
        new_y = current_position[1] + direction[1]
        
        #checks if adjacent move is valid. (not wall, not out of maze, and not explored)
        if check_bounds(new_x, new_y, maze_size) and not is_wall(maze, new_x, new_y) and [new_x, new_y] not in node.path:
            
            #print(new_x,new_y) #tracing
            new_node = Node(node, [new_x, new_y])
            new_node.path = node.path + [current_position]
            new_node.degree = node.degree + 1
            new_node.heuristic = manhattan_distance([new_x, new_y], end_position)

            new_node.function = new_node.calculate_function()

            possible_nodes.append(new_node)
        
    return possible_nodes

def a_star(maze_size, maze):
    end_position = find_end(maze_size, maze)

    explored = list()
    frontier = list()

    initial_node = Node(None, find_start(maze_size, maze))
    frontier.append(initial_node)

    while len(frontier) > 0:

        current_node = frontier[0]

        frontier.remove(current_node)
        explored.insert(0, current_node)

        if current_node.moves == end_position:
            current_node.path += [current_node.moves]
            # print(current_node.path) # path checker (MUST be optimal)
            return current_node

        possible_nodes = possible_moves(current_node, maze_size, maze)
        
        #if there is at least 1 possible node
        if possible_nodes:
            for possible_node in possible_nodes:
                insertion_index = len(frontier)
                    
                for index, node in enumerate(frontier):
                    if possible_node.function < node.function:
                        insertion_index = index
                        break

                frontier.insert(insertion_index, possible_node)
        #print(explored[0].moves)    #uncomment for explored path coordinates


def get_maze_size():
    return maze_size

def get_maze():
    return maze


maze = []

with open(os.path.join(sys.path[0], "maze.txt"), "r") as maze_file:

    maze_size = [int(i) for i in next(maze_file).split()][0]
    for i in range(maze_size):
        maze.append(list(next(maze_file))[0:maze_size])

    last_node = a_star(maze_size, maze)
    #print(last_node.path) #uncomment for final path coordinates
    
    #final path with "z'"
    print(last_node.path)
    for i in last_node.path:
        maze[i[0]][i[1]] = "Z"
     
    """   
    uncomment for maze final path
    for i in maze:
        print(i)
    print()
    """

