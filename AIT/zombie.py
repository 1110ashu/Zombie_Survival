import pygame
import sys
import random

pygame.init()

# ---------------- SOUND SETUP ----------------
try:
    pygame.mixer.init()
    print("Mixer initialized")
except Exception as e:
    print("Mixer Error:", e)

# Background Music
try:
    pygame.mixer.music.load("bg_music.wav")   # use WAV
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    print("Background music loaded")
except Exception as e:
    print("Music Error:", e)

# Sound Effects
try:
    move_sound = pygame.mixer.Sound("move.wav")
    print("Move sound loaded")
except Exception as e:
    print("Move sound error:", e)
    move_sound = None

try:
    win_sound = pygame.mixer.Sound("win.wav")
    print("Win sound loaded")
except Exception as e:
    print("Win sound error:", e)
    win_sound = None

try:
    lose_sound = pygame.mixer.Sound("lose.wav")
    print("Lose sound loaded")
except Exception as e:
    print("Lose sound error:", e)
    lose_sound = None

# ---------------- WINDOW ----------------
WIDTH = 600
ROWS = 20
UI_HEIGHT = 80
GAP = (WIDTH - UI_HEIGHT) // ROWS

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Zombie Survival Game")

# Fonts
FONT = pygame.font.SysFont("arial", 22)
BIG_FONT = pygame.font.SysFont("arial", 42)

# Colors
BG_COLOR = (20, 20, 30)
GRID_COLOR = (50, 50, 70)
PLAYER_COLOR = (0, 255, 120)
ZOMBIE_COLOR = (200, 0, 0)
SAFE_COLOR = (0, 150, 255)
UI_BAR = (30, 30, 50)

# ---------------- GLOW ----------------
def draw_glow(win, color, x, y, offset_x, offset_y):
    for i in range(3):
        pygame.draw.rect(win, color,
            (x*GAP - i + offset_x,
             y*GAP + UI_HEIGHT - i + offset_y,
             GAP + i*2, GAP + i*2), 1)

# ---------------- DRAW ----------------
def draw(player, zombies, safe, score, level, time_left, shake=0):
    offset_x = random.randint(-shake, shake)
    offset_y = random.randint(-shake, shake)

    WIN.fill(BG_COLOR)

    # UI bar
    pygame.draw.rect(WIN, UI_BAR, (offset_x, offset_y, WIDTH, UI_HEIGHT))

    score_text = FONT.render(f"Score: {score}", True, (255,255,255))
    level_text = FONT.render(f"Level: {level}", True, (255,255,255))
    time_text = FONT.render(f"Time: {time_left}s", True, (255,100,100))

    WIN.blit(score_text, (10 + offset_x, 10 + offset_y))
    WIN.blit(level_text, (10 + offset_x, 35 + offset_y))
    WIN.blit(time_text, (10 + offset_x, 60 + offset_y))

    # Grid
    for i in range(ROWS):
        for j in range(ROWS):
            x = i * GAP + offset_x
            y = j * GAP + UI_HEIGHT + offset_y

            pygame.draw.rect(WIN, GRID_COLOR, (x, y, GAP, GAP), 1)

            if (i, j) == player:
                pygame.draw.rect(WIN, PLAYER_COLOR,
                                 (x+3, y+3, GAP-6, GAP-6), border_radius=8)
                draw_glow(WIN, PLAYER_COLOR, i, j, offset_x, offset_y)

            elif (i, j) in zombies:
                pygame.draw.rect(WIN, ZOMBIE_COLOR,
                                 (x+2, y+2, GAP-4, GAP-4), border_radius=6)

            elif (i, j) == safe:
                pygame.draw.rect(WIN, SAFE_COLOR,
                                 (x+2, y+2, GAP-4, GAP-4), border_radius=6)

    pygame.display.update()

# ---------------- ZOMBIE SPREAD ----------------
def spread_zombies(zombies):
    new_zombies = set(zombies)
    for zx, zy in zombies:
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = zx + dx, zy + dy
            if 0 <= nx < ROWS and 0 <= ny < ROWS:
                new_zombies.add((nx, ny))
    return list(new_zombies)

# ---------------- START SCREEN ----------------
def start_screen():
    while True:
        WIN.fill((10,10,20))

        title = BIG_FONT.render("Zombie Survival", True, (0,255,120))
        start = FONT.render("Press ENTER to Start", True, (255,255,255))

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        WIN.blit(start, (WIDTH//2 - start.get_width()//2, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            break

# ---------------- GAME OVER ----------------
def show_message(text):
    pygame.mixer.music.stop()

    while True:
        WIN.fill((10,10,20))

        msg = BIG_FONT.render(text, True, (255,50,50))
        sub = FONT.render("Press R to Restart", True, (200,200,200))

        WIN.blit(msg, (WIDTH//2 - msg.get_width()//2, 250))
        WIN.blit(sub, (WIDTH//2 - sub.get_width()//2, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_r]:
            main()

# ---------------- MAIN GAME ----------------
def main():
    player = (0, 0)
    safe = (ROWS - 1, ROWS - 1)
    zombies = [(random.randint(5,15), random.randint(5,15))]

    clock = pygame.time.Clock()

    score = 0
    level = 1
    time_limit = 30

    last_spread = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        clock.tick(10)

        elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = time_limit - elapsed

        draw(player, zombies, safe, score, level, time_left)

        if time_left <= 0:
            if lose_sound: lose_sound.play()

            for _ in range(20):
                draw(player, zombies, safe, score, level, time_left, shake=10)
                pygame.time.delay(30)

            show_message("Time Over!")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()

        # Movement
        keys = pygame.key.get_pressed()
        x, y = player

        if keys[pygame.K_UP] and y > 0:
            player = (x, y - 1)
            if move_sound: move_sound.play()

        if keys[pygame.K_DOWN] and y < ROWS - 1:
            player = (x, y + 1)
            if move_sound: move_sound.play()

        if keys[pygame.K_LEFT] and x > 0:
            player = (x - 1, y)
            if move_sound: move_sound.play()

        if keys[pygame.K_RIGHT] and x < ROWS - 1:
            player = (x + 1, y)
            if move_sound: move_sound.play()

        # Zombie spread
        current_time = pygame.time.get_ticks()
        speed = max(1000 - (level * 120), 250)

        if current_time - last_spread > speed:
            zombies = spread_zombies(zombies)
            last_spread = current_time

        # Lose
        if player in zombies:
            if lose_sound: lose_sound.play()

            for _ in range(20):
                draw(player, zombies, safe, score, level, time_left, shake=10)
                pygame.time.delay(30)

            show_message("Zombies Got You!")
            break

        # Win
        if player == safe:
            if win_sound: win_sound.play()

            score += 10
            level += 1
            time_limit += 5

            player = (0, 0)
            zombies = [(random.randint(5,15), random.randint(5,15))]
            start_ticks = pygame.time.get_ticks()

# ---------------- RUN ----------------
start_screen()
main()