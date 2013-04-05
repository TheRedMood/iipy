import iipy
helpdb = {}

def setHelpdb():
    global helpdb
    helpdb = {}
    helpdb["info"] = "I am a plugin for the iipy program."
    helpdb["version"] = "0.001"
    helpdb["reload"] = "Reload the plugins."

    # Make sure that this is the last item
    helpdb["topics"] = list(helpdb.keys()) + ['topics']

def testlol(data):
    print("Channel: {0}, Date: {1}, Nick: {2}, Message: {3}".format(data.channel, data.date, data.nick, data.message))

def helpcmd(ii):
    if not ii.flags or not (ii.flags[0].lower() in helpdb):
        ii.say("{0}".format(helpdb["topics"]))
    else:
        ii.say("{0}".format(helpdb[ii.flags[0].lower()]))

def reloadcmd(data):
    iipy.reloadPlugin()
    data.say("Plugins reloaded.")

def donottalk(data):
    data.say("Your nick is: {0} and you talked to me.".format(data.nick))

def main():
    setHelpdb()
    iipy.eventAddHook("spoke", "testlol", testlol)
    iipy.eventAddHook("msg", "donottalk", donottalk)

    iipy.addCommand("help", helpcmd)
    iipy.addCommand("reload", reloadcmd)
