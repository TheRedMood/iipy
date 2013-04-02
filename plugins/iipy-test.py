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

def testlol(channel, date, nick, message):
    print("Channel: {0}, Date: {1}, Nick: {2}, Message: {3}".format(channel, date, nick, message))

def helpcmd(channel, date, nick, message, flags=()):
    if flags == () or not flags[0].lower() in helpdb:
        iipy.Message(channel, "You asked for help?")
    
    iipy.Message(channel, "{0}".format(helpdb[flags[0].lower()]))

def reloadcmd(channel, date, nick, message, flags=()):
    iipy.reloadPlugin()
    iipy.Message(channel, "Plugins reloaded.")

def donottalk(date, nick, message):
    iipy.Message(nick, "Your nick is: {0} and you talked to me.".format(nick))


def main():
    setHelpdb()
    iipy.eventAddHook("spoke", "testlol", testlol)
    iipy.eventAddHook("msg", "donottalk", donottalk)
    
    iipy.addCommand("help", helpcmd)
    iipy.addCommand("reload", reloadcmd)
