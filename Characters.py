from builtins import bool
from sched import scheduler
from time import *
from Dices import *
from Spells import *
from tkinter import *


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
            print("You cast a spell on the {0.name}".format(target))
            print("Hit chance is {}.".format(hit_chance))
            sleep(0.1)
            print("Your spell hits the {0.name}".format(target))
            target.health -= randint(self.chosen_spell.damg[0], self.chosen_spell.damg[1])
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

#Sisenedes Room1W näitab weapon buttonid ja paneb nende commandid
def weapons():
    btnTop.pack(fill=X,padx=10)
    btnTop.config(text="Mace",command=weapon_mace)
    btnMiddle.pack(fill=X,padx=10)
    btnMiddle.config(text="Stiletto",command=weapon_stiletto)
    btnBottom.pack(fill=X,padx=10)
    btnBottom.config(text="Scythe",command=weapon_scythe)

#Command, mis Room1W lahkudes peidab weapon nupud
def hideWeapons():
    btnTop.pack_forget()
    btnMiddle.pack_forget()
    btnBottom.pack_forget()

def fightOptions():
    textbox.delete(1.0, END)
    textbox.insert(END, "You challenge the goblin to a fight")
    btnN.pack_forget()
    btnW.pack_forget()
    btnE.pack_forget()
    btnS.pack_forget()
    btnTop.pack(fill=X, padx=10)
    btnTop.config(text="Melee", command=weapon_mace)
    btnMiddle.pack(fill=X, padx=10)
    btnMiddle.config(text="Spell", command=weapon_stiletto)
    btnBottom.pack(fill=X, padx=10)
    btnBottom.config(text="Skip turn", command=weapon_scythe)
#Checkmap command, mis ala kohta paneb õige minimapi display
def checkMap():
    global minimapImage
    if player.current_area == not_visited_areas["Start"]:
        minimapImage=PhotoImage(file="XpicRoomStart.png")
    elif player.current_area == not_visited_areas["Room1"]:
        minimapImage=PhotoImage(file="XpicRoom1.png")
    elif player.current_area == not_visited_areas["Room1W"]:
        minimapImage=PhotoImage(file="XpicRoom1W.png")
    elif player.current_area == not_visited_areas["Room1E"]:
        minimapImage=PhotoImage(file="XpicRoom1E.png")
    elif player.current_area == not_visited_areas["Room2E"]:
        minimapImage=PhotoImage(file="XpicRoom2E.png")
    elif player.current_area == not_visited_areas["Room1N"]:
        minimapImage=PhotoImage(file="XpicRoom1N.png")
    elif player.current_area == not_visited_areas["Room2N"]:
        minimapImage=PhotoImage(file="XpicRoom2N.png")
    elif player.current_area == not_visited_areas["RoomBoss"]:
        minimapImage=PhotoImage(file="XpicRoomBoss.png")
    screen.create_image(0, 0, anchor=NW, image=minimapImage)


def move_N():
    #siin peaks fight algama aga ei kutsu esile
    if "fight" in player.current_area.Actions:
        fight()
        if player.health > 0:
            player.current_area.Actions.remove("fight")
    if "weapon" in player.current_area.Actions:
        weapons()
    if player.current_area == not_visited_areas["Room1"]:
        if player.chosen_weapon is None:
            #T=Text(rw, height=2, width=30)
            textbox.delete(1.0, END)
            textbox.insert(END, "This way seems dangerous. You need a weapon to be safe.")
            #T.pack()
        else:
            player.current_area = not_visited_areas[player.current_area.Directions["n"]]
            textbox.delete(1.0, END)
            textbox.insert(END, "You decided to move north")
    else:
        player.current_area = not_visited_areas[player.current_area.Directions["n"]]
        textbox.delete(1.0, END)
        textbox.insert(END, "You decided to move north")
    checkMap()

