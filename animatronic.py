import sys, time, os, random, time, location

debug = True

class animatronic():
    def __init__(self, name, slocation, alocation, kind, ailvl):
        self.name = name
        self.slocation = slocation #starting location
        self.alocation = alocation #actual location
        self.kind = kind #For now kinds should be "freddy, "bonnie", "foxy" and "chica"
        self.ailvl = ailvl #AI LVL, for future custom night
    
    def think(self): #Yeah. So I Don't know how to do the AI yet
        pass

    
testbot = animatronic("TestBot", 'testa', 'testa', None, 20)
