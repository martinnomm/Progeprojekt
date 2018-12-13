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
        self.picstatus = None
        self.chosen_enemy = None
        self.max_health = 12
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
                if D20() > 12:
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

    def picSet(self, moment):
        if moment == 'Idle':
            self.picstatus = PhotoImage(file='Pictures/PlayerIdle.png')
        if moment == 'Attack':
            self.picstatus = PhotoImage(file='Pictures/PlayerAttack.png')
        if moment == 'Dodge':
            self.picstatus = PhotoImage(file='Pictures/PlayerDodge.png')
        if moment == 'None':
            self.picstatus = None


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
        self.picstatus = None

    def attack(self, target):
        target.health -= D6()

    def picSet(self, moment):
        if moment == 'Idle':
            self.picstatus = PhotoImage(file='Pictures/GoblinIdle.png')
        if moment == 'Attack':
            self.picstatus = PhotoImage(file='Pictures/GoblinAttack.png')
        if moment == 'Dodge':
            self.picstatus = PhotoImage(file='Pictures/GoblinDodge.png')
        if moment == 'None':
            self.picstatus = None






def unbinded(event):
    textbox.delete(1.0, END)
    textbox.insert(END, '''Can't run, you're locked in here!''')

def statuscheck():
    textbox.delete(1.0, END)
    if player.chosen_enemy.max_health == player.chosen_enemy.health:
        enemystatus = 'The {} is at maximum glory.'.format(player.chosen_enemy.name)
    elif player.chosen_enemy.health / player.chosen_enemy.max_health >= 0.75 and player.chosen_enemy.health / player.chosen_enemy.max_health < 1:
        enemystatus = 'The {} is slightly wounded.'.format(player.chosen_enemy.name)
    elif player.chosen_enemy.health / player.chosen_enemy.max_health >= 0.5 and  player.chosen_enemy.health / player.chosen_enemy.max_health < 0.75:
        enemystatus = 'The {} is wounded'.format(player.chosen_enemy.name)
    elif player.chosen_enemy.health / player.chosen_enemy.max_health >= 0.25 and player.chosen_enemy.health / player.chosen_enemy.max_health < 0.5:
        enemystatus = 'The {} is severely wounded'.format(player.chosen_enemy.name)
    elif player.chosen_enemy.health / player.chosen_enemy.max_health > 0 and player.chosen_enemy.health / player.chosen_enemy.max_health < 0.25:
        enemystatus = 'The {} is grievously wounded'.format(player.chosen_enemy.name)
    else:
        print('wat')
        enemystatus = 'Wat'
    textbox.insert(END, 'You are at {0.health} health. Your max is 12. \nThe {1.name} is weak to {1.weakness}. \n'.format(player, player.chosen_enemy)+enemystatus)

def melee():
    global playerpic, screen, enemypic
    player.picSet('Attack')

    player_hit_chance = D20()
    if player_hit_chance < player.chosen_enemy.evasion:
        player.chosen_enemy.picSet('Dodge')
        screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
    screen.create_image(100, 200, anchor=NW, image=player.picstatus)
    player.attack(player.chosen_enemy, player_hit_chance)
    btn1Nav.pack_forget()
    btn2Nav.pack_forget()
    btn3Nav.pack_forget()
    rw.bind('<Button-1>', fightcheck)

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
    global playerpic, enemypic, screen, fireballpic
    if player.mana < 20:
        textbox.delete(1.0, END)
        textbox.insert(END, 'You do not have enough mana to cast Fireball.')
    else:

        player_hit_chance = D20()
        player.chosen_spell = Fireball()
        player.spell_string = 'Fireball'
        if not(player_hit_chance >= player.chosen_enemy.evasion):
            player.chosen_enemy.picSet('Dodge')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        else:
            player.chosen_enemy.picSet('Idle')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        player.spell_attack(player.chosen_enemy, player_hit_chance)
        player.mana -= Fireball().mana_cost
        spell_back()
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
        rw.bind('<Button-1>', fightcheck)
        playerpic = player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        fireballpic = PhotoImage(file='Pictures/SpellFireball.png')
        screen.create_image(300, 230, anchor=NW, image=fireballpic)

def spell_use_iceshard():
    global playerpic, enemypic, screen, iceshardpic
    if player.mana < 20:
        textbox.delete(1.0,END)
        textbox.insert(END, 'You do not have enough mana to cast Iceshard')
    else:
        player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        player_hit_chance = D20()
        player.chosen_spell = Iceshard()
        player.spell_string = 'Iceshard'
        if not(player_hit_chance >= player.chosen_enemy.evasion):
            player.chosen_enemy.picSet('Dodge')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        else:
            player.chosen_enemy.picSet('Idle')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        player.spell_attack(player.chosen_enemy, player_hit_chance)
        player.mana -= Iceshard().mana_cost
        spell_back()
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
        rw.bind('<Button-1>', fightcheck)
        playerpic = player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        iceshardpic = PhotoImage(file='Pictures/SpellIceshard.png')
        screen.create_image(300, 230, anchor=NW, image=iceshardpic)


