import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
TILE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Clock
clock = pygame.time.Clock()
FPS = 10

# Generate random obstacles
def generate_obstacles():
    obstacles = set()
    for _ in range(GRID_SIZE * GRID_SIZE // 4):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in {(0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)}:
            obstacles.add((x, y))
    return obstacles

# BFS to check if a path exists and find the path
def bfs_find_path(start, end, obstacles):
    queue = deque([(start, [])])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path + [current]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                queue.append((neighbor, path + [current]))

    return []

# Main game function
def main():
    start = (0, 0)
    end = (GRID_SIZE - 1, GRID_SIZE - 1)
    obstacles = generate_obstacles()

    # Ensure a valid path exists
    path = bfs_find_path(start, end, obstacles)
    while not path:
        obstacles = generate_obstacles()
        path = bfs_find_path(start, end, obstacles)

    player_pos = list(start)
    lives = 3
    path_index = 0

    running = True
    while running:
        screen.fill(WHITE)

        # Draw grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (x, y) in obstacles:
                    pygame.draw.rect(screen, BLACK, rect)
                elif (x, y) == start:
                    pygame.draw.rect(screen, GREEN, rect)
                elif (x, y) == end:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect, 1)

        # Draw player
        player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, BLUE, player_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Autonomous movement along the path
        if path_index < len(path):
            next_pos = path[path_index]
            if next_pos == tuple(player_pos):
                path_index += 1
            else:
                player_pos[0], player_pos[1] = next_pos
        else:
            print("You win!")
            running = False

        # Check game over
        if lives <= 0:
            print("Game over!")
            running = False

        # Display lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
