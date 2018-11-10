from time import *
from Dices import *
from Spells import *
#Sets the base Character class with only health


class Character:

    def __init__(self,health):
        self.health = health


visited_areas =[]

#Sets the Player class based on Character, designating the correct health. Also defines the attack


class Player(Character):

    def __init__(self, health=12,):

        self.chosen_weapon = None
        self.current_area = not_visited_areas["Start"]
        super().__init__(health)
        self.Game_Over = None
        self.Inventory = []
        self.mana = 100
        self.xp = 0
        self.chosen_spell = None
        self.status = []
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
            target.health -= randint(self.chosen_weapon.damage_roll[0], self.chosen_weapon.damage_roll[1])
            if "bleed" in self.chosen_weapon.attributes:
                target.status_effects.append("bleeding")
            if "stun" in self.chosen_weapon.attributes:
                target.status_effects.append("stunned")
            if "poison" in self.chosen_weapon.attributes:
                target.status_effects.append("poisoned")

    def spell_attack(self, target, hit_chance):

        if hit_chance >= target.evasion:
            print("You cast a spell on {0.name}".format(target))
            print("Hit chance is {}.".format(hit_chance))
            sleep(0.1)
            print("Your spell hits the {0.name}".format(target))
            target.health -= randint(self.chosen_spell().damg[0], self.chosen_spell().damg[1])
                #Siin viskab errori 'str' object has no attribute 'dmg'
            if 'burn' in self.chosen_spell.attribute:
                target.status_effects.append('burned')

            if 'paralyze' in self.chosen_spell.attribute:
                target.status_effects.append('paralyzed')

            if 'freeze' in self.chosen_spell.attribute:
                target.status_effects.append('frozen')


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
    def __init__(self, name, strength, evasion, health, status_effects, weakness):
        super().__init__(health)
        self.status_effects = status_effects
        self.name = name
        self.strength = strength
        self.evasion = evasion
        self.weakness = weakness

    def attack(self,target):
        target.health -= self.strength


class Goblin(Enemy):
    def __init__(self, name="goblin", strength=D6(), evasion=8, health=11, status_effects =[], weakness = 'fire'):
        super().__init__(name, strength, evasion, health, status_effects, weakness)

    def attack(self, target):
        target.health -= D6()


def battle(player,enemy):
    print("An enemy {0.name} appears with a defense of {0.evasion}".format(enemy))
    #Combat loop
    while player.health > 0 and enemy.health > 0:
        player_hit_chance = D20()
        action = input("Do you want to attack, flee, heal or do nothing? (attack,flee, heal, ENTER)")
        if action.lower() == "attack":
            action_2 = input("Do you want to use a spell or melee attack? (spell, melee)")
            if action_2.lower() == 'melee':
                player.attack(enemy, player_hit_chance)

            if action_2.lower() == 'spell':
                w_spell = input("Which spell would you like to use? (Fireball, Thunderbolt, Iceshard, Heal, Heal status)")
                player.chosen_spell = w_spell
                if player.mana >= 20:
                    if w_spell == 'Fireball':
                        player.spell_attack(enemy, player_hit_chance)
                        player.mana -= Fireball().mana_cost
                    elif w_spell == 'Thunderbolt':
                        player.spell_attack(enemy, player_hit_chance)
                        player.mana -= Thunderbolt().mana_cost
                    elif w_spell == 'Iceshard':
                        player.spell_attack(enemy, player_hit_chance)
                        player.mana -= Iceshard().mana_cost

                else:
                    print("You do not have enough mana!")
        elif action.lower() == 'heal':
            action2 = input("Heal or heal status?")
            if player.mana >= 25:
                if action2.lower() == 'heal':
                    player.mana -= Heal().mana_cost
                    player.health += Heal().heal
                    if player.health > 12:
                        player.health = 12
                elif action2.lower() == 'heal status':
                    player.status.clear()
                    print("All status effects have been removed.")
            else:
                print("You do not have enough mana")
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
        elif 'frozen' in enemy.status_effects:
            print("The {0.name} is frozen".format(enemy))
        elif 'paralyzed' in enemy.status_effects:
            print("The {0.name} is paralyzed".format(enemy))
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
        if 'burned' in enemy.status_effects:
            print("The {0.name} takes damage from burn".format(enemy))
            enemy.health -= D4()
            enemy.status_effects.remove('burned')
        if player.health <= 0:
            break
        else:
            print("Your health is now {0.health}.".format(player))
        sleep(0.1)

    #Display outcome
    if enemy.health <= 0:
        player.xp += 14
        player.mana = 100
        xp_needed = 100 - player.xp

        print("You killed the {0.name}.".format(enemy))
        print('You gained 14 xp,',xp_needed,'xp needed to gain a level')
    elif player.health <= 0:
        print("The {0.name} killed you.".format(enemy))

############## Dungeon Area ###################



