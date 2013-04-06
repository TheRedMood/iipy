'''
The help system for iipy. Import this if you want to add stuff :D
Made by: TheRedMood <Teodor Spæren>
Date: 05-04-2013
'''
import iipy
from common import res
helpdb = {}

def setHelpdb():
    global helpdb
    helpdb = {}

    helpdb["info"]    = "Shows info about the bot."
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
    iipy.addCommand("info", res("This is a plugin written for the iipy program."))
    iipy.addCommand("version", res("0.01"))
    iipy.addCommand("help", helpcmd)
