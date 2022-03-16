import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Visualizer")

# DEFNING COLORS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
PINK = (255,192,203)
GREY = (128,128,128)
ORANGE = (255,165,0)

class Spot:
	def __init__(self, row, col, width, totalRows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.totalRows = totalRows

	def getPos(self):#DEFINING WHAT COLOR WILL CORRESPOND TO WHICH ACTIVITY
		return self.row, self.col

	def closed(self):
		return self.color == RED

	def open(self):
		return self.color == GREEN

	def barrier(self):
		return self.color == BLACK

	def start(self):
		return self.color == PINK

	def end(self):
		return self.color == ORANGE

	def reset(self):
		self.color = WHITE

	def mStart(self):
		self.color = PINK

	def mClosed(self):
		self.color = RED

	def mOpen(self):
		self.color = GREEN

	def mBarrier(self):
		self.color = BLACK

	def mEnd(self):
		self.color = ORANGE

	def mPath(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def updateNeighbors(self, grid):
		self.neighbors = []
		if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstructPath(cameFrom, current, draw):
	while current in cameFrom:
		current = cameFrom[current]
		current.mPath()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	cameFrom = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.getPos(), end.getPos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstructPath(cameFrom, end, draw)
			end.mEnd()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				cameFrom[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.getPos(), end.getPos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.mOpen()

		draw()

		if current != start:
			current.mClosed()

	return False


def makeGrid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def drawGrid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	drawGrid(win, rows, width)
	pygame.display.update()


def clickedPos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50 #can be changed to increase grid size
	grid = makeGrid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:# If player quits the game
				run = False

			if pygame.mouse.get_pressed()[0]: # IF left mouse is clicked
				pos = pygame.mouse.get_pos()
				row, col = clickedPos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.mStart()

				elif not end and spot != start:
					end = spot
					end.mEnd()

				elif spot != end and spot != start:
					spot.mBarrier()

			elif pygame.mouse.get_pressed()[2]: # If right mouse is clicked
				pos = pygame.mouse.get_pos()
				row, col = clickedPos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.updateNeighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = makeGrid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