def spell_use_thunderbolt():
    global playerpic, enemypic, screen, thunderboltpic
    if player.mana < 20:
        textbox.delete(1.0, END)
        textbox.insert(END, 'You do not have enough mana to cast Thunderbolt.')
    else:
        player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        player_hit_chance = D20()
        player.chosen_spell = Thunderbolt()
        player.spell_string = 'Thunderbolt'
        if not(player_hit_chance >= player.chosen_enemy.evasion):
            player.chosen_enemy.picSet('Dodge')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        else:
            player.chosen_enemy.picSet('Idle')
            screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        player.spell_attack(player.chosen_enemy, player_hit_chance)
        player.mana -= Thunderbolt().mana_cost
        spell_back()
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
        rw.bind('<Button-1>', fightcheck)
        playerpic = player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        thunderboltpic = PhotoImage(file='Pictures/SpellThunderbolt.png')
        screen.create_image(300, 230, anchor=NW, image=thunderboltpic)

def spell_use_heal():
    global playerpic,enemypic,screen, healpic
    if player.mana < 25:
        textbox.delete(1.0, END)
        textbox.insert(END, 'You do not have enough mana to cast Heal.')
    else:
        player.picSet('Idle')
        player.chosen_enemy.picSet('Idle')
        screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        nowhealth = player.health
        player.mana -= Heal().mana_cost
        player.health += Heal().heal
        if player.health > player.max_health:
            player.health = player.max_health
        newhealth = player.health
        textbox.delete(1.0, END)
        if nowhealth == newhealth:
            textbox.insert(END, 'You were already at full health.')
        elif newhealth > nowhealth:
            healthchange = newhealth - nowhealth
            textbox.insert(END, 'You healed yourself for {} health.'.format(healthchange))
        spell_back()
        btn1Nav.pack_forget()
        btn2Nav.pack_forget()
        btn3Nav.pack_forget()
        rw.bind('<Button-1>', fightcheck)
        playerpic = player.picSet('Attack')
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        healpic = PhotoImage(file='Pictures/SpellHeal.png')
        screen.create_image(300, 230, anchor=NW, image=healpic)



def spell_back():
    btnTop.pack_forget()
    btnMiddle.pack_forget()
    fightOptions()


# ############# Dungeon Area ################## #


class Area:
    def __init__(self, Directions, Actions):
        self.Directions = Directions
        self.Actions = Actions


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

# Neid pole vaja tähele panna, kood töötab täiuslikult ilma kõrvaliste parandusteta :)
thisishereasbandaid = False
thisishereasbandaid2 = False
thisishereasbandaid3 = False

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
    global btnN, btnW, btnS, btnE, enemypic, playerpic, checkstatus, screen, thisishereasbandaid, thisishereasbandaid2
    player.chosen_enemy.picSet('Idle')
    player.picSet('Idle')
    screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
    screen.create_image(100, 200, anchor=NW, image=player.picstatus)
    screen.update_idletasks()
    screen.update()
    checkstatus=1
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


