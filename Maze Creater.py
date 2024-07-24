import pygame
import numpy as np

# Define constants
CELL_SIZE = 40
ROWS = 20
COLS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize pygame
pygame.init()

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Creator")

# Initialize matrix
matrix = np.ones((ROWS, COLS), dtype=int)
start_pos = None
goal_pos = None

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if matrix[row][col] == 1 else WHITE
            pygame.draw.rect(window, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    if start_pos:
        pygame.draw.rect(window, RED, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if goal_pos:
        pygame.draw.rect(window, GREEN, (goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

running = True
drawing_wall = False
erasing_wall = False
setting_start = False
setting_goal = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE

            if event.button == 1:  # Left click
                drawing_wall = True
                matrix[row][col] = 1
            elif event.button == 3:  # Right click
                erasing_wall = True
                matrix[row][col] = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing_wall = False
            erasing_wall = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing_wall:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                matrix[row][col] = 1
            elif erasing_wall:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                matrix[row][col] = 0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                setting_start = True
                setting_goal = False
            elif event.key == pygame.K_g:
                setting_goal = True
                setting_start = False
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                matrix = np.ones((ROWS, COLS), dtype=int)
                start_pos = None
                goal_pos = None

        if setting_start or setting_goal:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if setting_start:
                    start_pos = (row, col)
                    setting_start = False
                elif setting_goal:
                    goal_pos = (row, col)
                    setting_goal = False

    # Draw everything
    window.fill(WHITE)
    draw_grid()

    # Update the display
    pygame.display.flip()

# Save the maze configuration
if start_pos and goal_pos:
    np.savez('maze_config.npz', matrix=matrix, start_pos=start_pos, goal_pos=goal_pos)

# Quit pygame
pygame.quit()
