import cx_Freeze as cx

executables = [cx.Executable("game.py")]

cx.setup(name="pyDLASYIAS", options={"build_exe": {"packages":["cocos", "pyglet"], "includes":["pygame.mixer"]}}, executables = executables)