class Area:
    def __init__(self, Directions, Actions):
        self.Directions = Directions
        self.Actions = Actions
    def show_actions(self):
        mingid_suunad = []
        for i in ["n","e","s","w"]:
            if self.Directions[i] is not None:
                mingid_suunad.append(i)
        for suund in mingid_suunad:
            print("You can move to: " + suund)
        if None not in player.current_area.Actions:
            for action in player.current_area.Actions:
                print("You can also: " + action)
        print("Leave = 'x'")
        vastus = input()
        choices = mingid_suunad[:]
        choices.extend("x")
        choices.append("weapon")
        choices.append("get_key")
        if None not in player.current_area.Actions:
            if "fight" in player.current_area.Actions:
                fight()
                if player.health > 0:
                    player.current_area.Actions.remove("fight")
        while vastus.lower() not in choices:
            print("Not understood")
            vastus = input()
        if  vastus.lower() == "n":
            if player.current_area == not_visited_areas["Room1"]:
                if player.chosen_weapon is None:
                    print("This way seems dangerous. You need a weapon to be safe.")
                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["n"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["n"]]
        if  vastus.lower() == "e":
            if player.current_area == not_visited_areas["Room1"]:
                if player.chosen_weapon is None:
                    print("This way seems dangerous. You need a weapon to be safe.")
                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["e"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["e"]]
        if  vastus.lower() == "s":
            if player.current_area == not_visited_areas["Room1"]:
                if "key" not in player.Inventory:
                    print("The door seems to have locked behind you. The key might be further ahead.")

                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["s"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["s"]]
        if  vastus.lower() == "w":
            player.current_area = not_visited_areas[player.current_area.Directions["w"]]
        if "Ayylmao" in player.current_area.Actions:
            print("Ayylmao")
        if "Game_Over_Leave" in player.current_area.Actions:
            if vastus.lower() == "x":
                player.Game_Over = "Leave"
        if "weapon" in player.current_area.Actions:
            if vastus.lower() == "weapon":
                choose_weapon()
        if "Get_Key" in player.current_area.Actions:
            if "key" not in player.Inventory:
                player.Inventory.append("key")

class Start_Area(Area):
    def __init__(self, Directions={"n": "Room1","e": None,"s": None,"w": None}, Actions=["Game_Over_Leave"]):
        super().__init__(Directions, Actions)




class Room1_Area(Area):
    def __init__(self,Directions={"n":"Room1N","e":"Room1E","s":"Start","w":"Room1W"},Actions=[None]):
        super().__init__(Directions,Actions)


class Room1W_Area(Area):
    def __init__(self, Directions = {"n":None, "e":"Room1", "s":None, "w":None}, Actions = ["weapon"]):
        super().__init__(Directions,Actions)


class Room1E_Area(Area):
    def __init__(self, Directions = {"n":"Room2E", "e":None, "s":None, "w":"Room1"}, Actions=[None]):
        super().__init__(Directions,Actions)

class Room2E_Area(Area):
    def __init__(self, Directions = {"n":None, "e":None, "s":"Room1E", "w":None}, Actions=[None]):
        super().__init__(Directions,Actions)


class Room1N_Area(Area):
    def __init__(self, Directions = {"n":"Room2N", "e":None, "s":"Room1", "w":None}, Actions = ["Ayylmao"]):
        super().__init__(Directions,Actions)


class Room2N_Area(Area):
    def __init__(self, Directions = {"n":"RoomBoss", "e":None, "s":"Room1N", "w":None}, Actions = [None]):
        super().__init__(Directions,Actions)


class RoomBoss_Area(Area):
    def __init__(self, Directions = {"n":None, "e":None, "s":"Room2N", "w":None}, Actions = ["Get_Key","fight"]):
        super().__init__(Directions,Actions)


###############################################################

visited_areas = []
not_visited_areas = {"Start": Start_Area(), "Room1": Room1_Area(), "Room1W": Room1W_Area(), "Room1E": Room1E_Area(),
                     "Room2E": Room2E_Area(), "Room1N": Room1N_Area(), "Room2N": Room2N_Area(), "RoomBoss": RoomBoss_Area()}

#for arv in not_visited_areas:
 #   suunad = []
  #  for i in range(4):
   #     if not_visited_areas[arv].Directions[i] != None:
    #        suunad.append(not_visited_areas[arv].Directions[i])
    #print(suunad)


playerlist = [Player()]
player = playerlist[0]


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
        new_answer = Mace()
    elif answer.lower() == "stiletto":
        new_answer = Stiletto()
    elif answer.lower() == "scythe":
        new_answer = Scythe()
    player.chosen_weapon = new_answer


def actual_game():
    pass





######## OLD STUFF


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
            if player.chosen_weapon != None:
                Go_Room1N()
            else:
                print("Need weapon fist")
        if vastus.lower() in ["e","east"]:
            if player.chosen_weapon != None:
                Go_Room1E()
            else:
                print("Need weapon first")
        if vastus.lower() in ["w","west"]:
            Go_Room1W()
        if vastus.lower() in ["s","south"]:
            if "RoomBoss_Area" in visited_areas:
                Go_Start_Area()
            else:
                print("Door locked")

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

###############
            

