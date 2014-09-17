import os, sys, time, random, util

debug = 1

class location(object):
    def __init__(self, rname, adjacent):
        self.rname = rname
        self.adjacent = adjacent

testa = location("Room A", ['testb'])
testb = location("Room B", ['testa'])
