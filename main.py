import random

import random

def start_game():
    global quit_game, exp, level, enemies_defeated, player_attack, player_health, player_max_health, enemy_base_attack, enemy_base_health, is_new_enemy

    quit_game = False
    exp = 0
    level = 1
    enemies_defeated = 0
    player_attack = 10
    player_health = 100
    player_max_health = 100
    enemy_base_attack = 5
    enemy_base_health = 50
    is_new_enemy = True

    spawn_enemy()

    while quit_game == False:
        print(user_menu)
        user_choice = int(input("What is your selection: "))
        if user_choice == 1:
            attack_move(player_attack)
            is_new_enemy = False
            if enemy_health > 0 and quit_game == False and not is_new_enemy:
                enemy_attack_move()
        elif user_choice == 2:
            use_shield()
            is_new_enemy = False
            if enemy_health > 0 and quit_game == False and not is_new_enemy:
                enemy_attack_move()
        elif user_choice == 3:
            show_stats()
        elif user_choice == 4:
            print("Thank you for playing Tower of Trial!")
            quit_game = True

    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() == 'yes':
        start_game()
        
enemy_list = ["GorgonZola", "Vampire", "Chimera", "Hydra", "Zombie", "Banshee", "Bogeyman"]
boss_list = ["Dragon", "Lich King", "Demon Lord", "Ancient God"]

user_menu = ("""
######################################
1 : Attack\t\t2 : Shield
3 : Stats\t\t4 : Quit
######################################
""")

def attack_move(attack):
    global enemy_health
    enemy_health -= attack
    print(f"Enemy's health: {enemy_health}")
    if enemy_health <= 0:
        enemy_killed()
        spawn_enemy()

def enemy_killed():
    exp_add = random.randrange(1, 20)
    print(f"The enemy has been killed, you got {exp_add} exp.")
    global exp, enemies_defeated
    exp += exp_add
    enemies_defeated += 1
    level_up()

def spawn_enemy():
    global enemy_name, enemy_attack, enemy_health, is_new_enemy
    is_new_enemy = True
    if enemies_defeated % 10 == 0 and enemies_defeated != 0:
        enemy_name = random.choice(boss_list)
        enemy_attack = 15
        enemy_health = 100
        print(f"{username} is now fighting a boss: {enemy_name}!")
        global enemy_base_attack, enemy_base_health
        enemy_base_attack += 2
        enemy_base_health += 10
        print("The enemies have gotten slightly stronger!")
    else:
        enemy_name = random.choice(enemy_list)
        enemy_attack = enemy_base_attack
        enemy_health = enemy_base_health
    print(f"A {enemy_name} has appeared!")

def level_up():
    global exp, level, player_health, player_max_health
    if exp >= 100:
        exp = 0
        level += 1
        print(f"Congratulations! You've reached level {level}.")
        player_health = player_max_health
        improve_stats()

def player_death():
    print("You died!")
    global quit_game
    quit_game = True

def enemy_attack_move():
    global player_health
    player_health -= enemy_attack
    print(f"You've been attacked! Your health: {player_health}")
    if player_health <= 0:
        player_death()

def show_stats():
    print(f"\nPlayer stats:\nLevel: {level}\nExp: {exp}\nHealth: {player_health}\n")

def use_shield():
    global player_health
    player_health += 15
    if player_health > player_max_health:
        player_health = player_max_health
    print(f"You used your shield! Your health: {player_health}")

def improve_stats():
    print("""
    Choose a stat to improve:
    1: Attack
    2: Max Health
    """)
    choice = int(input("Your choice: "))
    global player_attack, player_max_health
    if choice == 1:
        player_attack += 5
        print(f"Your attack power is now {player_attack}.")
    elif choice == 2:
        player_max_health += 20
        print(f"Your maximum health is now {player_max_health}.")

username = input("What is your username for this run: ")
start_game()
