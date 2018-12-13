from builtins import bool
from sched import scheduler
from time import *
from Dices import *
from Spells import *
from tkinter import *


# Sets the base Character class with only health


class Character:

    def __init__(self,health):
        self.health = health

# Sets the Player class based on Character, designating the correct health. Also defines the attack


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
        self.spell_string = None
        self.status = []
    evasion = 12
    strength = D8()

    def attack(self, target, hit_chance):
        textbox.delete(1.0, END)
        if hit_chance >= target.evasion:
            textbox.insert(END, 'You swing at the {} and hit.'.format(target.name))
            target.health -= randint(self.chosen_weapon.damage_roll[0], self.chosen_weapon.damage_roll[1])
            if "bleed" in self.chosen_weapon.attributes:
                if D20() > 8:
                    target.status_effects.append("bleeding")
            if "stun" in self.chosen_weapon.attributes:
                if D20() > 8:
                    target.status_effects.append("stunned")
            if "poison" in self.chosen_weapon.attributes:
                if D20() > 9:
                    target.status_effects.append("poisoned")
        else:
            textbox.insert(END, 'You swing at the {} but miss your attack.'.format(target.name))

    def spell_attack(self, target, hit_chance):
        if hit_chance >= target.evasion:
            textbox.delete(1.0, END)
            attackboost = 1
            if 'burn' in self.chosen_spell.attribute:
                if 'fire' in target.weakness:
                    attackboost = 2

            if 'paralyze' in self.chosen_spell.attribute:
                if 'lightning' in target.weakness:
                    attackboost = 2

            if 'freeze' in self.chosen_spell.attribute:
                if 'ice' in target.weakness:
                    attackboost = 2
            if attackboost == 2:
                tegevus = textbox.insert(END, 'You cast {1} and it hits the {0.name}. The {0.name} is weak to {1}'.format(target, player.spell_string))
            else:
                tegevus = textbox.insert(END,'You cast {1} and it hits the {0.name}.'.format(target, player.spell_string))
            rw.after(200, tegevus)
            target.health -= randint(self.chosen_spell.damg[0], self.chosen_spell.damg[1])*attackboost

        else:
            textbox.delete(1.0, END)
            tegevus = textbox.insert(END, 'You miss your attack.')
            rw.after(200, tegevus)


class Weapon:
    def __init__(self, damage_roll, attributes):
        self.damage_roll = damage_roll
        self.attributes = attributes


class Stiletto(Weapon):
    def __init__(self, damage_roll=[1, 6], attributes=["bleed"]):
        super().__init__(damage_roll, attributes)


class Mace(Weapon):
    def __init__(self,damage_roll=[1, 6], attributes=["stun"]):
        super().__init__(damage_roll, attributes)


class Scythe(Weapon):
    def __init__(self,damage_roll=[1, 8], attributes=["poison"]):
        super().__init__(damage_roll, attributes)
    

# Sets the Enemy class based on Character, designating name, strenth(dam),defense,health. Also defines the attack

class Enemy(Character):
    def __init__(self, name, strength, evasion, health, status_effects, weakness):
        super().__init__(health)
        self.status_effects = status_effects
        self.name = name
        self.strength = strength
        self.evasion = evasion
        self.weakness = weakness

    def attack(self, target):
        target.health -= self.strength


class Goblin(Enemy):
    def __init__(self, name="goblin", strength=D6(), evasion=8, health=20, status_effects=[], weakness='fire'):
        super().__init__(name, strength, evasion, health, status_effects, weakness)
        self.max_health = 20

    def attack(self, target):
        target.health -= D6()



def melee():
    global playerpic, screen,enemypic
    playerpic = playerattack
    enemypic = goblinidle
    player_hit_chance = D20()
    player.attack(newenemy, player_hit_chance)
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>',fightcheck)
    #Game_END()



def unbinded(event):
    textbox.delete(1.0, END)
    textbox.insert(END, '''Can't run, you're locked in here!''')

