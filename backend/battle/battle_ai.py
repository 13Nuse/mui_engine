"""
backend/battle/battle_ai.py

Basic minimal enemy decision making. Once the battle loop calls for an enemy action,
we use the random module to pick an alive party member to attack, nothing else, no magic, nada. 
will build up on that at another time.
"""
from __future__ import annotations

import random

from backend.battle.actions import ActionType, BattleAction
from backend.battle.combatant import Combatant


def decide_enemy_action(enemy: Combatant, party: list[Combatant]) -> BattleAction:
    alive_targets = [combatant for combatant in party if combatant.is_alive]
    targets = [random.choice(alive_targets)] if alive_targets else []
    return BattleAction(actor=enemy, action_type=ActionType.ATTACK, targets=targets)