import iipy

def testlol(channel, date, nick, message):
    print("Channel: {0}, Date: {1}, Nick: {2}, Message: {3}".format(channel, date, nick, message))

def simplecmd(channel, date, nick, message, flags=()):
    iipy.Message(channel, "You asked for help?")


def donottalk(date, nick, message):
    iipy.Message(nick, "Your nick is: {0} and you talked to me.".format(nick))


def main():
    iipy.eventAddHook("spoke", "testlol", testlol)
    iipy.eventAddHook("msg", "donottalk", donottalk)
    
    iipy.addCommand("help", simplecmd)
