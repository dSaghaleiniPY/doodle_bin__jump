# Example file showing a basic pygame "game loop"
import pygame
import random
pygame.init()

# configuration
SCREEN_WIDTH = 470
SCREEN_HEIGHT = 720
BG_COLOR = "#fdf1e7"

SCORE_FONT = pygame.font.SysFont("Arial", 30)

LEFT_BIN_IMAGE = pygame.image.load("bin_1.png")
RIGHT_BIN_IMAGE = pygame.image.load("bin_2.png")
SHOOTING_LEFT_BIN_IMAGE = pygame.image.load("shooting_left_bin.png")
SHOOTING_RIGHT_BIN_IMAGE = pygame.image.load("shooting_right_bin.png")
SHOOTING_BIN_IMAGE = pygame.image.load("shooting_bin.png")
LEFT_BIN_BALLIN_IMAGE = pygame.image.load("BIN_BALLIN!.png")
RIGHT_BIN_BALLIN_IMAGE = pygame.image.load("BIN_BALLIN 2!.png")

CURRENT_BIN_IMAGE = LEFT_BIN_IMAGE

BIN_WIDTH = 50
BIN_HEIGHT = 64
PLATFORM_WIDTH = SCREEN_WIDTH / 6
PLATFORM_THICKNESS = 10

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

bin_x = SCREEN_WIDTH/2
bin_y = SCREEN_HEIGHT * .3
bin_shooting = 0
starting_bin_y = bin_y
highest_bin_y = bin_y
camera_y = 0

platforms_to_hide = 0
hidden_platforms = 0

# platform_x = 75
# platform_y = bin_y + BIN_HEIGHT
bin_y_speed = 0

# helper functions
def game_x_to_screen(game_x):
    return game_x

def game_y_to_screen(game_y):
    return -game_y + SCREEN_HEIGHT + camera_y

def screen_y_to_game(screen_y):
    return -screen_y + SCREEN_HEIGHT + camera_y

def game_coordinate_to_screen(game_x, game_y):
    return (game_x_to_screen(game_x), game_y_to_screen(game_y))

# classes
class Platform:
    # types of platforms:
    # 0: normal
    # 1: bouncy
    def __init__(self, starting_y):
        self.x = random.randint(0, int(SCREEN_WIDTH - PLATFORM_WIDTH))
        self.y = starting_y
        self.active = True
        self.pick_settings()

    def pick_settings(self):
        self.bouncy = random.randint(1,8) == 1
        self.breaks = random.randint(1,7) == 1
        if random.randint(1, 10) == 1:
            self.x_speed = 3
        else:
            self.x_speed = 0

    def make_platform_move(self):
        if self.active:
            self.x += self.x_speed
            if self.x >= SCREEN_WIDTH - 10 - PLATFORM_WIDTH:
                self.x_speed *= -1
            if self.x <= 10:
                self.x_speed *= -1
    
    def reset_platform(self):
        self.y += SCREEN_HEIGHT
        self.x = random.randint(0, int(SCREEN_WIDTH - PLATFORM_WIDTH))
        self.pick_settings()
    
    def draw(self):
        global platforms_to_hide
        global hidden_platforms
        if self.active:
            if game_y_to_screen(self.y) > SCREEN_HEIGHT:
                if hidden_platforms < platforms_to_hide and random.randint(1,5) == 1:
                    hidden_platforms += 1
                    self.active = False
                else:
                    self.reset_platform()
            if self.breaks:
                pygame.draw.rect(screen, "#e76349", (game_x_to_screen(self.x), game_y_to_screen(self.y), PLATFORM_WIDTH, PLATFORM_THICKNESS))
            elif self.bouncy:
                pygame.draw.rect(screen, "#a3ce49", (game_x_to_screen(self.x), game_y_to_screen(self.y), PLATFORM_WIDTH, PLATFORM_THICKNESS))
            else:
                pygame.draw.rect(screen, "#393939", (game_x_to_screen(self.x), game_y_to_screen(self.y), PLATFORM_WIDTH, PLATFORM_THICKNESS))

    def bounce_player(self):
        global bin_y_speed
        if self.active:
            if (
                bin_x >= self.x - BIN_WIDTH / 2 and
                bin_x <= self.x + PLATFORM_WIDTH + BIN_WIDTH / 2 and
                bin_y >= self.y - PLATFORM_THICKNESS and
                bin_y <= self.y and
                bin_y_speed < 0
            ):
                if self.breaks:
                    self.reset_platform()
                elif self.bouncy:
                    bin_y_speed = 7.5
                else:
                    bin_y_speed = 5.6

