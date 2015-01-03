import sys, os, time, random, _thread, threading
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.animatronics as animatronics
import pyDLASYIAS.main as main

def launcher():
    print("pyDon't let animatronics stuff you in a suit -pyDLASYIAS-")
    print("1 - Custom night")
    print("2 - 20/20/20/20 mode")
    print("3 - Test option please ignore")
    inp = input("> ")
    if inp == "1":
        belvl = input("Input Bear's AI LVL: ")
        ralvl = input("Input Rabbit's AI LVL: ")
        chilvl = input("Input Chicken's AI LVL: ")
        folvl = input("Input Fox's AI LVL: ")
        rabbit = animatronics.animatronic("Rabbit", "rabbit", int(ralvl))
        chicken = animatronics.animatronic("Chicken", "chicken", int(chilvl))
        fox = animatronics.animatronic("Fox", "fox", int(folvl), "cam1c")
        bear = animatronics.animatronic("Bear", "bear", int(belvl))
        m = main.main("custom", 100, 0)
        return None

    if inp == "2":
        rabbit = animatronics.animatronic("Rabbit", "rabbit", 20)
        chicken = animatronics.animatronic("Chicken", "chicken", 20)
        fox = animatronics.animatronic("Fox", "fox", 20, "cam1c")
        bear = animatronics.animatronic("Bear", "bear", 20)
        m = main.main("custom", 100, 0)
        return None

    if inp == "3":
        inp = input("Input test mode code: ")
        if inp == "1": #Death debugging.
            rabbit = animatronics.animatronic("Rabbit", "rabbit", 20, "inside")
            m = main.main("custom", 10, 0)
            return None

        if inp == "2": #Bear behavior debugging.
            bear = animatronics.animatronic("Bear", "bear", 20, "cam1a")
            m = main.main("survival", 100, 0)
            return None

        if inp == "3": #Chicken debugging.
            chicken = animatronics.animatronic("Chicken", "chicken", 20, "cam1a")
            m = main.main("survival", 100, 0)
            return None

        else:
            print("Code invalid. Going back to the menu...")
            launcher()
            return None

    else:
        launcher()

if __name__ == '__main__':
    launcher()
