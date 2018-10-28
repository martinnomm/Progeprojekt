import Dices
import Characters
import random
import time


def fight():
    Characters.battle(Characters.Player(), random.choice(enemies))



enemies = [Characters.Enemy("Goblin", Dices.D4(), 8, 11)]

#fight()






while True:
    print("Choose a direction(left or right)")
    vastus = input("")
    if vastus.lower() in ("left","right"):
        print("You decide to move {}.".format(vastus))
        time.sleep(2)
        if Dices.D20() > 4:
            print("You reach your destination safely")
        else:
            fight()
    else:
        print("Not understood, you stay put")
        time.sleep(1)