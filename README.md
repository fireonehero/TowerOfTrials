#Tower of Trials

Tower of Trials is a text-based RPG game written in Python, where the player's character must battle a series of enemies and bosses in order to progress through the Tower of Trials. The game emphasizes strategic decision-making, with each player action influencing the course of the battle.
Gameplay

In Tower of Trials, the player is presented with various classes to choose from, each with their unique traits. Players are given the option to enhance their attack power or health after each enemy defeated. The game offers a Holy Shield that can be used to restore health and reduce incoming damage and potions that boost abilities.

Every 10th enemy the player encounters is a powerful boss. The enemies' attack power and health scale according to the player's level, creating a balanced challenge throughout the game.
Game Mechanics

    Entity: The base class for any character in the game, including the player and enemies. It contains attributes such as health, level, attack power, and critical hit chance, and methods to calculate attacks and receive damage.

    Player: A subclass of Entity, with additional attributes like inventory, and unique methods such as using a shield, adding a potion, and using a potion.

    GameManager: This class manages the game loop and the interaction between the player and enemies. It handles the spawning of enemies, player death, player actions during their turn, and the overall game loop.

Enemy & Boss Mechanics

The game features a list of possible enemies and bosses that the player can encounter. Each enemy and boss has a name, level, attack power, and health points. The bosses also have unique modifier names. The attributes of enemies and bosses scale according to the player's level, ensuring a balanced challenge.
Getting Started

To start playing, simply clone the repository and run the main Python file in your terminal:

bash

git clone https://github.com/fireonehero/TowerOfTrials
cd TowerOfTrials
python main.py

Future Work

Future updates will look into adding unique magic stats, abilities, speed augmentation, and drop rates for different classes.
