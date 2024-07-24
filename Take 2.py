import pygame
import numpy as np
import heapq

# Load the maze configuration from the file
data = np.load('maze_config.npz')
matrix = data['matrix']
start_pos = tuple(data['start_pos'])
goal_pos = tuple(data['goal_pos'])

# Define constants
CELL_SIZE = 40
WIDTH = len(matrix[0]) * CELL_SIZE
HEIGHT = len(matrix) * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Color for start position
GREEN = (0, 255, 0)  # Color for goal position
BLUE = (0, 0, 255)  # Color for the agent (player)
LIGHT_BLUE = (173, 216, 230)  # Color for the optimal path
LIGHT_GRAY = (200, 200, 200)  # Color for explored paths

# Initialize pygame
pygame.init()

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

# Player starting position
player_pos = list(start_pos)
visited = []
path_stack = []
optimal_path = []


# Function to draw the maze
def draw_maze():
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            color = BLACK if matrix[row][col] == 1 else WHITE
            pygame.draw.rect(window, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw the start position
    pygame.draw.rect(window, RED, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw the goal position
    pygame.draw.rect(window, GREEN, (goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Function to draw the player
def draw_player():
    pygame.draw.rect(window, BLUE, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Function to shade the explored paths
def shade_explored_paths():
    for pos in visited:
        pygame.draw.rect(window, LIGHT_GRAY, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Function to draw the optimal path
def draw_optimal_path():
    for pos in optimal_path:
        pygame.draw.rect(window, LIGHT_BLUE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def manhattan_distance(x, y, end):
    return abs(x - end[0]) + abs(y - end[1])


def flood_fill(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    weights = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and not visited[x][y] and matrix[x][y] == 0

    # Initialize priority queue with the starting point
    pq = [(manhattan_distance(start[0], start[1], end), start[0], start[1])]
    weights[start[0]][start[1]] = 0

    while pq:
        current_weight, x, y = heapq.heappop(pq)

        if visited[x][y]:
            continue

        visited[x][y] = True
        visited_list.append((x, y))  # Keep track of visited cells for visualization

        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[x][y]
            path.append(start)
            return path[::-1], visited_list

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                new_weight = weights[x][y] + 1
                if new_weight < weights[new_x][new_y]:
                    weights[new_x][new_y] = new_weight
                    heapq.heappush(pq, (new_weight + manhattan_distance(new_x, new_y, end), new_x, new_y))
                    parent[new_x][new_y] = (x, y)

    return None, visited_list


def automate_solver():
    global player_pos, optimal_path, visited
    optimal_path, visited = flood_fill(matrix, start_pos, goal_pos)
    player_pos = list(start_pos)  # Reset player position


def follow_optimal_path():
    global player_pos
    for pos in optimal_path:
        player_pos = pos
        # Draw everything
        draw_maze()
        shade_explored_paths()
        draw_optimal_path()
        draw_player()

        # Update the display
        pygame.display.flip()
        pygame.time.wait(100)  # Add a small delay to visualize the movements


# Main loop
running = True
automate_solver()  # Solve the maze initially

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    follow_optimal_path()

# Quit pygame
pygame.quit()
