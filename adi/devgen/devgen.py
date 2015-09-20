import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def devgen():
    """
Create Plone-Add-On-Skeletons of the commandline. Usage is:

    $ devgen [function_name] [argument(s)]

To see which arguments a function expects, type:

    $ devgen [function_name]
"""

    path = '.'                                      # default-value

    args = sys.argv                                 # get user's input as a list, using sys.argv

    this_script_path = args.pop(0)                  # remove sys.argv's inbuilt first default-arg

    if len(args) < 1:                               # no argument provided of user
        usable_funcs = ''                           # get functions of AddSkel
        all_funcs = dir(AddSkel)
        for fun in all_funcs:
            if not fun.startswith('__'):            # except built-in methods
                usable_funcs += ' ' + fun           # collect all others, show them and this func's docstr, abort
        exit(devgen.__doc__ + '\n\
The available functions are:\n\n   ' + usable_funcs + '\n\n')

    function_name = args.pop(0)                     # at least one arg was passed, it must be the function-name
    function = getattr(AddSkel, function_name)      # get function of AddSkel-class by corresponding name
    expected_args = inspect.getargspec(function)[0] # get the function's expected arguments
    if 'self' in expected_args:                     # except self-keyword of expected arguments,
        expected_args.remove('self')                # user can't pass that one ;)

    if len(args) == len(expected_args)-1:           # user omitted passing a path
        args.append(path)                           # add default-path to args

    if len(args) != len(expected_args):             # still, less or more args are given than expected
        docstr = getattr(function, '__doc__')
        helptxt = '\n    This function expects, these arguments: \n    ' + ' '.join(expected_args) + '\n    , please try again.\n' + docstr
        exit(helptxt)                               # help and abort

    getattr(AddSkel(), function_name)(*args)        # everything went well, we've come this far, now exe func

# '__name__' is '__devgen__',
# unless executed of commandline,
# then Python turns '__name__' to '__main__'
if __name__ == '__main__':
    devgen()

