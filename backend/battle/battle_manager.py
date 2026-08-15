"""
backend/battle/battle_manager.py

Creates one battle, the party, the enemies and turn order. Every module comes here then renders to the frontend.
Will build a more advance encounter shape to account for party average lvl.

Parties turn gauge will fill each frame by their speed stat, and equipment.
Would like to implement slowing down the gauge if hit by and enemy combatant.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.settings import ATB_TICK_RATE, BOSS_ENCOUNTER_SIZE, MAX_ENEMIES, MAX_PARTY_SIZE, BattleResult
from backend.battle.actions import ActionType, BattleAction, BattleActionResult, resolve_action
from backend.battle.combatant import Combatant, CombatantSide
from backend.battle.battle_ai import decide_enemy_action


@dataclass
class BattleManager:
    party: list[Combatant]
    enemies: list[Combatant]

    ready_queue: list[Combatant] = field(default_factory=list, init=False, repr=False)
    log: list[str] = field(default_factory=list, init=False, repr=False)
    result: BattleResult = field(default=BattleResult.ONGOING, init=False)

    def __post_init__(self) -> None:
        if len(self.party) > MAX_PARTY_SIZE:
            raise ValueError(
                f"party has {len(self.party)} members, exceeds MAX_PARTY_SIZE ({MAX_PARTY_SIZE})"
            )

        is_boss_fight = any(enemy.is_boss for enemy in self.enemies)
        limit = BOSS_ENCOUNTER_SIZE if is_boss_fight else MAX_ENEMIES
        if len(self.enemies) > limit:
            kind = "boss encounter" if is_boss_fight else "regular encounter"
            raise ValueError(
                f"{kind} has {len(self.enemies)} enemies, exceeds limit of {limit}"
            )

    def all_combatants(self) -> list[Combatant]:
        return self.party + self.enemies

    def all_party_members(self) -> list[Combatant]:
        return self.party

    def all_enemies(self) -> list[Combatant]: # I need seperation for handling sprite placements
        return self.enemies

    # timing
    def update(self, dt: float) -> None:
        """
        Call once per frame while the battle is BattleResult.ONGOING. Fills the gauges
        and moves the ready combatants into the turn ques.
        """

        if self.result != BattleResult.ONGOING:
            return

        for combatant in self.all_combatants():
            if not combatant.is_alive or combatant in self.ready_queue:
                continue
            combatant.tick_atb(dt, ATB_TICK_RATE)
            if combatant.is_ready:
                self.ready_queue.append(combatant)

    def peek_next_actor(self) -> Combatant | None:
        """The next combatant waiting on an action, or None if nobody's ready yet."""
        return self.ready_queue[0] if self.ready_queue else None

    # actions
    def submit_action(self, action: BattleAction) -> BattleActionResult:
        """
        Resolves a queued action (from either side) and updates battle
        state. Raises ValueError if the actor isn't actually at the front
        of the ready queue.
        """
        actor = action.actor
        if not self.ready_queue or self.ready_queue[0] is not actor:
            raise ValueError(f"{actor.name} is not next in the ready queue")

        if action.action_type != ActionType.DEFEND:
            actor.is_defending = False

        result = resolve_action(action)
        self.ready_queue.pop(0)
        actor.reset_atb()
        self.log.append(result.message)

        if result.fled:
            self.result = BattleResult.FLED
        else:
            self._update_result()

        return result

    def decide_and_submit_enemy_turn(self) -> BattleActionResult | None:
        """
        If the next ready actor is an enemy, let backend.battle.ai 
        decide its action and resolve it. Returns None if it isn't an enemy's turn.
        """
        actor = self.peek_next_actor()
        if actor is None or actor.side != CombatantSide.ENEMY:
            return None
        return self.submit_action(decide_enemy_action(actor, self.party))

    def get_flee_action(self, actor: Combatant) -> BattleAction:
        opposition = self.enemies if actor.side == CombatantSide.PLAYER else self.party
        return BattleAction(
            actor=actor,
            action_type=ActionType.FLEE,
            targets=[combatant for combatant in opposition if combatant.is_alive],
        )

    # battle state
    def _update_result(self) -> None:
        if all(not combatant.is_alive for combatant in self.party):
            self.result = BattleResult.DEFEAT
        elif all(not combatant.is_alive for combatant in self.enemies):
            self.result = BattleResult.VICTORY

    def get_state_snapshot(self) -> dict:
        """
        Dictionary view for the frontend to render.
        """
        return {
            "party": [_combatant_snapshot(combatant) for combatant in self.party],
            "enemies": [_combatant_snapshot(combatant) for combatant in self.enemies],
            "ready_queue": [combatant.name for combatant in self.ready_queue],
            "result": self.result.name,
            "log": list(self.log[-5:]), # last few messages for battle log UI
        }


def _combatant_snapshot(combatant: Combatant) -> dict:
    return {
        "name": combatant.name,
        "hp": combatant.current_hp,
        "max_hp": combatant.stats.max_hp,
        "mp": combatant.current_mp,
        "max_mp": combatant.stats.max_mp,
        "atb": combatant.atb_gauge,
        "alive": combatant.is_alive,
        "defending": combatant.is_defending,
        "is_boss": combatant.is_boss,
    }