def statuscheck():
    textbox.delete(1.0, END)
    if newenemy.max_health == newenemy.health:
        enemystatus = 'The {} is at maximum glory.'.format(newenemy.name)
    elif newenemy.health / newenemy.max_health >= 0.75 and newenemy.health / newenemy.max_health < 1:
        enemystatus = 'The {} is slightly wounded.'.format(newenemy.name)
    elif newenemy.health / newenemy.max_health >= 0.5 and  newenemy.health / newenemy.max_health < 0.75:
        enemystatus = 'The {} is wounded'.format(newenemy.name)
    elif newenemy.health / newenemy.max_health >= 0.25 and newenemy.health / newenemy.max_health < 0.5:
        enemystatus = 'The {} is severely wounded'.format(newenemy.name)
    elif newenemy.health / newenemy.max_health > 0 and newenemy.health / newenemy.max_health < 0.25:
        enemystatus = 'The {} is grievously wounded'.format(newenemy.name)
    else:
        print('wat')
    textbox.insert(END, 'You are at {0.health} health. Your max is 12. \nThe {1.name} is weak to {1.weakness}. \n'.format(player, newenemy)+enemystatus)

def enemycheck():
    if newenemy.health <= 0:
        textbox.delete(1.0, END)
        textbox.insert(END, 'You have slain the {}. And thus are able to escape the Dungeon.'.format(newenemy.name))
        return True
    else:
        return False

def Game_END():
    if enemycheck():
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
    else:
        newenemy.attack(player)
    if player.health <= 0:
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
        textbox.delete(1.0, END)
        textbox.insert(END, 'The {} has slain you and your body will remain in the Dungeon forever.'.format(newenemy.name))

    if enemycheck():
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()

def spell():
    textbox.delete(1.0, END)
    textbox.insert(END, "Which spell would you like to use?")
    btn1Nav.config(text='Fireball', command=spell_use_fireball)
    btn2Nav.config(text='Iceshard', command=spell_use_iceshard)
    btn3Nav.config(text='Thunderbolt', command=spell_use_thunderbolt)
    btnTop.pack(fill=X, padx=10)
    btnTop.config(text='Heal', command=spell_use_heal)
    btnMiddle.pack(fill=X, padx=10)
    btnMiddle.config(text='Back', command=spell_back)


def spell_use_fireball():
    player_hit_chance = D20()
    player.chosen_spell = Fireball()
    player.spell_string = 'Fireball'
    player.spell_attack(newenemy, player_hit_chance)
    player.mana -= Fireball().mana_cost
    spell_back()
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>', fightcheck)

def spell_use_iceshard():
    player_hit_chance = D20()
    player.chosen_spell = Iceshard()
    player.spell_string = 'Iceshard'
    player.spell_attack(newenemy, player_hit_chance)
    player.mana -= Iceshard().mana_cost
    spell_back()
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>', fightcheck)


def spell_use_thunderbolt():
    player_hit_chance = D20()
    player.chosen_spell = Thunderbolt()
    player.spell_string = 'Thunderbolt'
    player.spell_attack(newenemy, player_hit_chance)
    player.mana -= Thunderbolt().mana_cost
    spell_back()
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>', fightcheck)

def spell_use_heal():
    nowhealth = player.health
    player.mana -= Heal().mana_cost
    player.health += Heal().heal
    newhealth = player.health
    textbox.delete(1.0, END)
    if nowhealth == newhealth:
        textbox.insert(END, 'You were already at full health.')
    elif newhealth > nowhealth:
        healthchange = nowhealth - newhealth
        textbox.insert(END, 'You healed yourself for {} health.'.format(healthchange))
    spell_back()
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>', fightcheck)



def spell_back():
    btnTop.pack_forget()
    btnMiddle.pack_forget()
    fightOptions()

def battle(player,enemy):
    print("An enemy {0.name} appears with a defense of {0.evasion}".format(enemy))
    # Combat loop
    while player.health > 0 and enemy.health > 0:
        player_hit_chance = D20()
        textbox.delete(1.0, END)
        textbox.insert(END, "Do you want to attack, use a spell or do nothing?")
        if action.lower() == "attack":
            action_2 = input("Do you want to use a spell or melee attack? (spell, melee)")
            if action_2.lower() == 'melee':
                player.attack(enemy, player_hit_chance)

            if action_2.lower() == 'spell':
                w_spell = input("Which spell would you like to use? (Fireball, Thunderbolt, Iceshard")

                if player.mana >= 20:
                    if w_spell == 'Fireball':
                        player.chosen_spell = Fireball()
                        player.spell_attack(enemy, player_hit_chance)
                        player.mana -= Fireball().mana_cost
                    elif w_spell == 'Thunderbolt':
                        player.chosen_spell = Thunderbolt()
                        player.spell_attack(enemy, player_hit_chance)
                        player.mana -= Thunderbolt().mana_cost
                    elif w_spell == 'Iceshard':
                        player.chosen_spell = Iceshard()
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

    # Display outcome
    if enemy.health <= 0:
        player.xp += 14
        player.mana = 100
        xp_needed = 100 - player.xp

        print("You killed the {0.name}.".format(enemy))
        print('You gained 14 xp,', xp_needed, 'xp needed to gain a level')
    elif player.health <= 0:
        print("The {0.name} killed you.".format(enemy))

