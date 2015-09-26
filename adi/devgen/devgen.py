import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def devgen():
    """
    Create Plone-development-skeletons of the commandline.
    
    Usage:

        $ devgen [function_name] [argument(s)]

    To see which arguments a function expects, type:

        $ devgen [function_name]
"""

    available_functions = []

    expected_args_amount = 0

    defaults_amount = 0

    required_args_amount = 0


    # GET USER-INPUT:

    args = sys.argv

    # Remove sys.argv's inbuilt first and only arg (= not passed of user):
    this_script_path = args.pop(0)                  

    args_amount = len(args)

    # NO ARGS PASSED, SHOW HELP AND ABORT:

    if len(args) < 1:                               # No argument was provided of user,
        all_funcs = dir(AddSkel)                    # get functions of AddSkel,
        for fun in all_funcs:
            if not fun.startswith('__'):            # except built-in methods,
                available_functions.append(fun)     # collect all others, show them and this func's docstr, abort.
        exit(devgen.__doc__ + '\n\
    The available functions are:\n\n        ' + ', '.join(available_functions) + '\n\n')


    # GET FUNCTION OF PASSED FUNCTION-NAME:

    function_name = args.pop(0)                     # At least one arg was passed, it must be the function-name.
    function = getattr(AddSkel, function_name)      # Get function of AddSkel-class by corresponding name.


    # GET FUNCTION'S ARGS:

    expected_args = inspect.getargspec(function)[0]
    
    # Except self of expected arguments, user can't pass that one:
    if 'self' in expected_args: expected_args.remove('self')

    expected_args_amount = len(expected_args)
    
    defaults = inspect.getargspec(function)[3]


    # COMPUTE REQUIRED ARGS:

    if defaults:

        defaults_amount = len(defaults)

        required_args_amount = expected_args_amount - defaults_amount

    else:

        required_args_amount = expected_args_amount


    # VALIDATE PASSED ARGS:
    
    # If less args than required or more args than expected were passed:
    if required_args_amount > args_amount or args_amount > expected_args_amount:
        # Prep hlp-msg:
        helptxt = "\nThis didn't work out, less or more arguments are given, \
                   than expected, try again:\n\n    "
        # Include function-name, its expected args and default-vals in hlp-msg:
        helptxt += function_name + '(' + ', '.join(expected_args) + '):'
        # Include function's docstr in hlp-msg:
        helptxt += '\n        """' + getattr(function, '__doc__') + '"""'
        # Show hlp-msg and abort:
        exit(helptxt)

    # If less args than expected were passed, append default-vals to args:
    if args_amount < expected_args_amount:

        missing_args_amount = expected_args_amount - args_amount

        passed_defaults_amount = args_amount - required_args_amount

        missing_defaults_amount = defaults_amount - passed_defaults_amount

        while missing_defaults_amount > 0:

            default_arg = defaults[passed_defaults_amount]

            args.append(default_arg)

            missing_defaults_amount -= 1


    # EXECUTE CORRESPONDING FUNCTION OF PASSED FUNCTION-NAME:

    getattr(AddSkel(), function_name)(*args)


# EXECUTE THIS FUNCTION, WHEN TRIGGERED OF COMMANDLINE:
# Explanation: '__name__' of this function is '__devgen__', 
# unless executed of commandline, then it's '__main__'.
if __name__ == '__main__':
    devgen()