platforms = [
    Platform(30), # starting platform
    Platform(30 + bin_y - BIN_HEIGHT),
    Platform(30 + bin_y - BIN_HEIGHT + 100),
    Platform(30 + bin_y - BIN_HEIGHT + 200),
    Platform(30 + bin_y - BIN_HEIGHT + 300),
    Platform(30 + bin_y - BIN_HEIGHT + 400),
    Platform(30 + bin_y - BIN_HEIGHT + 450),
    Platform(30 + bin_y - BIN_HEIGHT + 500),
    Platform(30 + bin_y - BIN_HEIGHT + 600),
    Platform(30 + bin_y - BIN_HEIGHT + 650),
    Platform(30 + bin_y - BIN_HEIGHT + 700),
    Platform(30 + bin_y - BIN_HEIGHT + 800),
    Platform(30 + bin_y - BIN_HEIGHT + 850)
]
platforms[0].x = SCREEN_WIDTH / 2 - PLATFORM_WIDTH

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # shooting
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bin_shooting = 10

    # score
    score = camera_y/3

    # move down and jumping
    bin_y = bin_y + bin_y_speed
    if bin_y > highest_bin_y:
        highest_bin_y = bin_y
    camera_y = highest_bin_y - starting_bin_y
    bin_y_speed = bin_y_speed - 0.07

    # timers
    bin_shooting -= 1

    for platform in platforms:
        platform.bounce_player()
        platform.make_platform_move()

    # getting back on the screen when going off screen
    if bin_x > SCREEN_WIDTH + BIN_WIDTH/2:
        bin_x = -BIN_WIDTH/2
    if bin_x < -BIN_WIDTH/2:
        bin_x = SCREEN_WIDTH + BIN_WIDTH/2

    # moving
    pressed_keys = pygame.key.get_pressed()
    if score < 6500:
        if pressed_keys[pygame.K_LEFT]:
            bin_x = bin_x - 3
            CURRENT_BIN_IMAGE = LEFT_BIN_IMAGE
        if pressed_keys[pygame.K_RIGHT]:
            bin_x = bin_x + 3
            CURRENT_BIN_IMAGE = RIGHT_BIN_IMAGE
    else:
        if pressed_keys[pygame.K_LEFT]:
            bin_x = bin_x - 3
            CURRENT_BIN_IMAGE = LEFT_BIN_BALLIN_IMAGE
        if pressed_keys[pygame.K_RIGHT]:
            bin_x = bin_x + 3
            CURRENT_BIN_IMAGE = RIGHT_BIN_BALLIN_IMAGE

    if bin_shooting > 0:
        CURRENT_BIN_IMAGE = SHOOTING_BIN_IMAGE
    
    # losing
    if game_y_to_screen(bin_y) >= SCREEN_HEIGHT + BIN_HEIGHT:
        BG_COLOR = ("#FFDCDC")
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)

    screen.blit(CURRENT_BIN_IMAGE, (game_x_to_screen(bin_x -(BIN_WIDTH/2)), game_y_to_screen(bin_y+BIN_HEIGHT)))
    for platform in platforms:
        platform.draw()

    # score
    SCORE_IMAGE = SCORE_FONT.render(str(int(score)), True, "black")
    screen.blit(SCORE_IMAGE, (10, 10))

    # changing overtime
    if score >= 300:
        platforms_to_hide = 2
    if score >= 600:
        platforms_to_hide = 4

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
