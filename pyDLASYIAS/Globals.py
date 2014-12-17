def init():
    global animatronics, camdic, adjcam, debug

    debug = False

    animatronics = []

    camdic = {"cam1a" : "Stage Show",
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

    adjcam = {"cam1a" : ["cam1b"],
              "cam1b" : ["cam1a", "cam1c", "cam5", "cam6", "cam7", "cam2a", "cam4a"],
              "cam5" : ["cam1b"],
              "cam6" : ["cam1b"],
              "cam7" : ["cam1b"],
              "cam2a" : ["cam2b", "cam3"],
              "cam3" : ["cam2a"],
              "cam2b" : ["inside", "cam2a"],
              "cam4a" : ["cam1b", "cam4b"],
              "cam4b" : ["cam4a", "inside"]}
