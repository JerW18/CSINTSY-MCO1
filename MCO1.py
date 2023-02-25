import copy
import math

"""
Changes by Erika Feb 25: 
    - added Path List to Node Class
    - changed calculate_function operation from * to +
    - removed distance variable (bcs cost is counted from degree variable)
    - removed new_moves list (created path instead to track prev)
    - corrected adjacent moves
"""
directions = [[0,1],[1,0],[0,-1],[-1,0]]
class Node(object):
    def __init__(self, parent=None, moves=None, path=[]):
        self.parent = parent
        self.moves = moves
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
                return x, y

def manhattan_distance(current_position, end_position):
    x = end_position[0] - current_position[0]
    y = end_position[1] - current_position[1]
    
    return abs(x) + abs(y)

def possible_moves(node, maze_size, maze):
    possible_nodes = list()

    current_position = node.moves
    end_position = find_end(maze_size, maze)
    #print(current_position)
   
    for direction in range(len(directions)):
        #gives adjacent moves
        new_x = current_position[0] + directions[direction][0]
        new_y = current_position[1] + directions[direction][1]
        
        #checks if adjacent move is valid. (not wall, not out of maze, and not explored)
        if check_bounds(new_x, new_y, maze_size) and not is_wall(maze, new_x, new_y) and [new_x, new_y] not in node.path:
            
            #print(new_x,new_y)
            new_node = Node(node, [new_x, new_y])
            new_node.path = node.path + [current_position] + [[new_x, new_y, "*"]]
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
    #print(initial_node.moves)
    frontier.append(initial_node)
    loop = 0
    while len(frontier) > 0:
        loop += 1  #nvm counter lang 
        current_node = frontier[0]

        frontier.remove(current_node)
        explored.insert(0, current_node)

        if current_node.moves[-1] == end_position:
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
        #print(explored[0].moves)   #checker only
                  
maze = []

#change the path:
with open(r"/Users/erikac/Documents/GitHub/CSINTSY-MCO1/maze.txt") as maze_file:

    maze_size = [int(i) for i in next(maze_file).split()][0]
    for i in range(maze_size):
        maze.append(list(next(maze_file))[0:maze_size])

    a_star(maze_size, maze)