# ############# Dungeon Area ################## #


class Area:
    def __init__(self, Directions, Actions):
        self.Directions = Directions
        self.Actions = Actions

    def show_actions(self):
        mingid_suunad = []
        for i in ["n", "e", "s", "w"]:
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
        if vastus.lower() == "n":
            if player.current_area == not_visited_areas["Room1"]:
                if player.chosen_weapon is None:
                    print("This way seems dangerous. You need a weapon to be safe.")
                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["n"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["n"]]
        if vastus.lower() == "e":
            if player.current_area == not_visited_areas["Room1"]:
                if player.chosen_weapon is None:
                    print("This way seems dangerous. You need a weapon to be safe.")
                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["e"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["e"]]
        if vastus.lower() == "s":
            if player.current_area == not_visited_areas["Room1"]:
                if "key" not in player.Inventory:
                    print("The door seems to have locked behind you. The key might be further ahead.")

                else:
                    player.current_area = not_visited_areas[player.current_area.Directions["s"]]
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["s"]]
        if vastus.lower() == "w":
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
    def __init__(self, Directions={"n": "Room1", "e": None, "s": None, "w": None}, Actions=["Game_Over_Leave"]):
        super().__init__(Directions, Actions)
        self.name='Start'


class Room1_Area(Area):
    def __init__(self,Directions={"n":"Room1N", "e":"Room1E", "s":"Start", "w":"Room1W"}, Actions=[None]):
        super().__init__(Directions, Actions)
        self.name='Room1'


class Room1W_Area(Area):
    def __init__(self, Directions={"n":None, "e":"Room1", "s":None, "w":None}, Actions=["weapon"]):
        super().__init__(Directions, Actions)
        self.name='Room1W'


class Room1E_Area(Area):
    def __init__(self, Directions={"n":"Room2E", "e":None, "s":None, "w":"Room1"}, Actions=[None]):
        super().__init__(Directions, Actions)
        self.name='Room1E'

class Room2E_Area(Area):
    def __init__(self, Directions={"n":None, "e":None, "s":"Room1E", "w":None}, Actions=[None]):
        super().__init__(Directions, Actions)
        self.name='Room2E'


class Room1N_Area(Area):
    def __init__(self, Directions={"n":"Room2N", "e":None, "s":"Room1", "w":None}, Actions=[None]):
        super().__init__(Directions, Actions)
        self.name='Room1N'


class Room2N_Area(Area):
    def __init__(self, Directions={"n":"RoomBoss", "e":None, "s":"Room1N", "w":None}, Actions=[None]):
        super().__init__(Directions, Actions)
        self.name='Room2N'


class RoomBoss_Area(Area):
    def __init__(self, Directions={"n":None, "e":None, "s":"Room2N", "w":None}, Actions=["Get_Key","fight"]):
        super().__init__(Directions, Actions)
        self.name='RoomBoss'


###############################################################

visited_areas = []
not_visited_areas = {"Start": Start_Area(), "Room1": Room1_Area(), "Room1W": Room1W_Area(), "Room1E": Room1E_Area(),
                     "Room2E": Room2E_Area(), "Room1N": Room1N_Area(), "Room2N": Room2N_Area(), "RoomBoss": RoomBoss_Area()}


playerlist = [Player()]
player = playerlist[0]
enemylist = [Goblin()]
newenemy = enemylist[0]

thisishereasbandaid = False

def fight():
    battle(player, newenemy)

# enemies = [Enemy("Goblin", D4(), 8, 11)]


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

# Sisenedes Room1W näitab weapon buttonid ja paneb nende commandid


def weapons():
    btnTop.pack(fill=X, padx=10)
    btnTop.config(text="Mace", command=weapon_mace)
    btnMiddle.pack(fill=X, padx=10)
    btnMiddle.config(text="Stiletto", command=weapon_stiletto)
    btnBottom.pack(fill=X, padx=10)
    btnBottom.config(text="Scythe", command=weapon_scythe)

