def init():
    global animatronics, camdic, adjcam, debug, m, version, log, BLACK, RED, GREEN, BLUE, WHITE

    version = "v0.5-alpha (GUI)"

    debug = True #Debug variable. If set to true, prints debug info into the console.

    animatronics = [] #A list for all the animatronics. They auto-append themselves to this list.

    camdic = {"cam1a" : "Stage Show", #A list containing cameras and their names.
              "cam1b" : "Dinning Area",
              "cam1c" : "Pirate Cove",
              "cam2a" : "West Hall",
              "cam2b" : "West Hall Corner",
              "cam3" : "Supply Closet",
              "cam4a" : "East Hall",
              "cam4b" : "East Hall Corner",
              "cam5" : "Backstage",
              "cam6" : "Kitchen -Camera Disabled- (AUDIO ONLY)",
              "cam7" : "Restrooms"}

    adjcam = {"cam1a" : ["cam1b"], #A list containing cameras and their adjacent cameras.
              "cam1b" : ["cam1a", "cam1c", "cam5", "cam6", "cam7", "cam2a", "cam4a"],
              "cam5" : ["cam1b"],
              "cam6" : ["cam1b"],
              "cam7" : ["cam1b"],
              "cam2a" : ["cam2b", "cam3"],
              "cam3" : ["cam2a"],
              "cam2b" : ["inside", "cam2a"],
              "cam4a" : ["cam1b", "cam4b"],
              "cam4b" : ["cam4a", "inside"]}

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)


if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
