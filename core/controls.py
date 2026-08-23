"""
core/controls.py
"""
from __future__ import annotations

import pygame
from dataclasses import dataclass, field

from core.settings import GameState, ControlAction

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
        pygame.K_RETURN: ControlAction.CONFIRM,
        pygame.K_UP: ControlAction.MOVE_UP,
        pygame.K_DOWN: ControlAction.MOVE_DOWN,
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
   
    def get_held_actions(self, game_state: GameState) -> set[ControlAction]:
        """Continuous input - movement. Call once per frame."""
        bindings = self.held_bindings.get(game_state, {})
        if not bindings:
            return set()

        pressed = pygame.key.get_pressed()
        return {action for key, action in bindings.items() if pressed[key]}

    def get_event_actions(self, events: list[pygame.event.Event], game_state: GameState) -> list[ControlAction]:
        """
        Discrete input -- confirm, cancel, menu toggles, battle commands.
        Call once per frame with the events list from pygame.event.get().
        Returned in the order the keys were pressed so a frame with two
        keydowns doesn't silently drop one.
        """
        bindings = self.event_bindings.get(game_state, {})
        if not bindings:
            return []

        actions: list[ControlAction] = []
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in bindings:
                actions.append(bindings[event.key])
        return actions

    def movement_vector(self, game_state: GameState) -> pygame.Vector2:
        """
        Convenience helper for the world: turns held movement Actions
        into a normalized direction vector so diagonal movement isn't
        faster than cardinal movement.
        """
        held = self.get_held_actions(game_state)
        vector = pygame.Vector2(0, 0)

        if ControlAction.MOVE_UP in held:
            vector.y -= 1
        if ControlAction.MOVE_DOWN in held:
            vector.y += 1
        if ControlAction.MOVE_LEFT in held:
            vector.x -= 1
        if ControlAction.MOVE_RIGHT in held:
            vector.x += 1

        if vector.length_squared() > 0:
            vector = vector.normalize()

        return vector