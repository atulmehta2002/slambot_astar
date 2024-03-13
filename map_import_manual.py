import pygame
import os
import heapq
import tempfile

# Function to load a PNG file
def load_png(filename):
    image = pygame.image.load(filename)
    return image

# Function to scale down the image to a grid
def scale_down_to_grid(image, grid_size):
    scaled_image = []
    for y in range(0, image.get_height(), grid_size):
        row = []
        for x in range(0, image.get_width(), grid_size):
            total_r, total_g, total_b, total_a = 0, 0, 0, 0
            count = 0  # Count the number of pixels in this grid cell
            for dy in range(grid_size):
                for dx in range(grid_size):
                    if (x + dx) < image.get_width() and (y + dy) < image.get_height():
                        pixel = image.get_at((x + dx, y + dy))
                        total_r += pixel.r
                        total_g += pixel.g
                        total_b += pixel.b
                        total_a += pixel.a
                        count += 1
            average_r = total_r // count if count > 0 else 0
            average_g = total_g // count if count > 0 else 0
            average_b = total_b // count if count > 0 else 0
            average_a = total_a // count if count > 0 else 0
            row.append((average_r, average_g, average_b, average_a))
        scaled_image.append(row)
    return scaled_image

# A* algorithm implementation
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for next_node in graph.neighbors(current_node):
            new_cost = cost_so_far[current_node] + graph.cost(current_node, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current_node

    path = []
    current_node = goal
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(start)
    path.reverse()
    return path

# Graph representing the grid
class GridGraph:
    def __init__(self, grid):
        self.grid = grid

    def neighbors(self, node):
        x, y = node
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_neighbors = []
        for nx, ny in neighbors:
            if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                valid_neighbors.append((nx, ny))
        return valid_neighbors

    def cost(self, from_node, to_node):
        return abs(self.grid[to_node[1]][to_node[0]][0] - self.grid[from_node[1]][from_node[0]][0])

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 1               # Adjust this to change the grid size
MAP_FILENAME = "room.pgm"   # Change this to your map file

counter = 0                 # used to save map only once after second click event

# Load the map
map_image = load_png(MAP_FILENAME)

# Scale down the image to a grid
scaled_image = scale_down_to_grid(map_image, GRID_SIZE)

# Set up the display
cell_size = 5 # Adjust this for smaller squares
window_size = (len(scaled_image[0]) * cell_size, len(scaled_image) * cell_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Map Display")

# Graph representing the grid
graph = GridGraph(scaled_image)

# Variables for marking points
start_point = None
end_point = None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= cell_size
            y //= cell_size
            if start_point is None:
                start_point = (x, y)
            elif end_point is None:
                end_point = (x, y)
                
    # Draw the grid
    screen.fill((255, 255, 255))
    for y, row in enumerate(scaled_image):
        for x, color in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    # Draw start and end points
    if start_point:
        pygame.draw.circle(screen, (255, 0, 0), (start_point[0] * cell_size + cell_size // 2, start_point[1] * cell_size + cell_size // 2), cell_size // 4)
    if end_point:
        pygame.draw.circle(screen, (0, 255, 0), (end_point[0] * cell_size + cell_size // 2, end_point[1] * cell_size + cell_size // 2), cell_size // 4)

    # Run A* algorithm and draw the path
    if start_point and end_point:
        path = astar(graph, start_point, end_point)
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (0, 0, 255), (path[i][0] * cell_size + cell_size // 2, path[i][1] * cell_size + cell_size // 2),
                             (path[i+1][0] * cell_size + cell_size // 2, path[i+1][1] * cell_size + cell_size // 2), 3)
        
        if end_point and counter == 0:
            counter = 1
            save_file = os.path.join("shortest_path_map.png")  # Save the current display as a PNG file
            pygame.image.save(screen, save_file)
            print(f"Length in X: {len(scaled_image[0])}, Length in Y: {len(scaled_image)}")
            print(f"Map saved as: {save_file}")
        
        for event in pygame.event.get():               # use key "c" to clear al the start end points for new start end points
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:    
                    start_point = None
                    end_point = None
                    counter = 0

    pygame.display.flip()

pygame.quit()



## everything ok till here :) ##