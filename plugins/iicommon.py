'''
Name: common.py
Author: TheRedMood <Teodor Spæren>
Date: 05.04.2013
Desc:
    This is a set of functions commonly found in other bots.
'''
import iipy
import iihelp


# Reload function
def reloadcmd(ii):
    if ii.nick == iipy.owner:
        iipy.reloadPlugin()
        ii.say("Plugins reloaded.")
    else:
        ii.say("You don't got the permission to do that.")


# Command to join a channel
def joincmd(ii):
    if ii.nick == iipy.owner and ii.flags:
        iipy.joinChannel(ii.flags[0])
    else:
        ii.say("You don't got the permission to do that.")


# Command to leave a channel
def partcmd(ii):
    if ii.nick == iipy.owner and ii.flags:
        iipy.leaveChannel(ii.flags[0])
    else:
        ii.say("You don't got the permission to do that.")


# List channels.
def listchannels(ii):
    ii.say(str(iipy.channelList))


# Abstraction layer for simple responses
def res(msg):
    return lambda x: x.say(msg)


def main():
    # Reload
    iipy.addCommand("reload", reloadcmd)
    iihelp.addHelp("reload", "Reload the plugins.")

    # join
    iipy.addCommand("join", joincmd)
    iihelp.addHelp("join", "Have the bot join channels.")

    # part
    iipy.addCommand("part", partcmd)
    iihelp.addHelp("part", "Leave a channel specified by the first argument.")

    # list channels
    iipy.addCommand("list", listchannels)
    iihelp.addHelp("list", "List the current active channels")

    # Ping
    iipy.addCommand("ping", lambda x: x.say("{0}: Pong.".format(x.nick)))
    iihelp.addHelp("ping", "Simple delay test.")
