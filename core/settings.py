"""
core/settings.py

All constants live here.

"""

import sys
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto

# system config
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
FRONTEND_DATA_DIR = BASE_DIR / "frontend" / "data"
PLAYER_SPRITE_DIR = FRONTEND_DATA_DIR / "sprites"
ITEM_SPRITE_DIR = FRONTEND_DATA_DIR / "items"
SFX_DIR = FRONTEND_DATA_DIR / "sfx"
BGM_DIR = FRONTEND_DATA_DIR / "bgm"
FONT_DIR = FRONTEND_DATA_DIR / "fonts"
MAP_DIR = BASE_DIR / "frontend" / "maps"

GAME_ICON_PATH = FRONTEND_DATA_DIR / "icon.png"


# game config
GAME_ICON = pygame.Surface((16, 16)) # need to create and set 'pygame.image.load("")
GAME_ICON.fill((255, 255, 255)) # delete once actual image is applied

GAME_NAME = "My Game Engine"

# Window config
TILE_SIZE = 32
SCALE = 2
SCREEN_TILE_X = 20
SCREEN_TILE_Y = 15
SCREEN_WIDTH = SCREEN_TILE_X * TILE_SIZE
SCREEN_HEIGHT = SCREEN_TILE_Y * TILE_SIZE
WINDOW_WIDTH = SCREEN_WIDTH * SCALE
WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE
FPS = 60

# Player config
PLAYER_SPEED = 5
ENEMY_SPEED = 3
MAX_INVENTORY_SIZE = 20
MAX_INVENTORY_STACK = 99


class Direction(Enum):
    """
    str + Enum so a Direction compares equal to a plain string too
    (Direction.DOWN == "down" is True).
    """
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"


# Game state - controls and main use this to determine which input mapping to use
class GameState(Enum):
    MAIN_MENU = auto()
    WORLD = auto()
    DIALOGUE = auto()
    BATTLE = auto()
    SHOP = auto()
    INVENTORY = auto()
    PAUSED = auto()


# Controller actions
class ControlAction(Enum):
    # continuous / held - checks every frame via get_held_actions function
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()

    # discrete - checks once per KEWDOWN via get_event_actions function
    CONFIRM = auto()
    CANCEL = auto()
    INTERACT = auto()
    MENU = auto()
    PAUSE = auto()

    # battle only discrete actions
    ATTACK1 = auto()
    ATTACK2 = auto()
    ATTACK3 = auto()
    ATTACK4 = auto()
    CYCLE_TARGET_LEFT = auto()
    CYCLE_TARGET_RIGHT = auto()


# Items / equipment config
class ItemType(Enum):
    CONSUMABLE = auto()
    WEAPON = auto()
    ARMOR = auto()
    ACCESSORY = auto()
    KEY_ITEM = auto()
    MATERIAL = auto()


class ItemRarity(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto ()
    EPIC = auto()
    lEGENDARY = auto()


class EquipSlot(Enum):
    WEAPON = auto()
    HEAD = auto()
    BODY = auto()
    ACCESSORY = auto()
    NONE = auto()

# Battle system
MAX_PARTY_SIZE = 4
MAX_ENEMIES = 6               
BOSS_ENCOUNTER_SIZE = 3 # boss fights: 1 boss + 2 adds instead of up to 6 regular enemies
ATB_GAUGE_MAX = 100.0
ATB_TICK_RATE = 10.0     


# basic colors (RGB/ RGBA)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
BEIGE = (245, 245, 220)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)
MAROON = (128, 0, 0)
GOLD = (218, 165, 32)
SILVER = (192, 192, 192)
LIME = (0, 255, 0)
AQUA = (0, 255, 255)
TURQUOISE = (64, 224, 208)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
CRIMSON = (220, 20, 60)
SALMON = (250, 128, 114)
TOMATO = (255, 99, 71)
CORAL = (255, 127, 80)
GOLDENROD = (218, 165, 32)
DARKRED = (139, 0, 0)
DARKGREEN = (0, 100, 0)
DARKBLUE = (0, 0, 139)
DARKCYAN = (0, 139, 139)
DARKMAGENTA = (139, 0, 139)
DARKORANGE = (255, 140, 0)
DARKVIOLET = (148, 0, 211)
DARKOLIVE = (85, 107, 47)
DARKTEAL = (0, 128, 128)
DARKPURPLE = (48, 25, 52)
LIGHTPINK = (255, 182, 193)
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)
LIGHTYELLOW = (255, 255, 224)
LIGHTCYAN = (224, 255, 255)
LIGHTMAGENTA = (255, 182, 193)
LIGHTORANGE = (255, 215, 0)
LIGHTPURPLE = (216, 191, 216)
LIGHTRED = (255, 99, 71)
DEEPSKYBLUE = (0, 191, 255)
SKYBLUE = (135, 206, 235)
DODGERBLUE = (30, 144, 255)
ROYALBLUE = (65, 105, 225)
SLATEBLUE = (106, 90, 205)
MEDIUMBLUE = (0, 0, 205)
STEELBLUE = (70, 130, 180)
CADETBLUE = (95, 158, 160)
SEAGREEN = (46, 139, 87)
MEDIUMSEAGREEN = (60, 179, 113)
SPRINGGREEN = (0, 255, 127)
MINTCREAM = (245, 255, 250)
HONEYDEW = (240, 255, 240)
ALICEBLUE = (240, 248, 255)
AZURE = (240, 255, 255)
IVORY = (255, 255, 240)
LINEN = (250, 240, 230)
WHEAT = (245, 222, 179)
SANDYBROWN = (244, 164, 96)
CHOCOLATE = (210, 105, 30)
SIENNA = (160, 82, 45)
PERU = (205, 133, 63)
TAN = (210, 180, 140)
UI_BACKGROUND = (20, 20, 30, 200)   # semi-transparent UI panels
HP_BAR = (200, 30, 30)
MP_BAR = (40, 100, 200)
ATB_BAR = (230, 200, 40)

# font presets
FONT_FAMILY_DEFAULT = "arial"
FONT_FAMILY_TITLE = "arial"
FONT_FAMILY_DIALOG = "arial"
FONT_FAMILY_MONO = "consolas"

FONT_TITLE_SIZE = 48
FONT_TITLE_SIZE_LARGE = 64
FONT_SUBTITLE_SIZE = 24
FONT_BODY_SIZE = 20
FONT_DIALOG_SIZE = 24
FONT_BUTTON_SIZE = 28
FONT_SMALL_SIZE = 16
FONT_LABEL_SIZE = 18
FONT_TOOLTIP_SIZE = 14

FONT_TITLE_STYLE = {"bold": True}
FONT_SUBTITLE_STYLE = {}
FONT_BODY_STYLE = {}
FONT_DIALOG_STYLE = {"bold": True}
FONT_BUTTON_STYLE = {"bold": True}
FONT_SMALL_STYLE = {}
FONT_LABEL_STYLE = {}
FONT_TOOLTIP_STYLE = {}
