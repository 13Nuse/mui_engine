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
    max_health: int
    base_mana: int
    max_mana: int
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

    def reset_stats_on_level_up(self) -> None:
        self.base_health = self.max_health
        self.base_mana = self.max_mana

    def first_strike(self, target) -> bool: # who attacks first, the one with the higher speed stat will attack first
        return self.base_speed > target.base_speed

    def attack(self, target) -> int:
        if self.attack_hit_or_miss(target):
            damage = self.calculate_damage(target)
            damage = self.critical_hit(damage)
            if target.dodge_attack(damage):
                return 0  # Attack was dodged
            damage = target.block_attack(damage)
            actual_damage = target.take_damage(damage)
            return actual_damage
        else:
            return 0  # Attack missed

    def attack_hit_or_miss(self, target) -> bool:
        hit_chance = self.base_accuracy - target.base_dodge_chance
        return hit_chance >= 0.5  # Assuming a hit chance of 50% or more results in a hit, will build something better later

    def calculate_damage(self, target) -> int:
        damage = self.base_attack - target.base_defense
        return max(0, damage)  # Ensure damage is not negative

    def critical_hit(self, damage: int) -> int:
        if self.base_critical_chance >= 0.5:  # Assuming a critical chance of 50% or more results in a critical hit, will build something better later
            return int(damage * self.base_critical_damage)
        return damage

    def dodge_attack(self, damage: int) -> bool:
        dodge_chance = self.base_dodge_chance
        return dodge_chance >= 0.5  # Assuming a dodge chance of 50% or more results in a dodge, will build something better later

    def counter_attack(self, target) -> bool:
        counter_chance = target.base_speed - self.base_speed
        return counter_chance >= 0.5  # Assuming a counter chance of 50% or more results in a counter attack, will build something better later
    
    def block_attack(self, damage: int) -> int:
        block_chance = self.base_block_chance
        if block_chance >= 0.5:  # Assuming a block chance of 50% or more results in a block, will build something better later
            return int(damage * (1 - self.base_defense / 100))  # Assuming defense reduces damage by a percentage, will build something better later
        return damage
  
    def take_damage(self, damage: int) -> int:
        actual_damage = max(0, damage - self.base_defense)
        self.base_health -= actual_damage
        if self.base_health < 0:
            self.base_health = 0
        return actual_damage

    def heal(self, amount: int) -> None:
        self.base_health = min(self.max_health, self.base_health + amount)

    def regenerate_health(self) -> None:
        self.base_health = min(self.max_health, self.base_health + self.base_health_regeneration)

    def use_mana(self, amount: int) -> bool:
        if self.base_mana >= amount:
            self.base_mana -= amount
            return True
        return False

    def restore_mana(self, amount: int) -> None:
        self.base_mana = min(self.max_mana, self.base_mana + amount)

    def regenerate_mana(self) -> None:
        self.base_mana = min(self.max_mana, self.base_mana + self.base_mana_regeneration)

    def is_alive(self) -> bool:
        return self.base_health > 0

    def get_stats(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "experience_to_next_level": self.experience_to_next_level,
            "base_health": self.base_health,
            "max_health": self.max_health,
            "base_mana": self.base_mana,
            "max_mana": self.max_mana,
            "base_attack": self.base_attack,
            "base_magic_attack": self.base_magic_attack,
            "base_magic_defense": self.base_magic_defense,
            "base_defense": self.base_defense,
            "base_speed": self.base_speed,
            "base_critical_chance": self.base_critical_chance,
            "base_critical_damage": self.base_critical_damage,
            "base_health_regeneration": self.base_health_regeneration,
            "base_mana_regeneration": self.base_mana_regeneration,
            "base_luck": self.base_luck,
            "base_dodge_chance": self.base_dodge_chance,
            "base_block_chance": self.base_block_chance,
            "base_accuracy": self.base_accuracy,
            "base_resistance": self.base_resistance
        }

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
