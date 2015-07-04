import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def devgen():
    """ Creates Plone-Add-On-Skeletons of the commandline.
        
        Usage
        =====
        $ devgen [function_name] [argument] [path]
        
        Legend
        ======
        'function_name' : Required, can be any function's name you find in 'adi/devgen/scripts/skels.py'.
        'argument'      : Required, all functions expect at least one arg.
        'path'          : Optional, if not given 'here' is assumed (the dir where executed).
        Examples
        ========
        $ devgen addSkinsSkel example.addon     # create an addon
        $ devgen addDep mailtoplone.base        # register a dependency-addon
    """

    # For now, we assume at least two args and the most three args.

    function = None
    function_name = None
    argument = None
    path = '.'

    args = sys.argv                                 # get user's input as a list
    this_script_path = args.pop(0)                  # remove sys.argv's first default-arg
    if len(args) < 1:                               # no function-name provided
        exit(devgen.__doc__)                        # help: show this function's docstring
    else:                                           # a function-name is provided
        function_name = args.pop(0)                 # collect function-name
        function = getattr(AddSkel, function_name)  # get function of imported class by corresponding name

    if len(args) < 1:                               # no function-argument provided
        exit(getattr(function, '__doc__'))          # help: show the choosen function's docstring
    else:                                           # a function-argument is provided
        argument = args.pop(0)                      # collect function-argument

    if len(args) > 0:                               # there's still args left
        path = args.pop(0)                          # we assume it's the optional path-arg

    if len(args) > 0:                               # there's still args left
        exit('got more args than expected')         # something went wrong, abort


    getattr(AddSkel(), function_name)(argument, path)

#    amount_of_expected_arguments = len(inspect.getargspec(function)[0])

if __name__ == '__devgen__':                    # execute this script only of commandline, not of imports
    devgen()
