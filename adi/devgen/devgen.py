import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def devgen():
    """
        Create Plone-Add-On-Skeletons of the commandline.

        Usage
        =====
        $ devgen [function_name] [argument(s)] [path]
        
        Legend
        ======
        'function_name' : Required, can be any function's name you find in 'adi/devgen/scripts/skels.py'.
        'argument'      : Optional, if the functions expects more arguments, than only the function-name.
        'path'          : Optional, if not given, it is assumed, you execute devgen in an addon, defaults to '.'

        Examples
        ========
        $ devgen addSkinsSkel example.addon     # create an addon with a skins-folder
        $ devgen addDep mailtoplone.base        # register a dependency-addon

        Help
        ====
        To see, which arguments a function expects, type:

        $ devgen [function_name]

    """

    path = '.' # default-value

    function = None
    function_name = None
    argument = None

    # Get passed arguments of user:

    args = sys.argv                                 # get user's input as a list, using sys.argv
    this_script_path = args.pop(0)                  # remove sys.argv's inbuilt first default-arg

    if len(args) < 1:                               # no function-name provided of user
        print '\n\
Choose one of the function-names listed below and type "devgen [function_name]"\n\
to see, what it does and expects. Alternatively type "devgen help"\n\
to get a more verbose description of this tool.\n'
        funks = ''
        funcs = dir(AddSkel)
        for fun in funcs:
            if not fun.startswith('__'):            # except built-in methods
#                if fun.find('Skel') != -1:          # show only skel-methods, for now
                funks += ' ' + fun
        print funks + '\n\n'
        exit()                                      # abort


    else:                                           # a function-name is provided
        function_name = args.pop(0)                 # collect function-name
        if function_name == 'help':                 # user asked for help
            exit(devgen.__doc__)                    # show this function's docstring and abort

        function = getattr(AddSkel, function_name)  # get function of imported class by corresponding name

    # COMPARE ARGS
    
    expected_args = inspect.getargspec(function)[0] # get the function's expected arguments

    if 'self' in expected_args:                     # except self-keyword of expected arguments,
        expected_args.remove('self')                # user can't pass that one ;)

    if len(args) < len(expected_args)-1:            # not enough args passed, -1 excepts the optional path
            exit(getattr(function, '__doc__'))      # show the choosen function's docstring and abort

    if len(expected_args) > 1:                      # more than a path expected
        argument = args.pop(0)                      # next passed arg must be the argument for the function

    if len(args) > 0:                               # if there's still an arg
        path = args.pop(0)                          # it must be the path


    # EXECUTE FUNCTION
    
    if len(expected_args) > 1:                              # more than a path expected
        getattr(AddSkel(), function_name)(argument, path)   # execute corresponding func with arg
    else:                                                   # only a path expected
        getattr(AddSkel(), function_name)(path)             # execute corresponding func without arg

if __name__ == '__devgen__':    # only, if this script is executed,
    devgen()                    # execute devgen only of commandline not, if imported
