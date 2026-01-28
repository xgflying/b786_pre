# game_constants.py
from enum import Enum

# Screen and grid constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (220, 20, 20)
DARK_RED = (180, 0, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (20, 20, 60)
GRAY = (128, 128, 128)
BROWN = (101, 67, 33)
APPLE_GREEN = (50, 150, 50)
YELLOW = (255, 255, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PowerUpType(Enum):
    SLOW_DOWN = "slow_down"
    WALL_IMMUNITY = "wall_immunity"