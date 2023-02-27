import os
import sys
import pygame
import time
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)

pygame.init()
# main fonts for gui
gui_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 30)

class Button:
	def __init__(self, text, width, height, pos):
		# Action Attributes
		self.pressed = False
		
		#top rectangle
		self.top_rect = pygame.Rect(pos,(width, height))
		self.top_color = '#3179FF'
		
        #Button Text
		self.text_surf = gui_font.render(text, True, '#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
	
	def draw(self, screen):
		pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 15)
		screen.blit(self.text_surf, self.text_rect)
		self.click()
	
	def click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#2CDE3D'
			if pygame.mouse.get_pressed()[0]:
				self.pressed = True
			else:
				if self.pressed == True:
					self.pressed = False
		else:
			self.top_color = '#3179FF'
				
		
class Cell:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_barrier(self):
		return self.color == BLACK

	def make_start(self):
		self.color = ORANGE

	def make_explored(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_wall(self):
		self.color = BLACK

	def make_end(self):
		self.color = BLUE

	def make_path(self):
		self.color = PURPLE

	def draw(self, window):
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# Looks for starting point
def find_start(maze_size, maze):
    for x in range(maze_size):
        for y in range(maze_size):
            if(maze[x][y] == 'S'):
                return x, y

# Looks for ending point      
def find_end(maze_size, maze):
    for x in range(maze_size):
        for y in range(maze_size):
            if(maze[x][y] == 'G'):
                return x, y

# Computes manhattan distance
def manhattan_distance(current_position, end_position):
    x = end_position[0] - current_position[0]
    y = end_position[1] - current_position[1]
    
    return abs(x) + abs(y)

# Draws out the optimal path at the end
def show_optimal(explored, current, draw):
	while current in explored:
		current = explored[current]
		current.make_path()
		draw()

# A* algorithm with manhattan distance heuristic
def a_star(draw, grid, start_position, end_position):
	count = 0
	frontier = PriorityQueue()
	frontier.put((0, count, start_position))
	explored = {}
	cost = {cell: float("inf") for row in grid for cell in row}
	cost[start_position] = 0
	function_score = {cell: float("inf") for row in grid for cell in row}
	function_score[start_position] = manhattan_distance(start_position.get_pos(), end_position.get_pos())

	frontier_hash = {start_position}

	while not frontier.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = frontier.get()[2]
		frontier_hash.remove(current)

		if current == end_position:
			show_optimal(explored, end_position, draw)
			end_position.make_end()
			return True, explored

		for neighbor in current.neighbors:
			temp_cost = cost[current] + 1

			if temp_cost < cost[neighbor]:
				explored[neighbor] = current
				cost[neighbor] = temp_cost
				function_score[neighbor] = temp_cost + manhattan_distance(neighbor.get_pos(), end_position.get_pos())
				if neighbor not in frontier_hash:
					count += 1
					frontier.put((function_score[neighbor], count, neighbor))
					frontier_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start_position:
			current.make_explored()

	return False, explored

# Initialize the grid cells
def make_grid(maze_size, width, maze):
	grid = []
	gap = width // maze_size
	for i in range(maze_size):
		grid.append([])
		for j in range(maze_size):
			cell = Cell(i, j, gap, maze_size)
			
			if(maze[j][i] == '#'):
				cell.make_wall()
			elif(maze[j][i] == 'S'):
				cell.make_start()
			elif(maze[j][i] == 'G'):
				cell.make_end()
	
			grid[i].append(cell)

	return grid

# Draws the grid lines
def draw_grid(window, maze_size, width):
	gap = width // maze_size
	for i in range(maze_size):
		pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
		for j in range(maze_size):
			pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

# Draws the whole grid in window
def draw(window, grid, maze_size, width):

	for row in grid:
		for cell in row:
			cell.draw(window)

	draw_grid(window, maze_size, width)
	pygame.display.update()

def show_res(result, states, screen):
	if result == True:
	    visit = len(states)
	    state = Button('States Visited: ' + str(visit), 350, 50,(320, 725))
	    state.draw(screen)
	elif result == False:
		impossible = Button('IMPOSSIBLE MAZE!', 350, 50,(320, 725))
		impossible.draw(screen)
	#pygame.display.update()
# Main function
def main(window, width, maze_size, maze):
    
	grid = make_grid(maze_size, width, maze)
	
	temp = find_start(maze_size, maze)
	start = grid[temp[1]][temp[0]]
	
	temp = find_end(maze_size, maze)
	end = grid[temp[1]][temp[0]]
	
	run = True
	
	window.fill(WHITE)
	
	heuristic_but = Button('A Star Algorithm', 300, 60,(10, 720)) 
	while run:
		heuristic_but.draw(window)
		draw(window, grid, maze_size, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if heuristic_but.pressed == True and start and end:
				for row in grid:
					for cell in row:
						cell.update_neighbors(grid)
				
				res,states = a_star(lambda: draw(window, grid, maze_size, width), grid, start, end)
				show_res(res, states, window)
				

	pygame.quit()

maze = []

# File opening
with open(os.path.join(sys.path[0], "maze.txt"), "r") as maze_file:

    maze_size = [int(i) for i in next(maze_file).split()][0]
    for i in range(maze_size):
        maze.append(list(next(maze_file))[0:maze_size])

WIDTH = 700
LENGTH = 800
WINDOW = pygame.display.set_mode((WIDTH, LENGTH))
    
main(WINDOW, WIDTH, maze_size, maze)
