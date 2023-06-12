import time
import math
import random
from entity import Enemy, Player

boss_list = ["Minotaur", "Dragon", "Lich", "Ancient God", "Demon King", "Fallen Hero"]
enemy_list = ["GorgonZola", "Goblin", "Orc", "Troll", "Imp", "Banshee", "Skeleton", "Zombie"]
modifier_list = ["Desecration", "Annihilation", "Doom", "Certain Doom", "Sensei Trent's Sending", "Descension", "Death", "True Evil", "Chaos Incarnate", "Unchecked Power", "Unlimited Corruption"]

# Boss List is for Possible Bosses in the Game
# Enemy List is for Possible Enemies in the Game
# Modifier List is for Bosses. When they spawn, they get a special name such as: The Dragon of Descension or The Ancient God of Chaos Incarnate



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
            attack = 10 + random.randint(level * 3, level * 5)
            health = 200 + random.randint(level * 25, level * 35)
            
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
                    self.player.gain_experience(20 + math.pow(self.player.get_level() - 1, 1.2)) # Not sure if this is fair or not yet...
                else:
                    self.player.add_potion()
                    self.player.gain_experience(60 + math.pow(self.player.get_level() + 1, 1.5)) # Ditto to the last comment
        
        print(f"The Tower of Trials bids player {self.player.get_name()} adieu..") # Subject to change, I quite like this line


if __name__ == "__main__":
    gm = GameManager()
    gm.start_game()