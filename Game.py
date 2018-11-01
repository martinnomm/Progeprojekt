import Dices
import Characters
import random
import time

playerlist = [Characters.Player()]
player = playerlist[0]

def fight():
    Characters.battle(player, Characters.Goblin())



#enemies = [Characters.Enemy("Goblin", Dices.D4(), 8, 11)]

while True:
    print("Choose a direction(left or right) or fight")
    vastus = input("")
    if vastus.lower() in ("left","right"):
        print("You decide to move {}.".format(vastus))
        time.sleep(1)
        if Dices.D20() > 4:
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