# Command, mis Room1W lahkudes peidab weapon nupud


def hideWeapons():
    btnTop.pack_forget()
    btnMiddle.pack_forget()
    btnBottom.pack_forget()


def fightOptions():
    global btnN, btnW, btnS, btnE, enemypic, playerpic, checkstatus, screen
    checkstatus = 1

    screen.update_idletasks()
    screen.update()
    if 'fight' in player.current_area.Actions:
        textbox.delete(1.0, END)
        textbox.insert(END, "You challenge the goblin to a fight")
        player.current_area.Actions.remove('fight')
    btnN.grid_forget()
    btnW.grid_forget()
    btnE.grid_forget()
    btnS.grid_forget()
    rw.bind('<w>', unbinded)
    rw.bind('<s>', unbinded)
    rw.bind('<a>', unbinded)
    rw.bind('<d>', unbinded)
    btn1Nav.pack(fill=X, padx=10)
    btn1Nav.config(text="Melee", command=melee)
    btn2Nav.pack(fill=X, padx=10)
    btn2Nav.config(text="Spell", command=spell)
    btn3Nav.pack(fill=X, padx=10)
    btn3Nav.config(text="Status", command=statuscheck)
    #screen.create_image(500, 140, anchor=NW, image=enemypic)
    #screen.create_image(100, 200, anchor=NW, image=playerpic)

def enemyattack():
    global playerpic, enemypic, screen
    if 'stunned' not in newenemy.status_effects:
        enemypic = goblinattack
        #screen.create_image(500, 140, anchor=NW, image=enemypic)
        enemy_hit_chance = D20()
        textbox.delete(1.0, END)
        if enemy_hit_chance >= player.evasion:
            textbox.insert(END, "The {0.name} attacks you and hits".format(newenemy))
            newenemy.attack(player)
        else:
            playerpic = playerdodge
            #screen.create_image(100, 200, anchor=NW, image=playerpic)
            textbox.insert(END, "The {0.name} tries to hit you but you dodge their attack.".format(newenemy))


# Checkmap command, mis ala kohta paneb õige minimapi display


