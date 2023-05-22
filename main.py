import random

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
        self.potions = 3
        self.is_new_enemy = False
        self.enemy_base_attack = 5
        self.enemy_base_health = 50
        self.enemy_list = ["GorgonZola", "Vampire", "Chimera", "Hydra", "Zombie", "Banshee", "Bogeyman"]
        self.boss_list = ["Dragon", "Lich King", "Demon Lord", "Ancient God"]
        self.class_benefits()

    def class_benefits(self):
        if self.player_class == "Mage":
            self.player_attack += 5
        elif self.player_class == "Warrior":
            self.player_max_health += 50
            self.player_health += 50
        elif self.player_class == "Rogue":
            self.potions += 2

    def show_menu(self):
        print("""
        ######################################
        1 : Attack\t\t2 : Shield
        3 : Stats\t\t4 : Use Potion
        5 : Quit
        ######################################
        """)

    def story(self):
        print(f"\n{self.username}, a brave {self.player_class} is on a quest to defeat the legendary creatures that inhabit the Tower of Trials. "
            "\nEvery 10th enemy in the tower is a powerful boss, but don't fear! With each enemy defeated, you gain experience and can choose to increase your attack or maximum health."
            "\nYou also have a shield that can be used to restore health, and potions that can boost your abilities. Good luck!\n")

    def attack_move(self):
        self.enemy_health -= self.player_attack
        print(f"Enemy's health: {self.enemy_health}")
        if self.enemy_health <= 0:
            self.enemy_killed()
            self.spawn_enemy()

    def enemy_killed(self):
        exp_add = random.randrange(1, 20)
        print(f"The enemy has been killed, you got {exp_add} exp.")
        self.exp += exp_add
        self.enemies_defeated += 1
        self.level_up()

    def spawn_enemy(self):
        self.is_new_enemy = True
        if self.enemies_defeated % 10 == 0 and self.enemies_defeated != 0:
            self.enemy_name = random.choice(self.boss_list)
            self.enemy_attack = 15
            self.enemy_health = 100
            print(f"{self.username} is now fighting a boss: {self.enemy_name}!")
            self.enemy_base_attack += 2
            self.enemy_base_health += 10
            print("The enemies have gotten slightly stronger!")
        else:
            self.enemy_name = random.choice(self.enemy_list)
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

    def player_death(self):
        print("You died!")
        self.quit_game = True

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
        choice = int(input("Your choice: "))
        if choice == 1:
            self.player_attack += 5
            print(f"Your attack power is now {self.player_attack}.")
        elif choice == 2:
            self.player_max_health += 20
            print(f"Your maximum health is now {self.player_max_health}.")

    def use_potion(self):
        if self.potions > 0:
            self.player_attack += 5
            self.player_max_health += 10
            self.player_health = min(self.player_health + 20, self.player_max_health)
            self.potions -= 1
            print("You used a potion! Your attack and health have been increased!")
            print(f"Attack: {self.player_attack}\nHealth: {self.player_health}\n")
        else:
            print("You don't have any potions left.")

def choose_class():
    print("""
    Choose a class:
    1: Mage - increased attack
    2: Warrior - increased health
    3: Rogue - more potions
    """)
    class_choice = int(input("Your choice: "))
    if class_choice == 1:
        player_class = "Mage"
    elif class_choice == 2:
        player_class = "Warrior"
    elif class_choice == 3:
        player_class = "Rogue"
    else:
        print("Invalid choice. Please choose a valid class.")
        choose_class()
    return player_class

def start_game():
    global player
    player = Player(username, choose_class())
    player.story()
    player.spawn_enemy()
    while not player.quit_game:
        player.show_menu()
        user_choice = int(input("What is your selection: "))
        if user_choice == 1:
            player.is_new_enemy = False
            player.attack_move()
            if player.enemy_health > 0 and not player.quit_game and not player.is_new_enemy:
                player.enemy_attack_move()
        elif user_choice == 2:
            player.is_new_enemy = False
            player.use_shield()
            if player.enemy_health > 0 and not player.quit_game and not player.is_new_enemy:
                player.enemy_attack_move()
        elif user_choice == 3:
            player.show_stats()
        elif user_choice == 4:
            player.use_potion()
        elif user_choice == 5:
            print("Thank you for playing Tower of Trials!")
            player.quit_game = True
        else:
            print("Invalid selection! Please choose a number from 1 to 5.")
    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() == 'yes':
        start_game()
    else:
        print("Goodbye!")


username = input("What is your username for this run: ")
start_game()