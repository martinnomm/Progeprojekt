from time import *
from Dices import *

#Sets the base Character class with only health
class Character:

    def __init__(self,health):
        self.health = health
visited_areas =[]

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

def Go_Start_Area():
    Player.current_area = "Start_Area"
    if "Start_Area" not in visited_areas or "Start_Area" in visited_areas:
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
            Game_end()




def Go_Room1():
    Player.current_area = "Room1_Area"
    if "Room1_Area" not in visited_areas or "Room1_Area" in visited_areas:
        visited_areas.append("Room1_Area")
        print("You enter Room1")
        print("You can go North, East, South, West")
        vastus = input()
        while vastus.lower() not in ["n","e","s","w","west","north","east","south"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["n","north"]:
            Go_Room1N()
        if vastus.lower() in ["e","east"]:
            Go_Room1E()
        if vastus.lower() in ["w","west"]:
            Go_Room1W()
        if vastus.lower() in ["s","south"]:
            Go_Start_Area()

def Go_Room1W():
    Player.current_area = "Room1W_Area"
    if "Room1W" not in visited_areas or "Room1W" in visited_areas:
        visited_areas.append("Room1W_Area")
        print("You enter Room1W")
        print("You find a stash of weapons.")
        choose_weapon()
        print("You can go East")
        vastus = input()
        while vastus.lower() not in ["e","east"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["e","east"]:
            Go_Room1()

def Go_Room1E():
    Player.current_area = "Room1E_Area"
    if True:
        visited_areas.append("Room1E_Area")
        print("You enter Room1E")
        print("You can go North, West")
        vastus = input()
        while vastus.lower() not in ["w","west","n","north"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["n","north"]:
            Go_Room2E()
        if vastus.lower() in ["w","west"]:
            Go_Room1()

def Go_Room2E():
    Player.current_area = "Room2E_Area"
    if True:
        visited_areas.append("Room2E_Area")
        print("You enter Room2E")
        print("You can go South")
        vastus = input()
        while vastus.lower() not in ["s","south"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["s","south"]:
            Go_Room1E()

def Go_Room1N():
    Player.current_area = "Room1N_Area"
    if True:
        visited_areas.append("Room1N_Area")
        print("You enter Room1N")
        print("You can go North, South")
        vastus = input()
        while vastus.lower() not in ["s", "south", "n", "north"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["n", "north"]:
            Go_Room2N()
        if vastus.lower() in ["s", "south"]:
            Go_Room1()

def Go_Room2N():
    Player.current_area = "Room2N_Area"
    if True:
        visited_areas.append("Room2N_Area")
        print("You enter Room2N")
        print("You can go North, South")
        vastus = input()
        while vastus.lower() not in ["s", "south", "n", "north"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["n", "north"]:
            Go_RoomBoss()
        if vastus.lower() in ["s", "south"]:
            Go_Room1N()

def Go_RoomBoss():
    Player.current_area = "RoomBoss_Area"
    if True:
        visited_areas.append("RoomBoss_Area")
        print("You enter RoomBoss")
        print("You can go South")
        vastus = input()
        while vastus.lower() not in ["s","south"]:
            print("Not understood, repeat")
            vastus = input()
        if vastus.lower() in ["s", "south"]:
            Go_Room2N()




class Area:
    def __init__(self,Directions,Actions):
        self.Directions = Directions
        self.Actions = Actions

class Start_Area(Area):
    def __init__(self,Directions=["Room1",None,None,None],Actions=None):
        super().__init__(Directions,Actions)

class Room1_Area(Area):
    def __init__(self,Directions=["Room1N","Room1E","Start","Room1W"],Actions=None):
        super().__init__(Directions,Actions)

class Room1W_Area(Area):
    def __init__(self,Directions=[None,"Room1",None,None],Actions=None):
        super().__init__(Directions,Actions)

class Room1E_Area(Area):
    def __init__(self,Directions=["Room2E",None,None,"Room1"],Actions=None):
        super().__init__(Directions,Actions)

class Room1N_Area(Area):
    def __init__(self,Directions=["Room2N",None,"Room1",None],Actions=None):
        super().__init__(Directions,Actions)

class Room2N_Area(Area):
    def __init__(self,Directions=["RoomBoss",None,"Room1N",None],Actions=None):
        super().__init__(Directions,Actions)

class RoomBoss_Area(Area):
    def __init__(self,Directions=[None,None,"Room2N",None],Actions=None):
        super().__init__(Directions,Actions)


###############################################################

playerlist = [Player()]
player = playerlist[0]
visited_areas = []
not_visited_areas = [Start_Area(),Room1_Area(),Room1W_Area(),Room1E_Area(),Room1N_Area(),Room2N_Area(),RoomBoss_Area()]
def fight():
    battle(player, Goblin())



#enemies = [Enemy("Goblin", D4(), 8, 11)]


def choose_weapon():
    print("Choose weapon: stiletto or mace or scythe")
    answer = input()
    while answer.lower() not in ["mace","stiletto","scythe"]:
        print("Not understood")
        print("Choose weapon: stiletto or mace or scythe")
        answer = input()
    if answer.lower() == "mace":
        newanswer = Mace()
    elif answer.lower() == "stiletto":
        newanswer = Stiletto()
    elif answer.lower() == "scythe":
        newanswer = Scythe()

    player.chosen_weapon = newanswer


def Actual_Game():
    pass


for arv in not_visited_areas:
    suunad = []
    for i in range(4):
        if arv.Directions[i] != None:
            suunad.append(arv.Directions[i])
    print(suunad)