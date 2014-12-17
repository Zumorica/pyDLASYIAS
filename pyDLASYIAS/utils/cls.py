import os, sys, time
def cls(btimer=None, atimer=None): #Before-cls time.sleep / After-cls time.sleep
    if btimer != None:
        time.sleep(btimer)

    if os.name == "nt":
        os.system("cls")
        
    elif os.name == "unix":
        os.system("clear")

    if atimer != None:
        time.sleep(atimer)
