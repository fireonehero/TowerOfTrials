import random

boss_list = ["Minotaur", "Dragon", "Lich", "Ancient God", "Demon King", "Fallen Hero"]
enemy_list = ["GorgonZola", "Goblin", "Orc", "Troll", "Imp", "Banshee", "Skeleton", "Zombie"]

class Player:
    def __init__(self, username, player_class):
        self.username = username
        self.player_class = player_class
        self.quit_game = False
        self.exp = 0
        self.level = 1
        self.enemies_defeated = 0
        self.player_attack = 10
        self.player_health = 100
        self.player_max_health = 100
        self.enemy_base_attack = 5
        self.enemy_base_health = 50
        self.is_new_enemy = False
        self.inventory = {'Potion': 0}
        if player_class == "Warrior":
            self.player_health += 50
            self.player_max_health += 50
        elif player_class == "Mage":
            self.player_attack += 5
        elif player_class == "Rogue":
            self.inventory['Potion'] += 3
        self.enemy_name, self.enemy_attack, self.enemy_health = None, None, None

    def attack_move(self):
        self.enemy_health -= self.player_attack
        print(f"Enemy's health: {self.enemy_health}")
        if self.enemy_health <= 0:
            self.enemy_killed()

    def enemy_killed(self):
        exp_add = random.randrange(1, 20)
        print(f"The enemy has been killed, you got {exp_add} exp.")
        self.exp += exp_add
        self.enemies_defeated += 1
        self.level_up()
        if not self.quit_game:
            self.spawn_enemy()

    def spawn_enemy(self):
        self.is_new_enemy = True
        if self.enemies_defeated % 10 == 0 and self.enemies_defeated != 0:
            self.enemy_name = random.choice(boss_list)
            self.enemy_attack = 15
            self.enemy_health = 100
            print(f"{self.username} is now fighting a boss: {self.enemy_name}!")
            self.enemy_base_attack += 2
            self.enemy_base_health += 10
            print("The enemies have gotten slightly stronger!")
            self.add_potion()
        else:
            self.enemy_name = random.choice(enemy_list)
            self.enemy_attack = self.enemy_base_attack
            self.enemy_health = self.enemy_base_health
        print(f"A {self.enemy_name} has appeared!")

    def level_up(self):
        if self.exp >= 100:
            self.exp = 0
            self.level += 1
            print(f"Congratulations! You've reached level {self.level}.")
            self.player_health = self.player_max_health
            self.improve_stats()

    def enemy_attack_move(self):
        self.player_health -= self.enemy_attack
        print(f"You've been attacked! Your health: {self.player_health}")
        if self.player_health <= 0:
            self.player_death()

    def show_stats(self):
        print(f"\nPlayer stats:\nLevel: {self.level}\nExp: {self.exp}\nHealth: {self.player_health}\n")

    def use_shield(self):
        self.player_health += 15
        if self.player_health > self.player_max_health:
            self.player_health = self.player_max_health
        print(f"You used your shield! Your health: {self.player_health}")

    def improve_stats(self):
        print("""
        Choose a stat to improve:
        1: Attack
        2: Max Health
        """)
        choice = self.player_choice()
        if choice == 1:
            self.player_attack += 5
            print(f"Your attack power is now {self.player_attack}.")
        elif choice == 2:
            self.player_max_health += 20
            print(f"Your maximum health is now {self.player_max_health}.")

    def use_potion(self):
        if self.inventory["Potion"] > 0:
            self.inventory["Potion"] -= 1
            print(f"You used a potion! You now have {self.inventory['Potion']} potions.")
            self.player_attack += 5
            self.player_health += 20
        else:
            print("You don't have any potions left.")

    def add_potion(self):
        self.inventory["Potion"] += 1
        print(f"The enemy dropped a potion! You now have {self.inventory['Potion']} potions.")

    def player_death(self):
        print("You have died. Game Over.")
        self.quit_game = True

    def display_inventory(self):
        print("Your Inventory:")
        for item, quantity in self.inventory.items():
            print(f"{item}: {quantity}")

    def player_choice(self):
        while True:
            try:
                return int(input())
            except ValueError:
                print("Invalid selection. Please try again.")


def choose_class():
    print("""
    Choose a class:
    1: Mage - increased attack
    2: Warrior - increased health
    3: Rogue - more potions
    """)
    class_choice = int(input("Your choice: "))
    if class_choice == 1:
        return "Mage"
    elif class_choice == 2:
        return "Warrior"
    elif class_choice == 3:
        return "Rogue"
    else:
        print("Invalid choice. Please choose a valid class.")
        return choose_class()

def start_game():
    username = input("What is your username for this run: ")
    player_class = choose_class()
    player = Player(username, player_class)
    story(player)
    player.spawn_enemy()

    while not player.quit_game:
        show_menu()
        user_choice = input("What is your selection: ")
        try:
            user_choice = int(user_choice)
            if user_choice == 1:
                player.is_new_enemy = False
                player.attack_move()
            elif user_choice == 2:
                player.is_new_enemy = False
                player.use_shield()
            elif user_choice == 3:
                player.show_stats()
            elif user_choice == 4:
                player.use_potion()
            elif user_choice == 5:
                player.display_inventory()
            elif user_choice == 6:
                print("Thank you for playing Tower of Trial!")
                player.quit_game = True
            else:
                print("Invalid selection, please try again.")
            if player.enemy_health > 0 and not player.quit_game and not player.is_new_enemy:
                player.enemy_attack_move()
        except ValueError:
            print("Invalid selection, please input a number.")


def story(player):
    print(f"""
{player.username}, a brave {player.player_class} is on a quest to defeat the legendary creatures that inhabit the Tower of Trials. 
Every 10th enemy in the tower is a powerful boss, but don't fear! With each enemy defeated, you gain experience and can choose to increase your attack or maximum health.
You also have a shield that can be used to restore health, and potions that can boost your abilities. Good luck!
    """)


def show_menu():
    print("""
    What will you do:
    1: Attack
    2: Use Shield
    3: Show Stats
    4: Use Potion
    5: Show Inventory
    6: Quit Game
    """)

start_game()
