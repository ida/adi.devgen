import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def getFunctionsOfClass(class_):
    available_functions = []
    all_functions = dir(class_)
    for fun in all_functions:
        # Except built-in methods:
        if not fun.startswith('__'):
            available_functions.append(fun)
    return available_functions

def devgen():
    """
    Usage
    =====

    $ devgen [FUNCTION_NAME] [ARGUMENT_1] [ARGUMENT_2] ...

    Legend
    ======

    FUNCTION_NAME = Required. Can be any function-name present
                    in 'adi.devgen/adi/devgen/scripts/skels.py'

    ARGUMENT_X    = Depending on the choosen function, see help.

    Help
    ====

    Show the available functions of skels.py:
    
        $ devgen

    Show the expected arguments of a function:
    
        $ devgen [FUNCTION_NAME] help
"""

    defaults = None

    expected_args_amount = 0

    defaults_amount = 0

    required_args_amount = 0

    # Get user-input:
    args = sys.argv
    # Remove sys.argv's inbuilt first arg, of args:
    this_script_path = args.pop(0)                  

    # Get functions of AddSkel:
    available_functions = getFunctionsOfClass(AddSkel)

    # HELP
    # No argument was provided of user:
    if len(args) < 1:
        exit("\nAvailable functions:\n\n    " + ", ".join(available_functions) + ".\n\n\
Type `devgen [FUNCTION_NAME] help` to see the functions' docstr and which arguments it expects.\n\n\
Type `devgen help` to get a verbose description of this tool.\n")

    # At least one arg was passed, it must be the function-name:
    function_name = args.pop(0)
    # Unless it's the call for help, show this function's docstr and abort:
    if function_name == 'help': exit(devgen.__doc__)
    # Now, after removing funcname of args, get amount of rest of args:
    args_amount = len(args)

    # Passed function-name doesn't exist:
    if function_name not in available_functions:
        exit("\nThis function-name doesn't exist, maybe a typo? \
Try again, you can choose of these:\n\n" + ", ".join(available_functions) + ".\n")
    
    # GET FUNCTION:
    function = getattr(AddSkel, function_name)

    # GET ARGS:
    expected_args = inspect.getargspec(function)[0]
    if 'self' in expected_args: expected_args.remove('self')
    expected_args_amount = len(expected_args)
    if inspect.getargspec(function)[3]:
        defaults = list(inspect.getargspec(function)[3])

    # COMPUTE REQUIRED ARGS:
    if defaults:
        defaults_amount = len(defaults)
        required_args_amount = expected_args_amount - defaults_amount
    else:
        required_args_amount = expected_args_amount

    # PREP HELP-TXT:

    # First, add default vals to expected_args, if given:
    if defaults:
        i = 0
        while i > len(defaults)*-1:
            i -= 1
            new_arg  = expected_args[i] + "='" + defaults[i] + "'"
            expected_args[i] = new_arg

    # Get function, expected_args and docstr as one string:
    function_as_str = '    ' + function_name + '(' + ', '.join(expected_args) + '):'
    function_as_str += '\n        """' + getattr(function, '__doc__') + '"""'

    # Did user ask for help, concerning the function's expectations and usage?
    if args and args[0] == 'help':
        exit(function_as_str)

    # VALIDATE ARGS:

    # If less args than required or more args than expected were passed:
    if required_args_amount > args_amount or args_amount > expected_args_amount:
        helptxt = "\nThis didn't work out, less or more arguments are given, \
than expected. Try again:\n\n"
        # Show hlp-msg and abort:
        exit(helptxt + function_as_str)

    # If less args than expected were passed, append default-vals to args:
    if args_amount < expected_args_amount:
        missing_args_amount = expected_args_amount - args_amount
        passed_defaults_amount = args_amount - required_args_amount
        missing_defaults_amount = defaults_amount - passed_defaults_amount
        while missing_defaults_amount > 0:
            default_arg = defaults[passed_defaults_amount]
            args.append(default_arg)
            missing_defaults_amount -= 1
            passed_defaults_amount -= 1

    # EXECUTE FUNCTION OF PASSED FUNCTION-NAME:
    getattr(AddSkel(), function_name)(*args)

# ONLY EXECUTE THIS FUNCTION, WHEN TRIGGERED OF COMMANDLINE:
# Explanation: '__name__' of this function is '__devgen__', 
# unless executed of commandline, then it's '__main__'.
if __name__ == '__main__':
    devgen()

