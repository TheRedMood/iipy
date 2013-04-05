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

# Objects
class receiveData(object):
    '''The data object for the receive events '''
    def __init__(self, channel, date, nick, message): 
        self.channel = channel
        self.date = date
        self.nick = nick
        self.message = message

        # Start the desicion making :;)
        if channel != "" and channel[0] != "#":
            self.type = "msg"
            self.say = lambda s: Message(self.nick, s)
        else:
            self.type = "spoke"
            self.say = lambda s: Message(self.channel, s)
    
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


# Raw from C to python
def eventTriggered(*args):
    '''When an event is launched from C it is passed to this function. args is
       a tuple and the first element of it is always the name of the event. The
       rest of the elements depends on what even it is.'''
    # Loop trough the EventHooks if the event is there
    if not args[0] in EventHooks:
        return -1
   
    if len(args) >= 1:
        if args[0] == "receive":
            iipy_ReceiveEvents(*args[1:])


# From iipy to functions
def eventBroadcaster(data):
    # Looping trough the elements
    for function in EventHooks[data.type].values():
        function(data)


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


def handleCommand(data):
    # Checking commands
    if data.message[0] == cmdpre:
        # Check if the command is in there
        if data.message[1:].split(" ")[0] in cmdList:
            data.flags = data.message[1:].split(" ")
            cmdList[data.flags.pop(0)](data)


# Defining the msg and spoke events.  # This is the only place you can get commands from.
def iipy_ReceiveEvents(channel, date, nick, message):
    # Channel may be of type None
    if not channel: channel = ""
    
    # Create the event.
    data = receiveData(channel, date, nick, message)

    # Check for commands 
    handleCommand(data)

    # Handle the event.
    eventBroadcaster(data)


# Convinient functions
def joinChannel(channel):
    Message("", "/j {0}".format(channel))


def msgUser(user, message):
    if Message(user, message) == -1:
        joinChannel(user)
        Message(user, message)

