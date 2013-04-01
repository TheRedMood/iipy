import iipy

def testlol(channel, date, nick, message):
    print("Channel: {0}, Date: {1}, Nick: {2}, Message: {3}".format(channel, date, nick, message))

def simplecmd(channel, date, nick, message):
    if message == "!help":
        iipy.Message(channel, "You asked for help?")

def main():
    iipy.eventAddHook("spoke", "testlol", testlol)
    iipy.eventAddHook("spoke", "simplecmd", simplecmd)
