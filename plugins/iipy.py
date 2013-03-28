import os

# Defining global variables
loaded_plugins = []
EventHooks = {"spoke": {}, "msg": {}}


def load_plugin(name):
    ''' The plugin loader. It sorts out the loading of the object and so on.'''
    moduleobj = __import__(name)
    # I want it to be sourced and started here
    moduleobj.main()
    loaded_plugins.append(moduleobj)


def main():
    '''The main loader. It takes care of the setup rutines and such. '''
    # Just testing.
    print(iiHOST)
    # Start by loading the plugins
    for item in os.listdir("plugins/"):
        # Checking if the file is indeed a file suited for use
        if item not in ['__pycache__', 'iipy.py', '__init__.py'] and item.split('.')[-1] == 'py':
            # The first part of your name should be the module name.
            # This would turn "testing.py" into ["testing", "py"] and then do
            # [0] on that.
            load_plugin(item.split('.')[0])


# Function that adds event hooks
def eventAddHook(event, name, function):
    EventHooks[event][name] = function


def eventTriggered(*args):
    '''When an event is launched from C it is passed to this function. args is
       a tuple and the first element of it is always the name of the event. The
       rest of the elements depends on what even it is.'''
    # Loop trough the EventHooks if the event is there
    if not EventHooks.__contains__(args[0]):
        return 0;


    for _, hfunc in EventHooks[args[0]].items():
        # Checking to see if there are any events here
        if len(args) >= 1:
            hfunc(*args[1:])
        else:
            hfunc()

