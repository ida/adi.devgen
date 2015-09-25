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

    required_args_amount = 0

    args = sys.argv                                 # Get user's input as a list, using sys.argv.

    this_script_path = args.pop(0)                  # Remove sys.argv's inbuilt first default-arg.

    # First aid:
    if len(args) < 1:                               # No argument was provided of user,
        usable_funcs = ''                           # get functions of AddSkel,
        all_funcs = dir(AddSkel)
        for fun in all_funcs:
            if not fun.startswith('__'):            # except built-in methods,
                usable_funcs += ' ' + fun           # collect all others, show them and this func's docstr, abort.
        exit(devgen.__doc__ + '\n\
    The available functions are:\n\n        ' + usable_funcs + '\n\n')

    # Get corresponding function and its expected arguments:
    function_name = args.pop(0)                     # At least one arg was passed, it must be the function-name.
    function = getattr(AddSkel, function_name)      # Get function of AddSkel-class by corresponding name.
    expected_args = inspect.getargspec(function)[0] # Get the function's expected arguments,
    if 'self' in expected_args:                     # except self-keyword of expected arguments,
        expected_args.remove('self')                # user can't pass that one ;)
    defaults = inspect.getargspec(function)[3]      # Get possible default-values.
    if defaults:                                    # Compute amount of required args.
        required_args_amount = len(expected_args) - len(defaults)
    else:
        required_args_amount = len(expected_args)

    # If user gave less args than expected, add default-vals to passed args:
    if required_args_amount > len(args):

        if defaults:

            i = 0

            while i*-1 < len(defaults):

                i -= 1                                          

                expected_args[i] = expected_args[i] + '="' + defaults[i] + '"'

            if len(args) < len(expected_args):

                missing_args = len(expected_args) - len(args)

                while missing_args > 0:

                    args.append(defaults[i])

                    missing_args -= 1

    # Compare expectations with given arguments:
    if len(expected_args) > len(args) or len(expected_args) < len(args):
        helptxt = "\nThis didn't work out, less or more arguments are given, than expected, try again:\n"
        helptxt += '\n     '
        helptxt += function_name + '(' + ', '.join(expected_args) + '):'
        helptxt += '\n        """' + getattr(function, '__doc__') + '"""'
        exit(helptxt)

    # Now, after validating user-input, finally execute the function:
    getattr(AddSkel(), function_name)(*args)

# Only execute this, if triggered of commandline:
# ('__name__' is '__devgen__', if executed of commandline it's '__main__')
if __name__ == '__main__':
    devgen()

