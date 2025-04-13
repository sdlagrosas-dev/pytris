import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLOCK_START_SPEED = 1.0
BLOCK_MAX_SPEED = 0.08

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_CLOCK = pygame.time.Clock()
BG_MENU = pygame.image.load("assets/Background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