def checkMap():
    global locationImage
    global imgR1N, imgR1, imgStart, imgR1E, imgR1W, imgR2E, imgR2N, imgRBoss, Backgroundpic
    if player.current_area not in visited_areas:
        visited_areas.append(player.current_area.name)
    if player.current_area == not_visited_areas["Start"]:
        locationImage = PhotoImage(file="pictures/LocatedRoomStart.png")
        imgStart = PhotoImage(file="pictures/ExploredRoomStart.png")
        Backgroundpic = PhotoImage(file='pictures/BGStart.png')
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchot=NW, image=imgStart)
    elif player.current_area == not_visited_areas["Room1"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom1.png")
        imgR1 = PhotoImage(file="pictures/ExploredRoom1.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom1.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR1)
    elif player.current_area == not_visited_areas["Room1W"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom1W.png")
        imgR1W = PhotoImage(file="pictures/ExploredRoom1W.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom1W.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR1W)
    elif player.current_area == not_visited_areas["Room1E"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom1E.png")
        imgR1E = PhotoImage(file="pictures/ExploredRoom1E.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom1E.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR1E)
    elif player.current_area == not_visited_areas["Room2E"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom2E.png")
        imgR2E = PhotoImage(file="pictures/ExploredRoom2E.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom2E.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR2E)
    elif player.current_area == not_visited_areas["Room1N"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom1N.png")
        imgR1N = PhotoImage(file="pictures/ExploredRoom1N.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom1N.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR1N)
    elif player.current_area == not_visited_areas["Room2N"]:
        locationImage = PhotoImage(file="pictures/LocatedRoom2N.png")
        imgR2N = PhotoImage(file="pictures/ExploredRoom2N.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoom2N.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgR2N)
    elif player.current_area == not_visited_areas["RoomBoss"]:
        locationImage = PhotoImage(file="pictures/LocatedRoomBoss.png")
        imgRBoss = PhotoImage(file="pictures/ExploredRoomBoss.png")
        Backgroundpic = PhotoImage(file='pictures/BGRoomBoss.png')
        screen.create_image(377, 252, image=Backgroundpic)
        screen.create_image(2, 2, anchor=NW, image=minimapBG)
        screen.create_image(2, 2, anchor=NW, image=imgRBoss)
    screen.create_image(2, 2, anchor=NW, image=locationImage)

    if "Start" in visited_areas:
        imgStart = PhotoImage(file="pictures/ExploredRoomStart.png")
        screen.create_image(2, 2, anchot=NW, image=imgStart)
    if "Room1" in visited_areas:
        imgR1 = PhotoImage(file="pictures/ExploredRoom1.png")
        screen.create_image(2, 2, anchor=NW, image=imgR1)
    if "Room1W" in visited_areas:
        imgR1W = PhotoImage(file="pictures/ExploredRoom1W.png")
        screen.create_image(2, 2, anchor=NW, image=imgR1W)
    if "Room1" in visited_areas:
        imgR1E = PhotoImage(file="pictures/ExploredRoom1E.png")
        screen.create_image(2, 2, anchor=NW, image=imgR1E)
    if "Room2E" in visited_areas:
        imgR2E = PhotoImage(file="pictures/ExploredRoom2E.png")
        screen.create_image(2, 2, anchor=NW, image=imgR2E)
    if "Room1N" in visited_areas:
        imgR1N = PhotoImage(file="pictures/ExploredRoom1N.png")
        screen.create_image(2, 2, anchor=NW, image=imgR1N)
    if "Room2N" in visited_areas:
        imgR2N = PhotoImage(file="pictures/ExploredRoom2N.png")
        screen.create_image(2, 2, anchor=NW, image=imgR2N)
    if "RoomBoss" in visited_areas:
        imgRBoss = PhotoImage(file="pictures/ExploredRoomBoss.png")
        screen.create_image(2, 2, anchor=NW, image=imgRBoss)


def move_N():
    if player.current_area.Directions["n"] is None:
        textbox.delete(1.0, END)
        textbox.insert(END, "The Northern wall has no path")
    else:

        if "weapon" in player.current_area.Actions:
            weapons()
        if player.current_area == not_visited_areas["Room1"]:
            if player.chosen_weapon is None:
                textbox.delete(1.0, END)
                textbox.insert(END, "This way seems dangerous. You need a weapon to be safe.")
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["n"]]
                textbox.delete(1.0, END)
                textbox.insert(END, "You decided to move north")
                if player.current_area == not_visited_areas["Room1N"]:
                    textbox.delete(1.0, END)
                    textbox.insert(END, "You notice light from a fire in the distance.")
                if player.current_area == not_visited_areas["Room2N"]:
                    textbox.delete(1.0, END)
                    textbox.insert(END, 'There seems to be an angry looking green midget up ahead.')
                if "fight" in player.current_area.Actions:
                    enemypic = PhotoImage(file='Pictures/GoblinIdle.png')
                    playerpic = PhotoImage(file='Pictures/PlayerIdle.png')
                    screen.create_image(500, 140, anchor=NW, image=enemypic)
                    screen.create_image(100, 200, anchor=NW, image=playerpic)
                    fightOptions()

                    #fight()
                    if player.health > 0:
                        player.current_area.Actions.remove("fight")
        else:
            player.current_area = not_visited_areas[player.current_area.Directions["n"]]
            textbox.delete(1.0, END)
            textbox.insert(END, "You decided to move north")
            if player.current_area == not_visited_areas["Room1N"]:
                textbox.delete(1.0, END)
                textbox.insert(END, "You notice light from a fire in the distance.")
            if player.current_area == not_visited_areas["Room2N"]:
                textbox.delete(1.0, END)
                textbox.insert(END, 'There seems to be an angry looking green midget up ahead.')
            if "fight" in player.current_area.Actions:
                enemypic = PhotoImage(file='Pictures/GoblinIdle.png')
                playerpic = PhotoImage(file='Pictures/PlayerIdle.png')
                screen.create_image(500, 140, anchor=NW, image=enemypic)
                screen.create_image(100, 200, anchor=NW, image=playerpic)
                fightOptions()

                if player.health >= 0:
                    #Game_End()
                    pass
        checkMap()



def move_E():
    if player.current_area.Directions["e"] is None:
        textbox.delete(1.0, END)
        textbox.insert(END, "The Eastern wall has no path")
    else:
        if "weapon" in player.current_area.Actions:
            hideWeapons()
        if player.current_area == not_visited_areas["Room1"]:
            if player.chosen_weapon is None:
                textbox.delete(1.0, END)
                textbox.insert(END, "This way seems dangerous. You need a weapon to be safe.")
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["e"]]
                textbox.delete(1.0, END)
                textbox.insert(END, "You decided to move east")
        else:
            player.current_area = not_visited_areas[player.current_area.Directions["e"]]
            textbox.delete(1.0, END)
            textbox.insert(END, "You decided to move east")
        checkMap()


def move_S():
    if player.current_area.Directions["s"] is None:
        textbox.delete(1.0, END)
        textbox.insert(END, "The Southern wall has no path")
    else:
        if "weapon" in player.current_area.Actions:
            weapons()

        if player.current_area == not_visited_areas["Room1"]:
            if "key" not in player.Inventory:
                textbox.delete(1.0, END)
                textbox.insert(END, "The door seems to have locked behind you. The key might be further ahead.")
            else:
                player.current_area = not_visited_areas[player.current_area.Directions["s"]]
                textbox.delete(1.0, END)
                textbox.insert(END, "You decided to move south")
        else:
            player.current_area = not_visited_areas[player.current_area.Directions["s"]]
            textbox.delete(1.0, END)
            textbox.insert(END, "You decided to move south")
        checkMap()


def move_W():
    if player.current_area.Directions["w"] is None:
        textbox.delete(1.0, END)
        textbox.insert(END, "The Western wall has no path")
    else:
        player.current_area = not_visited_areas[player.current_area.Directions["w"]]
        textbox.delete(1.0, END)
        textbox.insert(END, "You decided to move west")
        if "weapon" in player.current_area.Actions:
            weapons()
        checkMap()

# WASD movementi jaoks event commandid, suunavad tavalistele movement commandidele


def go_N(event):
    move_N()


def go_W(event):
    move_W()


def go_S(event):
    move_S()


def go_E(event):
    move_E()


def weapon_mace():
    player.chosen_weapon = Mace()
    textbox.delete(1.0, END)
    textbox.insert(END, "You chose the mace, a weapon capable of stunning enmies.")


def weapon_stiletto():
    player.chosen_weapon = Stiletto()
    textbox.delete(1.0, END)
    textbox.insert(END, "You chose the stiletto, a weapon for bleeding DOT damage.")


def weapon_scythe():
    player.chosen_weapon = Scythe()
    textbox.delete(1.0, END)
    textbox.insert(END, "You chose the scythe, a weapon covered with poisonous aura.")


def kill_buttons():
    btnTop.pack_forget()
    btnMiddle.pack_forget()
    btnBottom.pack_forget()


def fightcheck(event):
    global checkstatus, statuspic, screen,enemypic,playerpic,thisishereasbandaid
    btn1Nav.pack()
    btn1Nav.config(text='Press left mouse button to cont.', command= passfunc)
    if not thisishereasbandaid:
        screen.create_image(500, 140, anchor=NW, image=enemypic)
        screen.create_image(100, 200, anchor=NW, image=playerpic)
        thisishereasbandaid = True
    enemypic = goblinidle
    playerpic=playeridle
    if checkstatus == 1:
        playerpic= playeridle
        enemypic=goblinidle
        if 'stunned' in newenemy.status_effects:
            textbox.delete(1.0, END)
            textbox.insert(END, 'The goblin is stunned.')
            statuspic = PhotoImage(file='Pictures/StatusStunned.png')
            screen.create_image(500, 100, image=statuspic)
            checkstatus = 3
        else:
            checkstatus = 2
    elif checkstatus == 2:
        enemypic=goblinattack
        enemyattack()

        checkstatus = 3
    elif checkstatus == 3:
        playerpic = playeridle
        enemypic = goblinidle
        if 'poisoned' in newenemy.status_effects:
            dam = randint(1, 4)
            newenemy.health -= dam
            newenemy.status_effects.remove('poisoned')
            textbox.delete(1.0, END)
            textbox.insert(END, 'The {0.name} takes damage from poison.'.format(newenemy))
            statuspic = PhotoImage(file='Pictures/StatusPoisoned.png')
            screen.create_image(500, 100, image=statuspic)
        if 'bleeding' in newenemy.status_effects:
            dam = randint(1, 6)
            newenemy.health -= dam
            newenemy.status_effects.remove('bleeding')
            textbox.delete(1.0, END)
            textbox.insert(END, 'The {0.name} takes damage from bleeding.'.format(newenemy))
            statuspic = PhotoImage(file='Pictures/StatusBleeding.png')
            screen.create_image(500, 100, image=statuspic)
        checkstatus = 4
    elif checkstatus == 4:
        statuspic = None
        fightOptions()
        rw.bind('<Button-1>', passfunc)


def passfunc(event):
    pass




rw = Tk()

rw.resizable(False, False)
# Tegin 2 suuremat frame, top ja bottom display ja alumise osa jaoks
displayFrame = Frame(rw, width=750, height=500)
displayFrame.pack(fill=BOTH, expand=YES, side=TOP)


bottomFrame = Frame(rw, bg='gray')
bottomFrame.pack(fill=BOTH, pady=10, padx=10)

# 3 frame, mis paigutatud bottom frame sisse(NESW nupud, Buttonite area, Textboxi area)
navigationFrame = Frame(bottomFrame, bg='gray')
navigationFrame.grid(column=0, row=0, sticky=W)

buttonFrame = Frame(bottomFrame, bg='gray')
buttonFrame.grid(column=1, row=0)

textFrame = Frame(bottomFrame, bg='gray')
textFrame.grid(column=2, row=0, sticky=E)

screen = Canvas(displayFrame, bg="darksalmon", height=500, width=750)
screen.pack(fill=X, expand=YES, side=TOP)

btn1Nav = Button(navigationFrame)
btn2Nav = Button(navigationFrame)
btn3Nav = Button(navigationFrame)

btnN = Button(navigationFrame, text="N", borderwidth=2, relief='groove', width=2)
btnN.grid(column=1, row=0)
btnN.config(command=move_N)

btnE = Button(navigationFrame, text="E", borderwidth=2, relief='groove', width=2)
btnE.grid(column=2, row=1)
btnE.config(command=move_E)

btnS = Button(navigationFrame, text="S", borderwidth=2, relief='groove', width=2)
btnS.grid(column=1, row=2)
btnS.config(command=move_S)

btnW = Button(navigationFrame, text="W", borderwidth=2, relief='groove', width=2)
btnW.grid(column=0, row=1)
btnW.config(command=move_W)

# Bindisin WASD keyboardilt map movementi jaoks
rw.bind("w", go_N)
rw.bind("a", go_W)
rw.bind("d", go_E)
rw.bind("s", go_S)

# Tegin ühe textboxi, mille teksti saab korduvalt muuta(Check weapons or movement restricions for example)
textbox = Text(textFrame, height=4, width=60, wrap=WORD)
textbox.insert(END, "This is a box of text")
textbox.pack(side=RIGHT)

# Tegin alguses valmis kolme nupu variabled, mida muuta (3 weaponi jaoks hetkel, aga saab kasutada muu jaoks veel)
btnTop = Button(buttonFrame, text="First Button", command=kill_buttons)
btnTop.pack(fill=X, padx=10)

btnMiddle = Button(buttonFrame, text="Second Button", command=kill_buttons)
btnMiddle.pack(fill=X, padx=10)

btnBottom = Button(buttonFrame, text="Third Button", command=kill_buttons)
btnBottom.pack(fill=X, padx=10)

Backgroundpic = PhotoImage(file='pictures/BGStart.png')
screen.create_image(377,252, image=Backgroundpic)


enemypic = PhotoImage(file='Pictures/GoblinIdle.png')
playerpic = PhotoImage(file='Pictures/PlayerIdle.png')

# Impordin starting are image minimapi jaoks
minimapBG = PhotoImage(file="pictures/Background.png")
minimapImage = PhotoImage(file="pictures/ExploredRoomStart.png")
locationImage = PhotoImage(file="pictures/LocatedRoomStart.png")
screen.create_image(2, 2, anchor=NW, image=minimapBG)
screen.create_image(2, 2, anchor=NW, image=minimapImage)
screen.create_image(2, 2, anchor=NW, image=locationImage)

goblindodge = PhotoImage(file='Pictures/GoblinDodge.png')
goblinattack = PhotoImage(file='Pictures/GoblinAttack.png')
goblinidle = PhotoImage(file='Pictures/GoblinIdle.png')
playeridle = PhotoImage(file='Pictures/PlayerIdle.png')
playerattack = PhotoImage(file='Pictures/PlayerAttack.png')
playerdodge = PhotoImage(file='Pictures/PlayerDodge.png')

rw.mainloop()