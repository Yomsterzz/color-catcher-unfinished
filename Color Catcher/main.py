import pygame
import random
import sys
pygame.init()

WIDTH = 600
HEIGHT = 600 
FPS = 30
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
BLACK = (0, 0, 0)

COLORS = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (255, 192, 203), # Pink
    (128, 0, 128),   # Purple
    (0, 255, 255),   # Cyan
    (255, 255, 255), # White
    (128, 128, 128), # Gray
    (0, 128, 0),     # Dark Green
    (75, 0, 130)     # Indigo
]

player_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
target_color = random.choice(COLORS)
score = 0
time_limit = 5
time_remaining = time_limit
grid_colors = [[(0, 0, 0) for i in range(GRID_SIZE)] for i in range(GRID_SIZE)]
game_over = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Catcher")
clock = pygame.time.Clock()

def fill_grid_with_colors():
    for i in range(30):
        color = random.choice(COLORS)
        clump_size = random.randint(3, 7)  
        clump_x = random.randint(0, GRID_SIZE - 1)
        clump_y = random.randint(0, GRID_SIZE - 1)

        for x in range(clump_size):
            for y in range(clump_size):
                if (clump_x + x < GRID_SIZE) and (clump_y + y < GRID_SIZE):
                    grid_colors[clump_x + x][clump_y + y] = color

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid_colors[x][y] == (0, 0, 0):
                grid_colors[x][y] = random.choice(COLORS)

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            pygame.draw.rect(screen, grid_colors[x][y], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player():
    pygame.draw.rect(screen, BLACK, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_target_color():
    global target_color
    font = pygame.font.SysFont(None, 48)
    color_text = font.render("Stand on: ", True, target_color)
    screen.blit(color_text, (10, 555))
    
    pygame.draw.rect(screen, target_color, (170, 555, 30, 30))

def restart_game():
    global player_pos, target_color, score, time_remaining, game_over, grid_colors
    player_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
    target_color = random.choice(COLORS)
    score = 0
    time_remaining = time_limit
    grid_colors = [[(0, 0, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    fill_grid_with_colors() 
    game_over = False

def display_game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  

def main():
    global time_remaining, score, target_color, game_over
    restart_game()
    
    while True:
        screen.fill(BLACK)
        draw_grid()
        draw_target_color()
        draw_player()
        
        font = pygame.font.SysFont(None, 48)
        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        time_text = font.render("Time: {:.1f}".format(time_remaining), True, (255, 255, 255))
        screen.blit(score_text, (300, 555))
        screen.blit(time_text, (450, 555))
        
        if not game_over:
            time_remaining -= 1 / FPS

            if time_remaining <= 0:
                player_color = grid_colors[player_pos[0]][player_pos[1]]
                if player_color == target_color:
                    score += 5
                    time_remaining -= random.uniform(0.1, 0.3) 
                    target_color = random.choice(COLORS) 
                else:
                    game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_pos[0] > 0:
                player_pos[0] -= 1
            if keys[pygame.K_d] and player_pos[0] < GRID_SIZE - 1:
                player_pos[0] += 1
            if keys[pygame.K_w] and player_pos[1] > 0:
                player_pos[1] -= 1
            if keys[pygame.K_s] and player_pos[1] < GRID_SIZE - 1:
                player_pos[1] += 1
            
            clock.tick(FPS)
            pygame.display.flip()
        else:
            display_game_over()
            restart_game()

if __name__ == "__main__":
    fill_grid_with_colors()
    main()