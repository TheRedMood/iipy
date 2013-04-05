'''
Name: common.py
Author: TheRedMood <Teodor Spæren>
Date: 05.04.2013
Desc:
    This is a set of functions commonly found in other bots.
'''
import iipy
import help

# Reload function
def reloadcmd(ii):
    iipy.reloadPlugin()
    ii.say("Plugins reloaded.")


def main():
    # Reload
    iipy.addCommand("reload", reloadcmd)
    help.addHelp("reload", "Reload the plugins.")
    
    # Ping
    iipy.addCommand("ping", lambda x: x.say("{0}: Pong.".format(x.nick)))
    help.addHelp("ping", "Simple delay test.")
