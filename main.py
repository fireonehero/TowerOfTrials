import time
import random

boss_list = ["Minotaur", "Dragon", "Lich", "Ancient God", "Demon King", "Fallen Hero"]
enemy_list = ["GorgonZola", "Goblin", "Orc", "Troll", "Imp", "Banshee", "Skeleton", "Zombie"]
modifier_list = ["Desecration", "Annihilation", "Doom", "Certain Doom", "Sensei Trent's Sending", "Descension", "Death", "True Evil", "Chaos Incarnate", "Unchecked Power", "Unlimited Corruption"]

# Boss List is for Possible Bosses in the Game
# Enemy List is for Possible Enemies in the Game
# Modifier List is for Bosses. When they spawn, they get a special name such as: The Dragon of Descension or The Ancient God of Chaos Incarnate


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
            self.player.attack += 3
            print(f"Your attack power is now {self.player.attack}.")
        elif player_choice == 2:
            self.player.max_health += 20
            print(f"Your maximum health is now {self.player.max_health}.")
    
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


class GameManager:
    
    def __init__(self) -> None:
        self.current_enemy = None
        self.quit_game = False
        self.enemies_defeated = 0
        
        player_name = input("What would you like to name your brave adventurer? ")
        
        classes = {
            "Mage": "Increased Attack + Unique Magic Stat / Abilities",
            "Warrior": "Increased Health + Damage Resistance | Slowed Movement",
            "Rogue": "Increased Drop Rates and Starter Potions + Speed"
        }
        
        # Unique Magic Stat, Abilities, Speed Augmentation of any kind, and Drop Rates have not been altered yet.
        
        print("\n".join([f"[{str(i+1)}] {x} - {classes[x]}" for i, x in enumerate(classes)]))
        class_choice = input("Your choice: ")
        while not (class_choice.isdigit() and int(class_choice) in [1, 2, 3]):
            class_choice = input("Your choice: ")
        
        self.player = Player(player_name, list(classes.keys())[int(class_choice)-1])
    
    def spawn_enemy(self):
        
        # ALL VALUES HERE ARE SUBJECT TO CHANGE
        # I just threw these together. They might scale horribly...
        # The idea is to create a sense of growth in opposition that should evenly match the player's skill.
        # I wanted them to have higher attack on average and lower health
        # Bosses should ideally have both
        
        if self.enemies_defeated % 10 != 0:
            boss = False
            name = random.choice(enemy_list)
            level = self.player.get_level() - 1
            attack = 5 + random.randint(level * 3 / 2, level * 8 / 3)
            health = 50 + random.randint(level * 8, level * 12)
        else:
            boss = True
            name = f"{random.choice(boss_list)} of {random.choice(modifier_list)}"
            level = self.player.get_level() + 1
            attack = random.randint(level * 3, level * 5)
            health = 150 + random.randint(level * 12, level * 16)
            
        self.current_enemy = Enemy(name, level, attack, health, boss)
        article = "The" if self.current_enemy.is_boss() else "A"
        print(f"{article} {self.current_enemy.get_name()} [{self.current_enemy.get_health()}] has appeared!")

    def player_death(self):
        print("You have died. Game Over.")
        self.quit_game = True
    
    def player_turn(self)->bool:
        
        time.sleep(2)
        
        options = ["Attack", "Use Shield", "Show Stats", "Use Potion", "Show Inventory", "Quit Game"]
        
        # code for checking states in game, see player_states
        
        print("What will you do?")
        print("\n".join([f"[{i+1}] {x}" for i, x in enumerate(options)]) + "\n")
        player_input = input("Your Choice: ")
        while not (player_input.isdigit() and int(player_input) in range(1, 7)):
            player_input = input("Your Choice: ")
        
        player_input = int(player_input)
        
        if player_input == 1:
            player_killed_enemy = self.player.attack_move(self.current_enemy)
            if player_killed_enemy:
                self.current_enemy = None
        elif player_input == 2:
            self.player.use_shield()
        elif player_input == 3:
            print(self.player.get_stats())
            return self.player_turn()
        elif player_input == 4:
            self.player.use_potion()
        elif player_input == 5:
            self.player.display_inventory()
            return self.player_turn()
        else:
            self.quit_game = True
        
    def start_game(self):
        print(f"""
{self.player.get_name()}, a brave {self.player.player_class} is on a quest to defeat the legendary creatures that inhabit the Tower of Trials. 
Every 10th enemy in the tower is a powerful boss, but do not fear, brave adventurer! With each enemy defeated, you gain experience and can choose to increase your attack or maximum health.
You also have a Holy Shield that can be used to restore health and reduce the impact of incoming damage, as well as potions that can boost your abilities. Good luck to you, mighty {self.player.player_class}!
        """)
        self.gameplay_loop()
        
    def gameplay_loop(self):
        while not self.quit_game:
            self.player.reset_shield()
            
            if self.current_enemy is None:
                self.enemies_defeated += 1 # this is meant to start the counter at 1 to avoid a boss fight in the beginning because 0 % 10 == 0 is True
                self.spawn_enemy()
            
            boss = self.current_enemy.is_boss() # checking for boss for additional exp once it no longer exists
            print(f"\nYou: {self.player.get_health()}")
            print(f"{self.current_enemy.get_name()}: {self.current_enemy.get_health()}")
            self.player_turn()
            
            if self.current_enemy is not None:
                player_died = self.current_enemy.attack_move(self.player) # I hope not!
                if player_died:
                    self.quit_game = True
            else:
                if not boss:
                    self.player.gain_experience(10 + (self.player.get_level() - 1) * 1.2) # Not sure if this is fair or not yet...
                else:
                    self.player.add_potion()
                    self.player.gain_experience(20 + (self.player.get_level() + 1) * 1.5) # Ditto to the last comment
        
        print(f"The Tower of Trials bids player {self.player.get_name()} adieu..") # Subject to change, I quite like this line


if __name__ == "__main__":
    gm = GameManager()
    gm.start_game()
    