def move_E():
    if "weapon" in player.current_area.Actions:
        hideWeapons()
    if player.current_area == not_visited_areas["Room1"]:
        if player.chosen_weapon is None:
            #T = Text(rw, height=2, width=30)
            textbox.delete(1.0, END)
            textbox.insert(END, "This way seems dangerous. You need a weapon to be safe.")
            #T.pack()
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
    if "weapon" in player.current_area.Actions:
        weapons()

    if player.current_area == not_visited_areas["Room1"]:
        if "key" not in player.Inventory:
            #T = Text(rw, height=2, width=30)
            textbox.delete(1.0, END)
            textbox.insert(END, "The door seems to have locked behind you. The key might be further ahead.")
            #T.pack()
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
    player.current_area = not_visited_areas[player.current_area.Directions["w"]]
    textbox.delete(1.0, END)
    textbox.insert(END, "You decided to move west")
    if "weapon" in player.current_area.Actions:
        weapons()
    checkMap()

#WASD movementi jaoks event commandid, suunavad tavalistele movement commandidele
def go_N(event):
    move_N()
def go_W(event):
    move_W()
def go_S(event):
    move_S()
def go_E(event):
    move_E()
# def move_S():
#     if "weapon" in player.current_area.Actions:
#         btn.pack_forget()
#         btn2.pack_forget()
#         btn3.pack_forget()
#         btn4.pack_forget()
#         wpn1=Button(rw, text="Mace")
#         wpn1.pack()
#         wpn2=Button(rw,text="Stiletto")
#         wpn2.pack()
#         wpn3=Button(rw, text="Scythe")
#         wpn3.pack()
#         backb=Button(rw, text="Back")
#         backb.pack()
#         t= Text(rw, height=2, width=30)
#         t.insert(END, "Current weapon:")
#         t.pack()
#     if player.current_area == not_visited_areas["Room1"]:
#         if "key" not in player.Inventory:
#             T = Text(rw, height=2, width=30)
#             T.insert(END, "The door seems to have locked behind you. The key might be further ahead.")
#             T.pack()
#         else:
#             player.current_area = not_visited_areas[player.current_area.Directions["s"]]
#     else:
# player.current_area = not_visited_areas[player.current_area.Directions["s"]]

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


rw = Tk()

#Tegin 2 suuremat frame, top ja bottom display ja alumise osa jaoks
displayFrame=Frame(rw)
displayFrame.grid(rowspan=2)


bottomFrame=Frame(rw)
bottomFrame.grid()

#3 frame, mis paigutatud bottom frame sisse(NESW nupud, Buttonite area, Textboxi area)
navigationFrame=Frame(bottomFrame)
navigationFrame.grid(column=0,row=0,sticky=W)

buttonFrame=Frame(bottomFrame)
buttonFrame.grid(column=1,row=0)

textFrame=Frame(bottomFrame)
textFrame.grid(column=2,row=0,sticky=E)

screen=Canvas(displayFrame,bg="lime")
screen.pack()

btnN=Button(navigationFrame, text="N")
btnN.grid(column=1,row=0)
btnN.config(command=move_N)

btnE = Button(navigationFrame, text="E")
btnE.grid(column=2,row=1)
btnE.config(command=move_E)

btnS=Button(navigationFrame, text="S")
btnS.grid(column=1,row=2)
btnS.config(command=move_S)

btnW=Button(navigationFrame, text="W")
btnW.grid(column=0,row=1)
btnW.config(command=move_W)

#Bindisin WASD keyboardilt map movementi jaoks
rw.bind("w",go_N)
rw.bind("a",go_W)
rw.bind("d",go_E)
rw.bind("s",go_S)

#Tegin ühe textboxi, mille teksti saab korduvalt muuta(Check weapons or movement restricions for example)
textbox=Text(textFrame,height=4,width=25)
textbox.insert(END,"This is a box of text")
textbox.pack()

#Tegin alguses valmis kolme nupu variabled, mida muuta (3 weaponi jaoks hetkel, aga saab kasutada muu jaoks veel)
btnTop=Button(buttonFrame, text="First Button")
btnTop.pack(fill=X,padx=10)
btnTop.pack_forget()

btnMiddle=Button(buttonFrame, text="Second Button")
btnMiddle.pack(fill=X,padx=10)
btnMiddle.pack_forget()

btnBottom=Button(buttonFrame, text="Third Button")
btnBottom.pack(fill=X,padx=10)
btnBottom.pack_forget()

#Impordin starting are image minimapi jaoks
minimapImage = PhotoImage(file="XpicRoomStart.png")
screen.create_image(2,1,anchor=NW, image=minimapImage)

rw.mainloop()




