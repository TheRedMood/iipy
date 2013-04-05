'''
The help system for iipy. Import this if you want to add stuff :D
Made by: TheRedMood <Teodor Spæren>
Date: 05-04-2013
'''
import iipy
helpdb = {}

def setHelpdb():
    global helpdb
    helpdb = {}

    helpdb["info"]    = "I am a plugin for the iipy program."
    helpdb["version"] = "Print the iipy version."

def addHelp(name, desc):
    global helpdb
    helpdb[name] = desc

def helpcmd(ii):
    if not ii.flags or not (ii.flags[0].lower() in helpdb):
        ii.say("{0}".format(list(helpdb.keys())))
    else:
        ii.say("{0}".format(helpdb[ii.flags[0].lower()]))

def helpfuncs(topic):
    if topic.lower() in helpdb:
        return lambda x: x.say(helpdb[topic])

    # if that fails
    return lambda x: x.say("There is no info about \"{0}\"".format(topic))


def main():
    setHelpdb()
    iipy.addCommand("info", helpfuncs("info"))
    iipy.addCommand("version", helpfuncs("version"))
    iipy.addCommand("help", helpcmd)
