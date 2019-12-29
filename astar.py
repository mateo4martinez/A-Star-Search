try:
	import pygame
	import math
	from tkinter import *
except:
	import install_requirements
	import pygame
	import math
	from tkinter import *
pygame.init()
pygame.display.set_caption('A-Star Search!')

TIME_DELAY = 5 #Milliseconds
MARGIN = 2
BLOCK_SIZE = 10
SIDE = 500
white = pygame.Color('white')
blue = pygame.Color('blue')#Start and end nodes
red = pygame.Color('red')#path
green = pygame.Color('green')#closed_set
orange = pygame.Color('orange')#open_set
black = pygame.Color('black')#barriers
FONT = ('Verdana', 10)
win = pygame.display.set_mode(size = (SIDE,SIDE))

#A class demonstrating each tile.
class Spot():
	def __init__(self, side, x, y, color, parent=None):
		self.side = side
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, self.side, self.side)
		self.color = color
		self.parent = parent

	def draw_spot(self):
		pygame.draw.rect(win, self.color, self.rect)

	def change_color(self, new_color):
		if self.color != blue:
			self.color = new_color
		pygame.draw.rect(win, self.color, self.rect)

	def get_color(self):
		return self.color

	def get_side(self):
		return self.side

	def get_position(self):
		return self.x, self.y

	def new_parent(self, parent):
		self.parent = parent

	def get_parent(self):
		return self.parent

	def in_spot(self, x, y):
		return (x>=self.x and x<=self.x+self.side) and (y>=self.y and y<=self.y+self.side)

	def is_valid(self):
		return self.color != black

#A class demonstrating the entire grid.
class Grid():
	def __init__(self, margin, block_size, side):
		self.side= side
		self.margin = margin
		self.spots = []
		self.block_size = block_size

	def generate_spots(self):
		for j in range(0, self.side-self.block_size-self.margin, self.block_size+self.margin):
			for i in range(0, self.side-self.block_size-self.margin, self.block_size+self.margin):
				self.spots.append(Spot(self.block_size, i+self.margin, j+self.margin, white))
	
	def get_spots(self):
		return self.spots

	def draw(self):
		for spot in self.spots:
			spot.draw_spot()

	def get_neighbors(self, node):
		nbrs = []
		x1,y1 = node.get_position()
		for spot in self.spots:
			x2, y2 = spot.get_position()
			if (x2==x1+spot.get_side()+self.margin or x2==x1-self.margin-spot.get_side()) and y2==y1 and spot.is_valid():
				nbrs.append(spot)
			elif (y2==y1+spot.get_side()+self.margin or y2==y1-self.margin-spot.get_side()) and x2==x1 and spot.is_valid():
				nbrs.append(spot)
			elif (x2==x1+spot.get_side()+self.margin or x2==x1-spot.get_side()-self.margin) and (y2==y1+spot.get_side()+self.margin or y2==y1-spot.get_side()-self.margin) and spot.is_valid():
				nbrs.append(spot)
		return nbrs

#Find the heuristic of 2 spots.
def heuristic(spot_1, spot_2):
	"""
	Finds the heuristic between 2 spots.
	inputs:
		- spot_1: a spot in grid
		- spot_2: a spot in grid
	outputs:
		- the heuristic between spot_1 and spot_2
	"""
	x1, y1 = spot_1.get_position()
	x2, y2 = spot_2.get_position()
	delta_x = x2-x1
	delta_y = y2-y1
	return math.sqrt((delta_y**2)+(delta_x**2))

def edge_distance():
	return 1

def find_lowest_fcost(f_cost, lst):
    """
    Finds the lowest f_cost in the open_set.
    
    inputs:
        - f_cost: a mapping of all the f_costs
        - lst: a sequence of nodes that represent the open set.
    outputs:
        - good_ele: node of the lowest f_cost
    """
    low_f = float('inf')
    good_ele = None
    for ele in lst:
        if ele in f_cost.keys() and f_cost[ele] <= low_f:
            low_f = f_cost[ele]
            good_ele = ele
    return good_ele