def enemyattack():
    global playerpic, enemypic, screen
    if 'stunned' not in player.chosen_enemy.status_effects:
        player.chosen_enemy.picSet('Attack')
        screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        enemy_hit_chance = D20()
        textbox.delete(1.0, END)
        if enemy_hit_chance >= player.evasion:
            player.picSet('Idle')
            screen.create_image(100, 200, anchor=NW, image=player.picstatus)
            textbox.insert(END, "The {0.name} attacks you and hits".format(player.chosen_enemy))
            player.chosen_enemy.attack(player)
        else:
            player.picSet('Dodge')
            screen.create_image(100, 200, anchor=NW, image=player.picstatus)
            textbox.insert(END, "The {0.name} tries to hit you but you dodge their attack.".format(player.chosen_enemy))
    else:
        player.chosen_enemy.status_effects.remove('stunned')

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
    global thisishereasbandaid3, Backgroundpic, screen
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
                    Backgroundpic = PhotoImage(file='pictures/BGRoomBoss.png')
                    screen.create_image(377, 252, image=Backgroundpic)
                    if player.current_area == not_visited_areas["RoomBoss"]:
                        player.chosen_enemy = newenemy
                    fightOptions()

                    thisishereasbandaid3 = True
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
                Backgroundpic = PhotoImage(file='pictures/BGRoomBoss.png')
                screen.create_image(377, 252, image=Backgroundpic)
                if player.current_area == not_visited_areas["RoomBoss"]:
                    player.chosen_enemy = newenemy
                fightOptions()
                thisishereasbandaid3 = True

        if not thisishereasbandaid3:
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
    global checkstatus, statuspic, screen, enemypic, playerpic, thisishereasbandaid, fireballpic, iceshardpic, thunderboltpic, healpic, Backgroundpic
    btn1Nav.pack()
    btn1Nav.config(text='Press left mouse button to cont.', command= passfuncnoevent)
    if not thisishereasbandaid:
        thisishereasbandaid = True
    if checkstatus == 1:
        if player.health <= 0 or player.chosen_enemy.health <= 0:
            rw.bind('<Button-1>', passfunc)
            rw.bind('w', passfunc)
            checkstatus = 1
            btn1Nav.pack_forget()
            if player.health <= 0:
                player.picSet('None')
                textbox.delete(1.0,END)
                textbox.insert(END,
                               "You have been defeated by the Goblin and your soul will remain in the dungeon forever.")
            if player.chosen_enemy.health <= 0:
                player.chosen_enemy.picSet('None')
                textbox.delete(1.0,END)
                textbox.insert(END,
                               "You have defeated the evil Goblin and you can finally escape the dreaded dungeon.")


            Backgroundpic = PhotoImage(file='pictures/GameOver.png')
            screen.create_image(377, 252, image=Backgroundpic)

        elif 'stunned' in player.chosen_enemy.status_effects:
            textbox.delete(1.0, END)
            textbox.insert(END, 'The goblin is stunned.')
            statuspic = PhotoImage(file='Pictures/StatusStunned.png')
            screen.create_image(500, 100, image=statuspic)
            checkstatus = 3
            player.chosen_enemy.status_effects.remove('stunned')
        else:
            checkstatus = 2
    elif checkstatus == 2:
        fireballpic = None
        iceshardpic = None
        thunderboltpic = None
        healpic = None

        enemyattack()

        checkstatus = 3
    elif checkstatus == 3:
        player.picSet('Idle')
        player.chosen_enemy.picSet('Idle')
        screen.create_image(500, 140, anchor=NW, image=player.chosen_enemy.picstatus)
        screen.create_image(100, 200, anchor=NW, image=player.picstatus)
        if 'poisoned' in player.chosen_enemy.status_effects:
            dam = randint(1, 4)
            player.chosen_enemy.health -= dam
            player.chosen_enemy.status_effects.remove('poisoned')
            textbox.delete(1.0, END)
            textbox.insert(END, 'The {0.name} takes damage from poison.'.format(player.chosen_enemy))
            statuspic = PhotoImage(file='Pictures/StatusPoisoned.png')
            screen.create_image(500, 100, image=statuspic)
        if 'bleeding' in player.chosen_enemy.status_effects:
            dam = randint(1, 6)
            player.chosen_enemy.health -= dam
            player.chosen_enemy.status_effects.remove('bleeding')
            textbox.delete(1.0, END)
            textbox.insert(END, 'The {0.name} takes damage from bleeding.'.format(player.chosen_enemy))
            statuspic = PhotoImage(file='Pictures/StatusBleeding.png')
            screen.create_image(500, 100, image=statuspic)
        checkstatus = 4
    elif checkstatus == 4:
        statuspic = None
        fightOptions()
        rw.bind('<Button-1>', passfunc)

def passfuncnoevent():
    pass
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
textbox = Text(textFrame, height=4, width=60, wrap=WORD, borderwidth=2, relief='groove')
textbox.insert(END, "You are a young adventurer with a curious mind. It just so happens that you found a mysterious door and are itching to see what lies beyond.")
textbox.pack(side=RIGHT)

# Tegin alguses valmis kolme nupu variabled, mida muuta (3 weaponi jaoks hetkel, aga saab kasutada muu jaoks veel)
btnTop = Button(buttonFrame, text="First Button", command=kill_buttons, borderwidth=2, relief='groove')

btnMiddle = Button(buttonFrame, text="Second Button", command=kill_buttons, borderwidth=2, relief='groove')

btnBottom = Button(buttonFrame, text="Third Button", command=kill_buttons, borderwidth=2, relief='groove')

Backgroundpic = PhotoImage(file='pictures/BGStart.png')
screen.create_image(377,252, image=Backgroundpic)

# Impordin starting are image minimapi jaoks
minimapBG = PhotoImage(file="pictures/Background.png")
minimapImage = PhotoImage(file="pictures/ExploredRoomStart.png")
locationImage = PhotoImage(file="pictures/LocatedRoomStart.png")
screen.create_image(2, 2, anchor=NW, image=minimapBG)
screen.create_image(2, 2, anchor=NW, image=minimapImage)
screen.create_image(2, 2, anchor=NW, image=locationImage)

rw.mainloop()
