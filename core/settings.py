import os
import sys
from dataclasses import dataclass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


GAME_ICON = "" # need to create and set 'pygame.image.load("")
GAME_NAME = "My Game"

TILE_SIZE = 32
SCALE = 2
SCREEN_TILE_X = 20
SCREEN_TILE_Y = 15
SCREEN_WIDTH = SCREEN_TILE_X * TILE_SIZE
SCREEN_HEIGHT = SCREEN_TILE_Y * TILE_SIZE
WINDOW_WIDTH = SCREEN_WIDTH * SCALE
WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE
FPS = 60
DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"] # may add more directions later if using a controller
PLAYER_SPEED = 5
ENEMY_SPEED = 3
MAX_INVENTORY_SIZE = 20

