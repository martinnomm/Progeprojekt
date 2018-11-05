from time import *
from Dices import *

#Sets the base Character class with only health
class Character:

    def __init__(self,health):
        self.health = health

#Sets the Player class based on Character, designating the correct health. Also defines the attack
class Player(Character):

    def __init__(self,health=12):
        self.chosen_weapon = None
        self.current_area = Start_Area
        super().__init__(health)

    evasion = 12
    strength = D8()
    def attack(self, target, hit_chance):
        #print("To attack press ENTER, type to not attack")
        #answer = input("")
        #if answer == "":
        if hit_chance >= target.evasion:
            print("You swing at the {0.name}".format(target))
            print("Hit chance is {}.".format(hit_chance))
            sleep(0.1)
            print("Your attack hits the {0.name}".format(target))
            target.health -= randint(self.chosen_weapon.damage_roll[0],self.chosen_weapon.damage_roll[1])
            if "bleed" in self.chosen_weapon.attributes:
                target.status_effects.append("bleeding")
            if "stun" in self.chosen_weapon.attributes:
                target.status_effects.append("stunned")
            if "poison" in self.chosen_weapon.attributes:
                target.status_effects.append("poisoned")

        else:
            print("You miss your attack")

        #else:
        #    print("You don't do a thing")
        #sleep(0.1)

#
#
#Template weapons as a test
class Weapon:
    def __init__(self,damage_roll,attributes):
        self.damage_roll = damage_roll
        self.attributes = attributes

class Stiletto(Weapon):
    def __init__(self, damage_roll=[1,6],attributes=["bleed"]):
        super().__init__(damage_roll,attributes)

class Mace(Weapon):
    def __init__(self,damage_roll=[1,6],attributes=["stun"]):
        super().__init__(damage_roll,attributes)

class Scythe(Weapon):
    def __init__(self,damage_roll=[1,8],attributes=["poison"]):
        super().__init__(damage_roll,attributes)
    
    
    
#Sets the Enemy class based on Character, designating name, strenth(dam),defense,health. Also defines the attack
class Enemy(Character):
    def __init__(self, name, strength, evasion, health, status_effects):
        super().__init__(health)
        self.status_effects = status_effects
        self.name = name
        self.strength = strength
        self.evasion = evasion
        
    def attack(self,target):
        target.health -= self.strength
        
class Goblin(Enemy):
    def __init__(self, name = "goblin", strength = D6(), evasion = 8, health = 11, status_effects = []):
        super().__init__(name,strength,evasion,health,status_effects)

    def attack(self,target):
        target.health -= D6()


def battle(player,enemy):
    print("An enemy {0.name} appears with a defense of {0.evasion}".format(enemy))
    #Combat loop
    while player.health > 0 and enemy.health > 0:
        player_hit_chance = D20()
        action = input("Do you want to attack, flee or do nothing? (attack,flee,ENTER)")
        if action.lower() == "attack":
            player.attack(enemy,player_hit_chance)
        elif action.lower() == "flee":
            if D20() > 10:
                print("You flee the fight")
                break
            else:
                print("Failed to flee")
        elif action == "":
            print("You do nothing")
        else:
            print("Not understood, doing nothing")

        print("The health of the {0.name} is now {0.health}.".format(enemy))
        if enemy.health <= 0:
            break
        enemy_hit_chance = D20()
        if "stunned" in enemy.status_effects:
            print("The {0.name} is stunned.".format(enemy))
            enemy.status_effects.remove("stunned")
        else:
            if enemy_hit_chance >= player.evasion:
                print("The {0.name} attacks you".format(enemy))
                enemy.attack(player)
            else:
                print("The {0.name} misses their attack.".format(enemy))
        if "poisoned" in enemy.status_effects:
            print("The {0.name} takes damage from poison".format(enemy))
            enemy.health -= D4()
            enemy.status_effects.remove("poisoned")
        if "bleeding" in enemy.status_effects:
            print("The {0.name} takes damage from bleeding".format(enemy))
            enemy.health -= D4()
            enemy.status_effects.remove("bleeding")
            print(enemy.health)
        if player.health <= 0:
            break
        else:
            print("Your health is now {0.health}.".format(player))
        sleep(0.1)

    #Display outcome
    if enemy.health <= 0:
        print("You killed the {0.name}.".format(enemy))
    elif player.health <= 0:
        print("The {0.name} killed you.".format(enemy))

def new_battle(player,enemy):
    print("An enemy {0.name} appears".format(enemy))
    while player.health and enemy.health > 0:
        player_hit_chance = D20()
        print("attack or flee or defend")
        action = input()
        if action == "attack":
            sleep(1)
            player_defense = 0
            player.attack(enemy, player_hit_chance)
        elif action == "flee":
            player_defense = 0
            sleep(1)
            if D20() > 10:
                print("You flee the fight")
                break
            else:
                print("Failed to flee")
        elif action == "defend":
            player_defense = D4()
        else:
            print("Not understood, doing nothing")

        if enemy.health <= 0:
            break
        enemy_hit_chance = D20()
        if enemy_hit_chance >= player.evasion:
            print("The {0.name} attacks you".format(enemy))


############## Dungeon Area ###################

def Game_end():
    print("GAME OVER")

def Go_Start():
    player.current_area = Start_Area
    if "start" not in visited_areas:
        visited_areas.append("Start_Area")
        print("You come upon a door leading to the Dungeon")
        sleep(0.5)
        print("Do you enter the door or leave? y/n")
        vastus = input()
        while vastus not in ["y","n"]:
            print("Not understood, re-enter your answer")
            vastus = input()
        if vastus == "y":
            Go_Room1()
        if vastus == "n":
            print("You decide that the Dungeon is too much of a task to handle.")
            print("Not everyone is meant to be an adventurer.")
            Game_End()


def Go_Room1():
    pass

def Go_Room1W():
    pass

def Go_Room1E():
    pass

def Go_Start_Area():
    pass

def Go_Room2E():
    pass

def Go_Room1N():
    pass

def Go_Room2N():
    pass

def Go_RoomBoss():
    pass


class Area:
    def __init__(self,North,East,South,West):
        self.North = North
        self.East = East
        self.South = South
        self.West = West

class Start_Area(Area):
    def __init__(self,North=Go_Room1(),East=None,South=None,West=None):
        super.__init__(North,East,South,West)

class Room1_Area(Area):
    def __init__(self,North=Go_Room1N(),East=Go_Room1E(),South=Go_Start_Area(),West=Go_Room1W()):
        super.__init__(North,East,South,West)

class Room1W_Area(Area):
    def __init__(self,North=None,East=Go_Room1(),South=None,West=None):
        super.__init__(North,East,South,West)

class Room1E_Area(Area):
    def __init__(self,North=Go_Room2E(),East=None,South=None,West=Go_Room1()):
        super.__init__(North,East,South,West)

class Room1N_Area(Area):
    def __init__(self,North=Go_Room2N(),East=None,South=Go_Room1(),West=None):
        super.__init__(North,East,South,West)

class Room2N_Area(Area):
    def __init__(self,North=Go_RoomBoss(),East=None,South=Go_Room1N(),West=None):
        super.__init__(North,East,South,West)

class RoomBoss_Area(Area):
    def __init__(self,North=None,East=None,South=Go_Room2N(),West=None):
        super.__init__(North,East,South,West)



###############################################################