from Dices import *
from Characters import *
from random import randint
import time



while True:
    break
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

while True:
    player.current_area.show_actions()
    if player.Game_Over is not None:
        if player.Game_Over == "Leave":
            print("You decide to leave the Dungeon")
            break