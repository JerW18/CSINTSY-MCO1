import copy
import math

directions = [[0,1],[1,0],[0,-1],[-1,0]]
class Node(object):
    def __init__(self, parent=None, moves=None, distance=None):
        self.parent = parent
        self.moves = moves
        self.distance = distance

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

    current_distance = node.distance + 1

    for direction in directions:
        new_x = current_position[0] + direction[0]
        new_y = current_position[1] + direction[1]

        if check_bounds(new_x, new_y, maze_size) and not is_wall(maze, new_x, new_y) and [new_x, new_y] not in node.moves:
            new_moves = copy.deepcopy(node.moves)
            new_moves.append([new_x, new_y])

            new_node = Node(node, new_moves, current_distance)

            new_node.degree = node.degree + 1
            new_node.heuristic = manhattan_distance([new_x, new_y], end_position)

            new_node.function = new_node.calculate_function()

            possible_nodes.append(new_node)

    return possible_nodes


def a_star(maze_size, maze):
    end_position = find_end(maze_size, maze)

    explored = list()
    frontier = list()

    initial_node = Node(None, find_start(maze_size, maze), 0)

    frontier.append(initial_node)

    while len(frontier) > 0:
        current_node = frontier[0]

        frontier.remove(current_node)
        explored.append(current_node)

        if current_node.moves[-1] == end_position:
            return current_node

        possible_nodes = possible_moves(current_node, maze_size, maze)

        if possible_nodes:
            for possible_node in possible_nodes:
                insertion_index = len(frontier)

                for index, node in enumerate(frontier):
                    if possible_node.function < node.function:
                        insertion_index = index
                        break

                frontier.insert(insertion_index, possible_node)


maze = []

with open(r"D:\Codes\Codes_Python\maze.txt") as maze_file:

    maze_size = [int(i) for i in next(maze_file).split()][0]
    for i in range(maze_size):
        maze.append(list(next(maze_file))[0:maze_size])

    a_star(maze_size, maze)