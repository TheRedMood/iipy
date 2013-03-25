import os


# Defining global variables
loaded_plugins = []
events = {"spoke": {}, "msg": {}}


def iievent_add(event, name, function):
    events[event][name] = function


def iiplugins_show():
    for event, hooks in events.items():
        print("{0}: {1}".format(event, hooks))


def load_plugin(name):
    ''' The plugin loader. It sorts out the loading of the object and so on.'''
    moduleobj = __import__(name)

    # I want it to be sourced and started here
    moduleobj.main()
    loaded_plugins.append(moduleobj)


def main():
    '''The main loader. It takes care of the setup rutines and such. '''
    # Start by loading the plugins
    for item in os.listdir("plugins/"):
        # Checking if the file is indeed a file suited for use
        if item not in ['__pycache__', 'manager.py', '__init__.py'] and item.split('.')[-1] == 'py':
            # The first part of your name should be the module name
            # This would turn "testing.py" into ["testing", "py"] and then do
            # [0] on that.
            load_plugin(item.split('.')[0])
