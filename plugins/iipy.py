import os
from os import path
import imp

# Embeded functions
import iipyemb

# Defining global variables
loaded_plugins = []
event_hooks = {"receive": {}, "spoke": {}, "msg": {}}
cmd_list = {}
CMDPRE = "@"
channel_list = []

# Config variables
OWNER = "TheRedMood"


# Objects
class ReceiveData(object):
    '''The data object for the receive events.'''
    def __init__(self, channel, date, nick, message):
        self.channel = channel
        self.date = date
        self.nick = nick
        self.message = message

        # Start the desicion making :;)
        if channel and channel[0] != "#":
            self.type = "msg"
            self.say = lambda s: send_msg(self.nick, s)
        else:
            self.type = "spoke"
            self.say = lambda s: send_msg(self.channel, s)


def load_plugin(name):
    ''' The plugin loader. It sorts out the loading of the object and so on.'''
    moduleobj = __import__(name)
    # I want it to be sourced and started here
    moduleobj.main()
    global loaded_plugins
    loaded_plugins.append(moduleobj)


# Reload them plugins!
def reload_plugins():
    for plugin in loaded_plugins:
        imp.reload(plugin)
        plugin.main()


# function that add events hooks
def event_add_hook(event, name, function):
    event_hooks[event][name] = function


def main():
    '''The main loader. It takes care of the setup rutines and such. '''
    # Load the diffrent events
    event_add_hook("receive", "ReceiveEvents", iipy_receive_events)

    for item in os.listdir("plugins/"):
        # Checking if the file is indeed a file suited for use
        if item in ['__pycache__', 'iipy.py', '__init__.py']:
            continue

        if item.split('.')[-1] == 'py':
            # The first part of your name should be the module name.
            # This would turn "testing.py" into ["testing", "py"] and then do
            # [0] on that.
            load_plugin(item.split('.')[0])


# Raw from C to python
def eventTriggered(*args):
    '''When an event is launched from C it is passed to this function. args is
       a tuple and the first element of it is always the name of the event. The
       rest of the elements depends on what even it is.'''
    # Loop trough the event_hooks if the event is there
    if not args[0] in event_hooks:
        return -1

    if len(args) >= 1:
        if args[0] == "receive":
            iipy_receive_events(*args[1:])


# From iipy to functions
def event_launcher(data):
    # Looping trough the elements
    for function in event_hooks[data.type].values():
        function(data)


# Finding the directory that a channel have.
def iipy_channeldir(channel):
    if not channel:
        return iipyemb.getPath()

    return path.join(iipyemb.getPath(), channel.lower())


# Send message to in file :)
def send_msg(channel, message):
    infile = path.join(iipy_channeldir(channel), "in")
    if not path.exists(infile):
        return -1

    with open(infile, "w", encoding="utf-8") as file:
        file.write(message + "\n")

    return 0


def add_command(cmd, func):
    cmd_list[cmd] = func


# Handling of commands.... Still very messy.
def handle_cmd(data):
    # Checking commands
    if data.message[0] == CMDPRE:
        # Check if the command is in there
        if data.message[1:].split(" ")[0] in cmd_list:
            data.flags = data.message[1:].split(" ")
            cmd_list[data.flags.pop(0)](data)

    elif data.type == "msg":
        if data.message.split(" ")[0] in cmd_list:
            data.flags = data.message.split(" ")
            cmd_list[data.flags.pop(0)](data)


# This is the only place you can get commands from.
def iipy_receive_events(channel, date, nick, message):
    # Channel may be of type None
    if not channel:
        channel = ""

    # Create the event.
    data = ReceiveData(channel, date, nick, message)

    # Check for commands
    handle_cmd(data)

    # Handle the event.
    event_launcher(data)


# Convinient functions
def join_channel(channel):
    global channel_list
    if not channel in channel_list:
        send_msg("", "/j {0}".format(channel))
        channel_list.append(channel)


# Use these two channels to
def leave_channel(channel):
    global channel_list
    if channel in channel_list:
        send_msg(channel, "/l {0}".format(channel))
        channel_list.remove(channel)


# message user
def msg_user(user, message):
    if send_msg(user, message) == -1:
        join_channel(user)
        send_msg(user, message)


def do(channel, action):
    send_msg(channel, "\x01ACTION {0}\x01".format(action))
