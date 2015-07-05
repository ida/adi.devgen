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

    path = '.'                                      # if user didn't specify, we assume to be in the addon

    function = None                                 # try to find these three vars in the following
    function_name = None
    argument = None

    args = sys.argv                                 # get user's input as a list, using sys.argv
    this_script_path = args.pop(0)                  # remove sys.argv's inbuilt first default-arg
    this_script_name = this_script_path.split('/')[-1]  # extract name of it

    if len(args) < 1:                               # no function-name provided
        exit(this_script_name.__doc__)              # show this function's docstring and abort
    else:                                           # a function-name is provided
        function_name = args.pop(0)                 # collect function-name
        function = getattr(AddSkel, function_name)  # get function of imported class by corresponding name


    if len(args) > 0:
        path = args.pop(0)
    if len(args) > 0:
        argument = args.pop(0)
#            getattr(AddSkel(), function_name)(path, argument)

    expected_args = inspect.getargspec(function)[0]
    if len(expected_args) == 2:                             # expected are 'self' and 'path'
        getattr(AddSkel(), function_name)(path)             # execute corresponding func
    elif len(expected_args) == 3:                           # expected are 'self', 'path' and one more arg
        if not argument:
            exit(getattr(function, '__doc__'))              # show the choosen function's docstring and abort
        getattr(AddSkel(), function_name)(path, argument)   # execute corresponding func

if __name__ == '__devgen__':                    # execute this script only of commandline, not of imports
    devgen()
