from Dices import *
from Characters import *
from random import randint
import time

playerlist = [Player()]
player = playerlist[0]
visited_areas = []
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

while True:
    choose_weapon()
    print("Choose a direction(left or right) or fight")
    vastus = input("")
    if vastus.lower() in ("left","right"):
        print("You decide to move {}.".format(vastus))
        time.sleep(1)
        if D20() > 4:
            print("You reach your destination safely")
        else:
            fight()
            if player.health <= 0:
                print("GAME OVER")
                break
    elif vastus.lower() == "fight":
        fight()
        if player.health <= 0:
            print("GAME OVER")
            break

    else:
        print("Not understood, you stay put")
        time.sleep(1)



