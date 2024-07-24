import pygame
import numpy as np

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
RED = (255, 0, 0)      # Color for start position
GREEN = (0, 255, 0)    # Color for goal position
BLUE = (0, 0, 255)     # Color for the agent (player)
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

def move(current_pos):
    if tuple(current_pos) not in visited:
        visited.append(tuple(current_pos))
        path_stack.append(current_pos.copy())

    row, col = current_pos
    if col + 1 < len(matrix[0]) and (row, col + 1) not in visited and matrix[row][col + 1] != 1:
        return 'R'
    elif col - 1 >= 0 and (row, col - 1) not in visited and matrix[row][col - 1] != 1:
        return 'L'
    elif row + 1 < len(matrix) and (row + 1, col) not in visited and matrix[row + 1][col] != 1:
        return 'D'
    elif row - 1 >= 0 and (row - 1, col) not in visited and matrix[row - 1][col] != 1:
        return 'U'

    path_stack.pop()
    if path_stack:
        return 'B'
    return None

def automate_solver():
    global player_pos, optimal_path
    while tuple(player_pos) != goal_pos:
        choice = move(player_pos)
        if choice == 'U':
            player_pos = [player_pos[0] - 1, player_pos[1]]
        elif choice == 'D':
            player_pos = [player_pos[0] + 1, player_pos[1]]
        elif choice == 'L':
            player_pos = [player_pos[0], player_pos[1] - 1]
        elif choice == 'R':
            player_pos = [player_pos[0], player_pos[1] + 1]
        elif choice == 'B':
            if path_stack:
                player_pos = path_stack[-1]  # Backtrack to the previous position

        # Draw everything
        draw_maze()
        shade_explored_paths()
        draw_optimal_path()
        draw_player()

        # Update the display
        pygame.display.flip()
        pygame.time.wait(40)  # Add a small delay to visualize the movements

    # Store the optimal path once the goal is reached
    optimal_path = path_stack.copy()

def return_to_start():
    global player_pos
    while player_pos != list(start_pos):
        path_stack.pop()
        player_pos = path_stack[-1]
        # Draw everything
        draw_maze()
        shade_explored_paths()
        draw_optimal_path()
        draw_player()

        # Update the display
        pygame.display.flip()
        pygame.time.wait(1)  # Add a small delay to visualize the movements

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
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

    automate_solver()
    return_to_start()
    follow_optimal_path()

# Quit pygame
pygame.quit()
