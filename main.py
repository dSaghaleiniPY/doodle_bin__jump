# Example file showing a basic pygame "game loop"
import pygame
import random
pygame.init()

# configuration
SCREEN_WIDTH = 470
SCREEN_HEIGHT = 720
BG_COLOR = "#fdf1e7"

LEFT_BIN_IMAGE = pygame.image.load("bin_1.png")
RIGHT_BIN_IMAGE = pygame.image.load("bin_2.png")
SHOOTING_LEFT_BIN_IMAGE = pygame.image.load("shooting_left_bin.png")
SHOOTING_RIGHT_BIN_IMAGE = pygame.image.load("shooting_right_bin.png")
SHOOTING_BIN_IMAGE = pygame.image.load("shooting_bin.png")

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
starting_bin_y = bin_y
highest_bin_y = bin_y
camera_y = 0

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
    def __init__(self):
        self.x = random.randint(0, int(SCREEN_WIDTH - PLATFORM_WIDTH))
        self.y = random.randint(0, int(SCREEN_HEIGHT / 2))
    
    def draw(self):
        if game_y_to_screen(self.y) > SCREEN_HEIGHT:
            self.y = screen_y_to_game(SCREEN_HEIGHT) + 200
        pygame.draw.rect(screen, "#393939", (game_x_to_screen(self.x), game_y_to_screen(self.y), PLATFORM_WIDTH, PLATFORM_THICKNESS))
    
    def bounce_player(self):
        global bin_y_speed
        if (
            bin_x >= self.x - BIN_WIDTH / 2 and
            bin_x <= self.x + PLATFORM_WIDTH + BIN_WIDTH / 2 and
            bin_y >= self.y - PLATFORM_THICKNESS and
            bin_y <= self.y and
            bin_y_speed < 0
        ):
            bin_y_speed = 4.7

platform1 = Platform()
platform2 = Platform()
platform3 = Platform()
safety_platform = Platform()
platform1.y = bin_y - BIN_HEIGHT
platform2.y = bin_y - BIN_HEIGHT + 100
platform3.y = bin_y - BIN_HEIGHT + 200
safety_platform.y = 30
safety_platform.x = SCREEN_WIDTH / 2 - PLATFORM_WIDTH

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move down and jumping
    bin_y = bin_y + bin_y_speed
    if bin_y > highest_bin_y:
        highest_bin_y = bin_y
    camera_y = highest_bin_y - starting_bin_y

    bin_y_speed = bin_y_speed - 0.07
    platform1.bounce_player()
    platform2.bounce_player()
    platform3.bounce_player()
    safety_platform.bounce_player()

    # getting back on the screen when going off screen
    if bin_x > SCREEN_WIDTH + BIN_WIDTH/2:
        bin_x = -BIN_WIDTH/2
    if bin_x < -BIN_WIDTH/2:
        bin_x = SCREEN_WIDTH + BIN_WIDTH/2

    # move left and right
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        bin_x = bin_x - 3
    if pressed_keys[pygame.K_RIGHT]:
        bin_x = bin_x + 3
        
    # losing
    if bin_y <= -BIN_HEIGHT:
        BG_COLOR = ("#FFDCDC")
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, "#a3ce49", (game_x_to_screen(bin_x -(BIN_WIDTH/2)), game_y_to_screen(bin_y+BIN_HEIGHT), BIN_WIDTH, BIN_HEIGHT))
    platform1.draw()
    platform2.draw()
    platform3.draw()
    safety_platform.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
