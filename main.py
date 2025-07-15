import random
import pygame

# Initialize pygame
pygame.init()

# Constants
FPS = 60
GRAVITY = 0.6
JUMP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue background

# Game states
START_SCREEN = "start"
SETTINGS_SCREEN = "settings"
GAME_RUNNING = "running"
GAME_OVER_SCREEN = "game_over"

# Initialize settings
pipe_gap = PIPE_GAP
game_speed = 3
gravity = GRAVITY
music_on = True


# Game classes
class Bird:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, 34, 24)  # Bird as a rectangle
        self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += gravity
        self.rect.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)  # Draw the bird as a yellow rectangle


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + pipe_gap, PIPE_WIDTH,
                                       SCREEN_HEIGHT - self.height - pipe_gap)

    def update(self):
        self.x -= game_speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.top_rect)  # Draw the top pipe as a black rectangle
        pygame.draw.rect(screen, BLACK, self.bottom_rect)  # Draw the bottom pipe as a black rectangle


def display_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def start_screen(screen):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Press S to Start", 50, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60)
    display_text(screen, "Press C for Settings", 50, BLACK, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2)
    display_text(screen, "Press Q to Quit", 50, BLACK, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 60)
    pygame.display.flip()


def settings_screen(screen):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Settings", 50, BLACK, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 160)
    display_text(screen, f"1: Increase Speed ({game_speed})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 - 80)
    display_text(screen, f"2: Decrease Speed ({game_speed})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 - 40)
    display_text(screen, f"3: Increase Pipe Gap ({pipe_gap})", 40, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    display_text(screen, f"4: Decrease Pipe Gap ({pipe_gap})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 + 40)
    display_text(screen, f"5: Toggle Music ({'On' if music_on else 'Off'})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 + 80)
    display_text(screen, f"6: Increase Gravity ({gravity:.1f})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 + 120)
    display_text(screen, f"7: Decrease Gravity ({gravity:.1f})", 40, BLACK, SCREEN_WIDTH // 2 - 100,
                 SCREEN_HEIGHT // 2 + 160)
    display_text(screen, "Press B to Go Back", 40, BLACK, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 220)
    pygame.display.flip()


def game_over_screen(screen, score):
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Game Over", 70, BLACK, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
    display_text(screen, f"Score: {score}", 50, BLACK, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    display_text(screen, "Press R to Restart", 50, BLACK, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100)
    pygame.display.flip()


def toggle_music():
    global music_on
    try:
        if music_on:
            pygame.mixer.music.play(-1)  # Loop music indefinitely
        else:
            pygame.mixer.music.stop()
    except pygame.error as e:
        print(f"Music error: {e}. Music will not play.")


def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, pipe_gap, game_speed, gravity, music_on
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)  # Allow resizing
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    state = START_SCREEN  # Start at the start screen
    bird = Bird()
    pipes = []
    score = 0
    frame_count = 0

    # Load music with error handling
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("background_music.mp3")
    except pygame.error as e:
        print(f"Error loading music: {e}. Continuing without music.")
        music_on = False  # Disable music if the file is missing

    toggle_music()  # Start music if enabled

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                # Update screen size and recreate the screen surface
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if state == START_SCREEN:
                    if event.key == pygame.K_s:
                        state = GAME_RUNNING
                        bird = Bird()
                        pipes = []
                        score = 0
                        frame_count = 0
                    elif event.key == pygame.K_c:
                        state = SETTINGS_SCREEN
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
                elif state == SETTINGS_SCREEN:
                    if event.key == pygame.K_1:  # Increase speed
                        game_speed += 1
                    elif event.key == pygame.K_2 and game_speed > 1:  # Decrease speed (min 1)
                        game_speed -= 1
                    elif event.key == pygame.K_3:  # Increase pipe gap
                        pipe_gap += 10
                    elif event.key == pygame.K_4 and pipe_gap > 50:  # Decrease pipe gap (min 50)
                        pipe_gap -= 10
                    elif event.key == pygame.K_5:  # Toggle music
                        music_on = not music_on
                        toggle_music()
                    elif event.key == pygame.K_6:  # Increase gravity
                        gravity += 0.1
                    elif event.key == pygame.K_7 and gravity > 0.1:  # Decrease gravity (min 0.1)
                        gravity -= 0.1
                    elif event.key == pygame.K_b:  # Go back to start screen
                        state = START_SCREEN
                elif state == GAME_RUNNING:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif state == GAME_OVER_SCREEN:
                    if event.key == pygame.K_r:
                        state = START_SCREEN

        if state == START_SCREEN:
            start_screen(screen)

        elif state == GAME_RUNNING:
            bird.update()
            if frame_count % 90 == 0:
                pipes.append(Pipe(SCREEN_WIDTH))
            for pipe in pipes:
                pipe.update()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    state = GAME_OVER_SCREEN
            if bird.rect.y > SCREEN_HEIGHT or bird.rect.y < 0:
                state = GAME_OVER_SCREEN
            screen.fill(BACKGROUND_COLOR)
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)
            display_text(screen, f'Score: {score}', 36, BLACK, 10, 10)
            pygame.display.flip()
            frame_count += 1

        elif state == SETTINGS_SCREEN:
            settings_screen(screen)

        elif state == GAME_OVER_SCREEN:
            game_over_screen(screen, score)

        clock.tick(FPS)



if __name__ == "__main__":
    main()
