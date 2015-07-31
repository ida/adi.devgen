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

    path = '.'                                      # default-value
    args = sys.argv                                 # get user's input as a list, using sys.argv
    this_script_path = args.pop(0)                  # remove sys.argv's inbuilt first default-arg
    # FIRST AID
    if len(args) < 1:                               # no argument provided of user
        print '\n\
Choose one of the function-names listed below and type "devgen [function_name]"\n\
to see, what it does and expects. Alternatively type "devgen help"\n\
to get a more verbose description of this tool.\n'  # help
        funks = ''
        funcs = dir(AddSkel)                        # get functions of AddSkel
        for fun in funcs:                           # for each one
            if not fun.startswith('__'):            # except built-in methods
                funks += ' ' + fun                  # collect all others
        exit(funks + '\n\n')                        # show them and abort
    if args[0] == 'help':                           # at least one arg was passed, it's the help-keyword
        exit(devgen.__doc__)                        # show this function's docstring and abort
    # GET FUNCTION                                  # at least one argument was passed by user
    function_name = args.pop(0)                     # it's not the help-keyword, so must be the function-name
    function = getattr(AddSkel, function_name)      # get function of AddSkel-class by corresponding name
    # GET EXPECTATION
    expected_args = inspect.getargspec(function)[0] # get the function's expected arguments
    if 'self' in expected_args:                     # except self-keyword of expected arguments,
        expected_args.remove('self')                # user can't pass that one ;)
    if len(args) == len(expected_args)-1:           # user omitted passing a path
        args.append(path)                           # add default-path to args
    # MET EXPECTATION?
    if len(args) != len(expected_args):             # still, less or more args are given than expected
        exit(getattr(function, '__doc__'))          # show the choosen function's docstring and abort
    # EXECUTE FUNCTION
    getattr(AddSkel(), function_name)(*args)

if __name__ == '__devgen__':    # only, if this script is executed,
    devgen()                    # execute devgen only of commandline not, if imported
