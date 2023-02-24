import math

class Node(object):

    def __init__(self, parent=None, moves=None, state=None):
        self.parent = parent
        self.moves = moves
        self.state = state

        self.function = 0
        self.degree = 0
        self.heuristic = 0
    
    def calculate_function(self):
        return self.degree * self.heuristic

def is_wall(maze, x, y):
    if(maze[x][y] == "#"):
        return True
    return False

def is_goal(maze, x, y):
    if(maze[x][y] == "G"):
        return True
    return False

def find_start(n, maze):
    for i in range(n):
        for j in range(n):
            if(maze[i][j] == 'S'):
                return i, j
            
def find_end(n, maze):
    for i in range(n):
        for j in range(n):
            if(maze[i][j] == 'S'):
                return i, j

def solve():
    maze = []

    with open(r"D:\Codes\Codes_Python\maze.txt") as maze_file:

        n = [int(i) for i in next(maze_file).split()][0]
        for i in range(n):
            maze.append(list(next(maze_file))[0:n])
        
        x,y = find_start(n, maze)
        # Search Func