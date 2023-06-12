import random

class Entity:
    def __init__(self, name, level, attack, health:float) -> None:
        self.name = name
        self.level = level
        self.attack = attack
        self.weapon = None
        self.max_health = health
        self.health = self.max_health
        self.max_mana = -1
        self.mana = -1
        self.damage_resistance = 0
        self.crit_chance = .05
        self.crit_damage = .8
        self.dead = False
        
    
    def attack_move(self, target)->bool:
        if random.random() > .05:
            attack = self.calculate_attack()
            received_damage = target.receive_damage(attack)
            print(f"{self.name} has attacked {target.get_name()} for {received_damage} damage!")
            return target.is_dead()
        else:
            print(f"{self.name} Missed!")
            return False
    
    def reset_health(self):
        self.health = self.max_health
    
    def calculate_attack(self):
        if random.random() <= self.crit_chance:
            return self.attack + self.crit_damage * self.attack
        return self.attack
    
    def receive_damage(self, damage):
        self.health -= (1-self.damage_resistance/100.0) * damage
        self.health = round(self.health, 3)
        self.dead = self.health <= 0
        return damage
    
    def get_name(self):
        return self.name
    
    def get_level(self):
        return self.level
    
    def is_dead(self):
        return self.dead
    
    def get_health(self):
        return f"{self.health} / {self.max_health}"
    

class Enemy(Entity):
    def __init__(self, name, level, attack, health, boss = False):
        super().__init__(name, level, attack, health)
        self.boss = boss
        
    def is_boss(self):
        return self.boss
        

class Player(Entity):
    def __init__(self, name, player_class):
        super().__init__(name, 1, 10, 100)
        self.player_class = player_class
        self.exp = 0
        self.exp_for_next_level = 100
        self.shield_in_use = False
        
        self.inventory = {"Potion": 0}
        
        if player_class == "Warrior":
            self.health += 50
            self.max_health += 50
            self.damage_resistance = 3
        elif player_class == "Mage":
            self.attack += 4
            self.max_mana = 30
            self.mana = 30
        elif player_class == "Rogue":
            self.inventory["Potion"] += 3
        
        self.stats = [["Attack", self.attack],
                      ["Max Health", self.max_health],
                      ["Damage Resistance", self.damage_resistance],
                      ["Critical Chance", self.crit_chance],
                      ["Critical Damage", self.crit_damage]]
    
    def gain_experience(self, exp):
        self.exp += exp
        if self.exp < self.exp_for_next_level:
            return
        self.exp -= self.exp_for_next_level
        self.exp_for_next_level *= 1.2
        self.level += 1
        print(f"Congratulations! You've reached level {self.level}!")
        self.use_shield() # This is an easy way to introduce leveling. Instead of healing the player fully, it provides them with a 30% health boost that is reset in gameloop
        self.improve_stats()
    
    def improve_stats(self):
        print("""
              Choose a stat to improve:
              1: Attack
              2: Max Health
        """)
        
        player_choice = input("Your Choice: ")
        while not (player_choice.isdigit() and int(player_choice.isdigit()) in [1, 2]):
            player_choice = input("Your Choice: ")
        player_choice = int(player_choice)
        
        if player_choice == 1:
            self.attack += 3
            print(f"Your attack power is now {self.attack}.")
        elif player_choice == 2:
            self.max_health += 20
            print(f"Your maximum health is now {self.max_health}.")
    
    def display_inventory(self):
        print("Your Inventory:")
        print("\n".join([f"{x} x"+str(self.inventory[x]) for x in self.inventory]))
    
    def receive_damage(self, damage):
        return super().receive_damage(damage / (2 if self.shield_in_use else 1))
    
    def use_shield(self):
        self.shield_in_use = True
        self.health += self.max_health * .3
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"You have been healed for {self.max_health * .3} Health!")
    
    def reset_shield(self):
        if self.shield_in_use:
            self.shield_in_use = False
    
    def add_potion(self):
        self.inventory["Potion"] += 1
        print(f"The enemy dropped a potion! You now have {self.inventory['Potion']} potions.")
    
    def use_potion(self):
        if self.inventory["Potion"] > 0:
            self.inventory["Potion"] -= 1
            print(f"You used a potion! You now have {self.inventory['Potion']} potions.")
            self.attack += 5
            self.player_health += 20
        else:
            print("You don't have any potions left.")
    
    def get_stats(self):
        return  f"{self.name} [{self.level}]:\n" + "\n".join([f"{x[0]} - {x[1]}" for x in self.stats])
    
    def get_stats_dict(self):
        return self.stats
    
    def is_mage(self):
        return self.max_mana > 0

