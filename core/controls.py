"""
core/controls.py
"""

import pygame
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto

from core.settings import GameState


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

# keys checked continuously via pygame.key.get_pressed() - movement only.
_HELD_BINDINGS: dict[GameState, dict[int, ControlAction]] = {
    GameState.WORLD: {
        pygame.K_UP: ControlAction.MOVE_UP,
        pygame.K_w: ControlAction.MOVE_UP,
        pygame.K_DOWN: ControlAction.MOVE_DOWN,
        pygame.K_s: ControlAction.MOVE_DOWN,
        pygame.K_LEFT: ControlAction.MOVE_LEFT,
        pygame.K_a: ControlAction.MOVE_LEFT,
        pygame.K_RIGHT: ControlAction.MOVE_RIGHT,
        pygame.K_d: ControlAction.MOVE_RIGHT,
    },
}

# keys checked once per KEYDOWN event - menus, confirms, battle commands.
_EVENT_BINDINGS: dict[GameState, dict[int, ControlAction]] = {
    GameState.WORLD: {
        pygame.K_e: ControlAction.INTERACT,
        pygame.K_i: ControlAction.MENU,
        pygame.K_ESCAPE: ControlAction.PAUSE
    },
    GameState.MAIN_MENU: {
        pygame.K_UP: ControlAction.MOVE_UP,
        pygame.K_DOWN: ControlAction.MOVE_DOWN,
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_f: ControlAction.CONFIRM,
        pygame.K_ESCAPE: ControlAction.CANCEL,
        pygame.K_x: ControlAction.CANCEL, 
    },
    GameState.DIALOGUE: {
        pygame.K_f: ControlAction.CONFIRM,
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_x: ControlAction.CANCEL,
        pygame.K_ESCAPE: ControlAction.CANCEL,
    },
    GameState.BATTLE: {
        pygame.K_f: ControlAction.CONFIRM,
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_x: ControlAction.CANCEL,
        pygame.K_a: ControlAction.ATTACK1,
        pygame.K_d: ControlAction.ATTACK2,
        pygame.K_i: ControlAction.ATTACK3,
        pygame.K_f: ControlAction.ATTACK4,
        pygame.K_LEFT: ControlAction.CYCLE_TARGET_LEFT,
        pygame.K_RIGHT: ControlAction.CYCLE_TARGET_RIGHT,
    },
    GameState.SHOP: {
        pygame.K_UP: ControlAction.MOVE_UP,
        pygame.K_DOWN: ControlAction.MOVE_DOWN,
        pygame.K_z: ControlAction.CONFIRM,
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_x: ControlAction.CANCEL,
        pygame.K_ESCAPE: ControlAction.CANCEL,
    },
    GameState.INVENTORY: {
        pygame.K_UP: ControlAction.MOVE_UP,
        pygame.K_DOWN: ControlAction.MOVE_DOWN,
        pygame.K_LEFT: ControlAction.MOVE_LEFT,
        pygame.K_RIGHT: ControlAction.MOVE_RIGHT,
        pygame.K_z: ControlAction.CONFIRM,
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_x: ControlAction.CANCEL,
        pygame.K_ESCAPE: ControlAction.CANCEL,
    },
    GameState.PAUSED: {
        pygame.K_ESCAPE: ControlAction.CANCEL,
        pygame.K_z: ControlAction.CONFIRM,
    },
}


@dataclass
class Controls:
    """
    Central input handler. One instance lives for the whole game session.
    Calls get_held_actions for every frame for continuous input, and pass the frame's
    pygame event list to get_event_actions for discrete button presses. Both takes the 
    current GameState so that the same keys can mean something different.
    """

    held_bindings: dict[GameState, dict[int, ControlAction]] = field(
        default_factory=lambda: _HELD_BINDINGS
    )

    event_bindings: dict[GameState, dict[int, ControlAction]] = field(
        default_factory=lambda: _EVENT_BINDINGS
    )