def find_path(start, end):
	"""
	Finds the path from the start to end.
	inputs:
		- start: the first node.
		- end: the last node.
	outputs:
		- a path from the end node to the start node.
		  Needs to be reversed.
	"""
	path = []
	path.append(end)
	spot = end
	while spot != start:
		parent = spot.get_parent()
		path.append(parent)
		spot = parent
	return path

def popup_msg(msg):
	#Creates a popup message. 
	popup = Tk()
	popup.wm_title('A-star Search!')
	label = Label(popup, text=msg, font=FONT)
	label.pack(side='top', fill='x', pady=10)
	ok = Button(popup, text='Okay', command=popup.destroy)
	ok.pack()
	popup.mainloop()

def build_path(path):
	#Builds the shortest path.
	for spot in path:
		spot.change_color(red)
		pygame.display.update()

def a_star(grid, start, end):
	"""
	Executes the A* Algorithm
	inputs:
		- grid: The Grid in which the spots lie on.
		- start: The starting point.
		- end: The ending point.
	"""
	open_set = []
	closed_set = []
	g_cost = {}
	f_cost = {}
	g_cost[start] = 0
	f_cost[start] = heuristic(start, end)

	open_set.append(start)

	while len(open_set)>0:
		current = find_lowest_fcost(f_cost, open_set)
		open_set.remove(current)
		closed_set.append(current)
		if current == end:
			path = find_path(start, end)[::-1]
			build_path(path)
			popup_msg('The shortest path is '+ str(f_cost[end])+' units.')
			break
		for nbr in grid.get_neighbors(current):
			if nbr in closed_set:
				continue
			new_g = g_cost[current]+edge_distance()
			if nbr not in open_set:
				open_set.append(nbr)
			elif new_g >= g_cost[nbr]:
				continue

			nbr.new_parent(current)
			g_cost[nbr] = new_g
			h_cost = heuristic(nbr, end)
			f_cost[nbr] = h_cost + g_cost[nbr]
		for spot in closed_set:
			if spot.get_color() != green:
				pygame.time.delay(TIME_DELAY)
				spot.change_color(green)
				pygame.display.update()
		for spot in open_set:
			if spot.get_color() != orange:
				pygame.time.delay(TIME_DELAY)
				spot.change_color(orange)
				pygame.display.update()

def find_spot(spots, x, y):
	#Finds if the button click was within 
	#the spot area.
	for spot in spots:
		if spot.in_spot(x, y):
			return spot
	return None

def picking(spots):
	"""
	Pick the starting and ending points.
	inputs:
		- spots: a sequence of Spots
	outputs:
		- start: the start point chosen.
		- end: the end point chosen.
	"""
	start = None
	end = None
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("QUIT")
				pygame.quit()
				running = False
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				spot = find_spot(spots, x, y)
				if start == None and spot != None:
					#Starting point chosen.
					start = spot
					start.change_color(blue)
					pygame.display.update()
				elif start != None and spot != None:
					#Ending point chosen.
					running = False
					end = spot
					end.change_color(blue)
					pygame.display.update()
	return start, end

def building(spots):
	#User get to choose where to put obstacles.
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("QUIT")
				pygame.quit()
				running = False
				quit()
			elif pygame.mouse.get_pressed()[0]:
				x, y = pygame.mouse.get_pos()
				spot = find_spot(spots, x, y)
				if spot != None:
					spot.change_color(black)
					pygame.display.update()
			elif event.type == pygame.KEYDOWN:
				#User clicks space key to stop building.
				if event.key == pygame.K_SPACE:
					running = False


grid = Grid(MARGIN, BLOCK_SIZE, SIDE)

grid.generate_spots()
spots = grid.get_spots()
grid.draw()
pygame.display.update()

#Pick Start and End points.
start, end = picking(spots)
#Build obstacles.
building(spots)
#Find the shortest path.
a_star(grid, start, end)
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print("QUIT")
			pygame.quit()
			running = False
			quit()