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
PLATFORM_WIDTH = SCREEN_WIDTH / 2
PLATFORM_THICKNESS = 10

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

bin_x = SCREEN_WIDTH/2
bin_y = SCREEN_HEIGHT * .3
# platform_x = 75
# platform_y = bin_y + BIN_HEIGHT
bin_y_speed = 0

# helper functions
def game_x_to_screen(game_x):
    return game_x

def game_y_to_screen(game_y):
    return -game_y + 720

def game_coordinate_to_screen(game_x, game_y):
    return (game_x_to_screen(game_x), game_y_to_screen(game_y))

# classes
class Platform:
    def __init__(self):
        self.x = random.randint(0, int(SCREEN_WIDTH - PLATFORM_WIDTH))
        self.y = random.randint(0, int(SCREEN_HEIGHT / 2))
    
    def draw(self):
        pygame.draw.rect(screen, "#393939", (game_x_to_screen(self.x), game_y_to_screen(self.y), SCREEN_WIDTH/2, PLATFORM_THICKNESS))
    
    def bounce_player(self):
        global bin_y_speed
        if bin_y <= self.y and (
            bin_x + BIN_WIDTH / 2 >= self.x and
            bin_x - BIN_WIDTH / 2 <= self.x + PLATFORM_WIDTH and
            bin_y >= self.y - PLATFORM_THICKNESS and
            bin_y_speed > 0
        ):
            bin_y_speed = 4.7

platform1 = Platform()
platform2 = Platform()
platform3 = Platform()
platform1.y = bin_y - BIN_HEIGHT

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move down and jumping
    bin_y = bin_y + bin_y_speed
    bin_y_speed = bin_y_speed - 0.07
    platform1.bounce_player()
    platform2.bounce_player()
    platform3.bounce_player()
    # getting back on the screen when going off screen
    if bin_x > SCREEN_WIDTH:
        bin_x = - BIN_WIDTH/2
    if bin_x <= -BIN_WIDTH/2:
        bin_x = SCREEN_WIDTH + BIN_WIDTH/2

    # move left and right
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        bin_x = bin_x - 3
    if pressed_keys[pygame.K_RIGHT]:
        bin_x = bin_x + 3
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, "#a3ce49", (game_x_to_screen(bin_x -(BIN_WIDTH/2)), game_y_to_screen(bin_y+BIN_HEIGHT), BIN_WIDTH, BIN_HEIGHT))
    platform1.draw()
    platform2.draw()
    platform3.draw()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
