import pygame, os 
import math
from timeit import default_timer as timer
from queue import PriorityQueue
from collections import deque

WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver (Multiple Algorithms)")

# Colors
BACKGROUND = (46, 2, 73)
PATH_CLOSE = (87, 9, 135)
PATH_OPEN = (127, 17, 194)
GRID = (87, 10, 87)
WALL = (248, 6, 204)
START = (0, 255, 171)
END = (47, 255, 0)
PATH = (255, 210, 76)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BACKGROUND
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = BACKGROUND

    def make_close(self):
        self.color = PATH_CLOSE

    def make_open(self):
        self.color = PATH_OPEN

    def make_wall(self):
        self.color = WALL
    
    def make_start(self):
        self.color = START

    def make_end(self):
        self.color = END

    def make_path(self):
        self.color = PATH

    def is_closed(self):
        return self.color == PATH_CLOSE

    def is_opened(self):
        return self.color == PATH_OPEN

    def is_wall(self):
        return self.color == WALL
    
    def is_start(self):
        return self.color == START

    def is_end(self):
        return self.color == END

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        # checks for neighbours in all four directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = self.row + dx, self.col + dy
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows and not grid[new_row][new_col].is_wall():
                self.neighbours.append(grid[new_row][new_col])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(node_path, current, draw, counter_start):
    pygame.display.set_caption("Maze Solver (Constructing Path...)")
    path_count = 0

    while current in node_path:
        current = node_path[current]            
        current.make_path()
        path_count += 1
        draw()
    counter_end = timer()
    time_elapsed = counter_end - counter_start
    pygame.display.set_caption(f'Time Elapsed: {format(time_elapsed, ".2f")}s | Cells Visited: {len(node_path) + 1} | Shortest Path: {path_count + 1} Cells')    

def a_star(draw, grid, start, end, counter_start):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    node_path = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
        
    open_set_hash = {start}
    
    while not open_set.empty():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                node_path[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()
        if current != start:
            current.make_close()

    pygame.display.set_caption("Maze Solver (Unable To Find The Target Node!)")
    return False

def dijkstra(draw, grid, start, end, counter_start):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    node_path = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_distance = distance[current] + 1

            if temp_distance < distance[neighbour]:
                node_path[neighbour] = current
                distance[neighbour] = temp_distance
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((distance[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()
        if current != start:
            current.make_close()

    pygame.display.set_caption("Maze Solver (Unable To Find The Target Node!)")
    return False

def bfs(draw, grid, start, end, counter_start):
    queue = deque([start])
    visited = {start}
    node_path = {}
    
    while queue:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            reconstruct_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                node_path[neighbour] = current
                queue.append(neighbour)
                neighbour.make_open()

        draw()
        if current != start:
            current.make_close()

    pygame.display.set_caption("Maze Solver (Unable To Find The Target Node!)")
    return False

def dfs(draw, grid, start, end, counter_start):
    stack = [start]
    visited = set()
    node_path = {}
    
    while stack:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        if current not in visited:
            visited.add(current)
            for neighbour in current.neighbours:
                if neighbour not in visited:
                    node_path[neighbour] = current
                    stack.append(neighbour)
                    neighbour.make_open()

        draw()
        if current != start:
            current.make_close()

    pygame.display.set_caption("Maze Solver (Unable To Find The Target Node!)")
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID ,(i * gap, 0), (i * gap, width))

def draw_grid_wall(rows, grid):
    for i in range(rows):
        for j in range(rows):
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot = grid[i][j]
                spot.make_wall()

def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    draw_grid_wall(rows, grid)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    algorithm = a_star  # Default algorithm

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_wall()                

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    counter_start = timer()
                    pygame.display.set_caption(f"Maze Solver (Running {algorithm.__name__}...)")
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, counter_start)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    pygame.display.set_caption("Maze Solver (Multiple Algorithms)")
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_a:
                    algorithm = a_star
                    pygame.display.set_caption("Maze Solver (A* Algorithm Selected)")
                if event.key == pygame.K_d:
                    algorithm = dijkstra
                    pygame.display.set_caption("Maze Solver (Dijkstra's Algorithm Selected)")
                if event.key == pygame.K_b:
                    algorithm = bfs
                    pygame.display.set_caption("Maze Solver (BFS Algorithm Selected)")
                if event.key == pygame.K_f:
                    algorithm = dfs
                    pygame.display.set_caption("Maze Solver (DFS Algorithm Selected)")

    pygame.quit()

if __name__ == "__main__":
    main(win, WIDTH)