import random
import sys
import os
import time
import pygame
import pyDLASYIAS.Globals as Globals

pygame.init()

Globals.log = open("log.txt", "a")
Globals.log.write(time.strftime("\n %d/%m/%Y - %H:%M:%S \n"))

def debugprint(text, animatronic=None, writetolog=True):
    if writetolog == True:
        if animatronic == None:
            Globals.log.write("%s %s \n" % (text, time.strftime("%H:%M:%S")))
        else:
            Globals.log.write("%s -%s BEHAVIOR- -AI LVL: %s- -%s- -BWATCHED: %s- -STATUS %s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.location.upper(), animatronic.beingWatched, animatronic.status, time.strftime("%H:%M:%S")))

    if Globals.debug == True:
        if animatronic == None:
            print("%s -%s- \n" % (text, time.strftime("%H:%M:%S")))
        else:
            print("%s -%s BEHAVIOR- -AI LVL: %s- -%s- -BWATCHED: %s- -STATUS %s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.location.upper(), animatronic.beingWatched, animatronic.status, time.strftime("%H:%M:%S")))
    return None


def cls(btimer=None, atimer=None):                                              # Before-cls time.sleep / After-cls time.sleep
    if btimer != None:
        time.sleep(btimer)

    if os.name == "nt":
        os.system("cls")

    elif os.name == "unix":
        os.system("clear")

    if atimer != None:
        time.sleep(atimer)

    return None

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
