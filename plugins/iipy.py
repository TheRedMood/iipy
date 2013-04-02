import os
from os import path
import imp

# Embeded functions
import iipyemb

# Defining global variables
loaded_plugins = []
EventHooks = {"receive": {}, "spoke": {}, "msg": {}}
cmdList = {}
cmdpre = "@"

def load_plugin(name):
    ''' The plugin loader. It sorts out the loading of the object and so on.'''
    moduleobj = __import__(name)
    # I want it to be sourced and started here
    moduleobj.main()
    global loaded_plugins
    loaded_plugins.append(moduleobj)

# Reload them plugins!
def reloadPlugin():
    for plugin in loaded_plugins:
        imp.reload(plugin)
        plugin.main()

# function that add events hooks
def eventAddHook(event, name, function):
    EventHooks[event][name] = function

def main():
    '''The main loader. It takes care of the setup rutines and such. '''
    # Load the diffrent events
    eventAddHook("receive", "ReceiveEvents", iipy_ReceiveEvents)
   
    for item in os.listdir("plugins/"):
        # Checking if the file is indeed a file suited for use
        if item not in ['__pycache__', 'iipy.py', '__init__.py'] and item.split('.')[-1] == 'py':
            # The first part of your name should be the module name.
            # This would turn "testing.py" into ["testing", "py"] and then do
            # [0] on that.
            load_plugin(item.split('.')[0])
    
def eventTriggered(*args):
    '''When an event is launched from C it is passed to this function. args is
       a tuple and the first element of it is always the name of the event. The
       rest of the elements depends on what even it is.'''
    # Loop trough the EventHooks if the event is there
    if not args[0] in EventHooks:
        return -1;
    
    # Looping trough the elements
    for hfunc in EventHooks[args[0]].values():
        # Checking to see if there are any events here
        if len(args) >= 1:
            hfunc(*args[1:])
        else:
            hfunc()


# Finding the directory that a channel have.
def iipy_ChannelDir(channel):
    if channel == "":
        return iipyemb.getPath()

    return path.join(iipyemb.getPath(), channel.lower())


# Send message to in file :)
def Message(channel, message):
    infile = path.join(iipy_ChannelDir(channel), "in")
    if not path.exists(infile):
        return -1

    with open(infile, "w", encoding="utf-8") as file:
        file.write(message + "\n")
    return 0


def addCommand(cmd, func):
    cmdList[cmd] = func


def handleCommand(message, args):
    # Checking commands
    if message[0] == cmdpre:
        # Check if the command is in there
        if message[1:].split(" ")[0] in cmdList:
            parts = message[1:].split(" ")
            if len(parts) >= 2:
                cmdList[parts[0]](*args, flags=parts[1:])
            else:
                cmdList[parts[0]](*args)


# Defining the msg and spoke events.  # This is the only place you can get commands from.
def iipy_ReceiveEvents(channel, date, nick, message):
    # Channel may be of type None
    if not channel:
        channel = ""
    
    # Handle commands
    handleCommand(message, (channel, date, nick, message))

    if channel != "" and channel[0] != "#":
        eventTriggered("msg", date, nick, message)
    else:
        eventTriggered("spoke", channel, date, nick, message)

# Convinient functions
def joinChannel(channel):
    Message("", "/j {0}".format(channel))

def msgUser(user, message): 
    if Message(user, message) == -1:
        joinChannel(user)
        Message(user, message)

