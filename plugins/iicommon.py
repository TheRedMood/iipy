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
    if ii.nick == iipy.OWNER:
        iipy.reload_plugins()
        ii.say("Plugins reloaded.")
    else:
        ii.say("You don't got the permission to do that.")


# Command to join a channel
def joincmd(ii):
    if ii.nick == iipy.OWNER and ii.flags:
        iipy.join_channel(ii.flags[0])
    else:
        ii.say("You don't got the permission to do that.")


# Command to leave a channel
def partcmd(ii):
    if ii.nick == iipy.OWNER and ii.flags:
        iipy.leave_channel(ii.flags[0])
    else:
        ii.say("You don't got the permission to do that.")


# List channels.
def listchannels(ii):
    ii.say(str(iipy.channel_list))


# Abstraction layer for simple responses
def res(msg):
    return lambda x: x.say(msg)


def main():
    # Reload
    iipy.add_command("reload", reloadcmd)
    iihelp.add_help("reload", "Reload the plugins.")

    # join
    iipy.add_command("join", joincmd)
    iihelp.add_help("join", "Have the bot join channels.")

    # part
    iipy.add_command("part", partcmd)
    iihelp.add_help("part", "Leave a channel specified by the first argument.")

    # list channels
    iipy.add_command("list", listchannels)
    iihelp.add_help("list", "List the current active channels")

    # Ping
    iipy.add_command("ping", lambda x: x.say("{0}: Pong.".format(x.nick)))
    iihelp.add_help("ping", "Simple delay test.")
