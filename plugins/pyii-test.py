import iipy

def testlol(channel, message):
    print("Channel: {0}, Message: {1}".format(channel, message))

def main():
    print("Test loaded!")
    iipy.eventAdd("spoke", "testlol", testlol)
