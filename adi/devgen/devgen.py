import sys
import inspect
from adi.devgen.scripts.skels import AddSkel

def devgen():
    """ Creates Plone-Add-On-Skeletons of the commandline.
        
        Usage
        =====
        $ devgen [function_name] [argument]
        
        Legend
        ======
        'function_name' : Required, can be any function's name you find in 'adi/devgen/scripts/skels.py'.
        'argument':       Optional, provided for additional parameters, such as a name.
        
        Examples
        ========
        $ devgen addSkinsSkel example.addon     # create an addon
        $ devgen addDep mailtoplone.base        # register a dependency-addon
    """

    if len(sys.argv) < 2:                       # no function-name provided
        exit(sys.argv[0] + devgen.__doc__)      # show this function's docstring
    else:
        function = sys.argv[1]
        method = getattr(AddSkel, function)     # get corresponding function of class

    amount_of_expected_arguments = len(inspect.getargspec(method)[0])
    argument = None
    if amount_of_expected_arguments > 2:
        if len(sys.argv) < 3:                   # no argument provided
            print inspect.getargspec(method)
            exit(getattr(method, '__doc__'))    # show the choosen function's docstring
        else:
            argument = sys.argv[2]
    else:
        argument = '.'
    getattr(AddSkel(), function)(argument)      # execute function


if __name__ == '__devgen__':                    # execute this script only of commandline, not of imports
    devgen()
