from random import *
from time import *
from Dices import *

#Sets the base Character class with only health
class Character:

    def __init__(self,health):
        self.health = health

#Sets the Player class based on Character, designating the correct health. Also defines the attack
class Player(Character):

    def __init__(self,health=12):
        super().__init__(health)

    defense = 12
    strength = D8()
    def attack(self, target, hit_chance):
        print("To attack press ENTER, type to not attack")
        answer = input("")
        if answer == "":
            if hit_chance >= target.defense:
                print("You swing at the {0.name}".format(target))
                print("Hit chance is {}.".format(hit_chance))
                sleep(0.1)
                print("Your attack hits the {0.name}".format(target))
                target.health -= self.strength
            else:
                print("You miss your attack")
        else:
            print("You don't do a thing")
        sleep(0.1)
    
    
    
#Sets the Enemy class based on Character, designating name, strenth(dam),defense,health. Also defines the attack
class Enemy(Character):
    def __init__(self, name, strength, defense, health):
        super().__init__(health)
        self.name = name
        self.strength = strength
        self.defense = defense
        
    def attack(self,target):
        target.health -= self.strength
        



def battle(player,enemy):
    print("An enemy {0.name} appears with a defense of {0.defense}".format(enemy))
    #Combat loop
    while player.health > 0 and enemy.health > 0:
        player_hit_chance = D20()
        player.attack(enemy, player_hit_chance)
        print("The health of the {0.name} is now {0.health}.".format(enemy))
        if enemy.health <= 0:
            break
        enemy_hit_chance = D20()
        if enemy_hit_chance >= player.defense:
            print("The {0.name} attacks you".format(enemy))
            enemy.attack(player)
        else:
            print("The {0.name} misses their attack.".format(enemy))
        if player.health <= 0:
            break
        else:
            print("Your health is now {0.health}.".format(player))
        sleep(0.1)

    #Display outcome
    if player.health > 0:
        print("You killed the {0.name}.".format(enemy))
    elif enemy.health > 0:
        print("The {0.name} killed you.".format(enemy))
