from dataclasses import dataclass
from typing import List

from backend.inventory.models import Inventory

@dataclass
class Player:
    id: int
    username: str
    password_hash: str
    created_at: str
    updated_at: str
    inventory: List[Inventory]

    def __str__(self) -> str:
        return f"username={self.username}"
    

@dataclass
class CharacterStats:
    id: int
    name: str
    level: int
    experience: int
    experience_to_next_level: int

    base_health: int
    base_mana: int
    base_attack: int
    base_magic_attack: int
    base_magic_defense: int
    base_defense: int
    base_speed: int

    base_critical_chance: float
    base_critical_damage: float
    base_health_regeneration: float
    base_mana_regeneration: float
    base_luck: float
    base_dodge_chance: float
    base_block_chance: float
    base_accuracy: float
    base_resistance: float
    sprite: str

    def gain_experience(self, amount: int) -> int:
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            amount_left = self.experience_to_next_level - amount     
            self.level_up()
        return amount_left

    def level_up(self) -> None: # these hardcoded values are just for demonstration purposes will be replaced with classes
        self.level += 1
        self.experience = 0
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        self.base_health += 10
        self.base_mana += 5
        self.base_attack += 2
        self.base_magic_attack += 2
        self.base_defense += 1
        self.base_speed += 1
        self.base_critical_chance += 0.01
        self.base_critical_damage += 0.05
        self.base_health_regeneration += 0.1
        self.base_mana_regeneration += 0.05
        self.base_luck += 0.01
        self.base_dodge_chance += 0.01
        self.base_block_chance += 0.01
        self.base_accuracy += 0.01
        self.base_resistance += 0.01

    def attack_hit_or_miss(self, target) -> bool:
        hit_chance = self.base_accuracy - target.base_dodge_chance
        return hit_chance >= 0.5  # Assuming a hit chance of 50% or more results in a hit, will build something better later

    def take_damage(self, damage: int) -> int:
        actual_damage = max(0, damage - self.base_defense)
        self.base_health -= actual_damage
        if self.base_health < 0:
            self.base_health = 0
        return actual_damage


    def __str__(self) -> str:
        return f"CharacterStats(id={self.id}, 
        name={self.name}, 
        level={self.level}, 
        experience={self.experience}, 
        experience_to_next_level={self.experience_to_next_level}, 
        base_health={self.base_health}, base_mana={self.base_mana}, 
        base_attack={self.base_attack}, base_magic_attack={self.base_magic_attack}, 
        base_defense={self.base_defense}, base_speed={self.base_speed}, 
        base_critical_chance={self.base_critical_chance}, 
        base_critical_damage={self.base_critical_damage}, 
        base_health_regeneration={self.base_health_regeneration}, 
        base_mana_regeneration={self.base_mana_regeneration}, 
        base_luck={self.base_luck}, base_dodge_chance={self.base_dodge_chance}, 
        base_block_chance={self.base_block_chance}, base_accuracy={self.base_accuracy}, 
        base_resistance={self.base_resistance})"


@dataclass
class NPC:
    id: int
    name: str
    description: str
    location: str
    dialogue: List[str]


@dataclass
class Enemy(CharacterStats):
    experience_reward: int
