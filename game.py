#!/usr/bin/env python
import sys
import os
import time
import random
import _thread
import threading
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.animatronics as animatronics
import pyDLASYIAS.main as main


def launcher():
    print("pyDon't let animatronics stuff you in a suit -pyDLASYIAS-")
    print("1 - Custom night")
    print("2 - 20/20/20/20 mode")
    print("3 - Random night. W.I.P -BUGGY/EXPERIMENTAL-")
    print("4 - Real-time mode! (With limited power)")
    print("5 - Test option please ignore")
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
        main.main("custom", 100, 0)
        return None

    if inp == "2":
        rabbit = animatronics.animatronic("Rabbit", "rabbit", 20)
        chicken = animatronics.animatronic("Chicken", "chicken", 20)
        fox = animatronics.animatronic("Fox", "fox", 20, "cam1c")
        bear = animatronics.animatronic("Bear", "bear", 20)
        main.main("custom", 100, 0)
        return None

    if inp == "3":
        rabbit = animatronics.animatronic("Rabbit", "rabbit", random.randint(1, 20))
        print("Rabbit's AILVL is %s" % (rabbit.ailvl))
        chicken = animatronics.animatronic("Chicken", "chicken", random.randint(1, 20))
        print("Chicken's AILVL is %s" % (chicken.ailvl))
        fox = animatronics.animatronic("Fox", "fox", random.randint(1, 20), "cam1c")
        print("Fox's AILVL is %s" % (fox.ailvl))
        bear = animatronics.animatronic("Bear", "bear", random.randint(1, 20))
        print("Bear's AILVL is %s" % (bear.ailvl))
        main.main("custom", random.randint(50, 100), random.randint(0, 6))
        return None

    if inp == "4":
        belvl = input("Input Bear's AI LVL: ")
        ralvl = input("Input Rabbit's AI LVL: ")
        chilvl = input("Input Chicken's AI LVL: ")
        folvl = input("Input Fox's AI LVL: ")
        rabbit = animatronics.animatronic("Rabbit", "rabbit", int(ralvl))
        chicken = animatronics.animatronic("Chicken", "chicken", int(chilvl))
        fox = animatronics.animatronic("Fox", "fox", int(folvl), "cam1c")
        bear = animatronics.animatronic("Bear", "bear", int(belvl))
        main.main("custom", 100, 0, sectohour=3600)

    if inp == "5":
        inp = input("Input test mode code: ")
        if inp == "1": #Death debugging.
            rabbit = animatronics.animatronic("Rabbit", "rabbit", 20, "inside")
            main.main("custom", 10, 0)
            return None

        if inp == "2": #Bear behavior debugging.
            bear = animatronics.animatronic("Bear", "bear", 20, "cam1a")
            main.main("survival", 100, 0)
            return None

        if inp == "3": #Chicken debugging.
            chicken = animatronics.animatronic("Chicken", "chicken", 20, "cam1a")
            main.main("survival", 100, 0)
            return None

        else:
            print("Code invalid. Going back to the menu...")
            launcher()
            return None

    else:
        launcher()

try:
    if __name__ == '__main__':
        launcher()
except:
    Globals.log.write("\n Unexpected error: %s %s \n" % (sys.exc_info()[0], time.strftime("%H:%M:%S")))
