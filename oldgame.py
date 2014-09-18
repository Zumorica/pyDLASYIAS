import os, sys, time, random, util

#dear me from the future: I'm sorry

class location(object):
    def __init__(self, rname, adyacent):
        self.rname = rname
        self.adyacent = adyacent
        self.rndomval = 123 #debug

    def accessAdyacent(self): #debugging
        exec "%s.rndomval = 2" % (self.adyacent)


class animatronic(object):
    def __init__(self, name, slocation, ailvl=5, alocation=None):
        self.name = name
        self.slocation = slocation #starting location
        self.alocation = slocation #actual location
        self.ailvl = int(ailvl) #For use in custom night, etc

    def debugMove(self, room): #magic --debug--
        self.alocation = room
        util.debugprnt("Moved to %s" % (self.alocation))

    def cthink(self):
        if random.randint(0, 50) in range(0, self.ailvl):
            exec "self.choose = random.choice(%s.adyacent)" % (str(self.alocation))
            util.debugprnt("Choose is %s" % (self.choose))
            print "test"
            util.debugprnt("Actual location %s" % (self.alocation))
        else:
            time.sleep(10)
            self.cthink()



rooma = location("test room A", "roomb")
roomb = location("test room B", "rooma")
rooma.accessAdyacent()

chica = animatronic("Chica", roomb, 20)
chica.cthink()

