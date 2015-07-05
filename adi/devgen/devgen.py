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
        'argument'      : Optional, if the functions expects more args than 'self' and 'path'.
        'path'          : Optional, if not given, it is assumed, you execute devgen in an addon, defaults to '.'

        Examples
        ========
        $ devgen addSkinsSkel example.addon     # create an addon
        $ devgen addDep mailtoplone.base        # register a dependency-addon
    """

    path = '.'

    function = None
    function_name = None
    argument = None

    # GET FUNCTION

    args = sys.argv                                 # get user's input as a list, using sys.argv
    this_script_path = args.pop(0)                  # remove sys.argv's inbuilt first default-arg
    this_script_name = this_script_path.split('/')[-1]  # extract name of it

    if len(args) < 1:                               # no function-name provided
        exit(this_script_name.__doc__)              # show this function's docstring and abort
    else:                                           # a function-name is provided
        function_name = args.pop(0)                 # collect function-name
        function = getattr(AddSkel, function_name)  # get function of imported class by corresponding name

    # COMPARE ARGS
    
    # What does the func expect?
    expected_args = inspect.getargspec(function)[0]
    # Remove 'self', user cannot pass that one :)
    if 'self' in expected_args: expected_args.remove('self')

    if len(args) < len(expected_args)-1:            # not enough args passed
            exit(getattr(function, '__doc__'))      # show the choosen function's docstring and abort

    if len(expected_args) > 1:                      # more than a path expected
        argument = args.pop(0)                      # next passed arg must be the argument for the function

    if len(args) > 0:                               # if there's still an arg
        path = args.pop(0)                          # it must be the path


    # EXECUTE FUNCTION
    
    if len(expected_args) > 1:                              # more than a path expected
        getattr(AddSkel(), function_name)(path, argument)   # execute corresponding func with arg
    else:                                                   # only a path expected
        getattr(AddSkel(), function_name)(path)             # execute corresponding func without arg

if __name__ == '__devgen__':    # only, if this script is executed,
    devgen()                    # execute this function, not if imported
