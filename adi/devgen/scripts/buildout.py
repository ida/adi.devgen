# Any buildout-related methods should live here.
# We'll call add-ons eggs here, for better distinction from the addon-generator-methods.

import glob

from adi.commons.commons import fileExists
from adi.commons.commons import fileHasStr
from adi.commons.commons import getLines
from adi.commons.commons import insertAfterLine 
from adi.commons.commons import removeLinesContainingPattern 
from adi.commons.commons import read 

from adi.devgen.scripts.conventions import getEggCachePaths


def addAddonToScript(addon_path, script_path):
    """Insert addon_path after occurence of 'sys.path[0:0] = [' in script."""
    new_lines = []
    if not fileHasStr(script_path, "'" + addon_path + "',"):
        insertAfterLine(script_path,
                        'sys.path[0:0] = [',
                        "  '" + addon_path + "',\n")

def addAddonToBuildoutConfig(addon_path, instance_path, config_name='buildout'):
    """
    Expects the config in instance_path, expects an eggs-
    and a develop-section in it, adds the addon to it.
    """
    DEVELOP_ADDON = False
    PATTERN_FOUND = False
    buildout_config_path = instance_path + config_name + '.cfg'
    if addon_path.endswith('/'): addon_path = addon_path[:-1]
    addon_name = addon_path.split('/')[-1]
    if fileHasStr(buildout_config_path, addon_name):
        exit('The addon seems to be registered already, \
please check your buildout.cfg')
    # It's a stable-egg, get the addon_name only:
    if addon_name.endswith('.egg'):
        addon_name = addon_name.split('-')[0]
    # It's a develop-egg, we need an entry in the develop-section:
    else:
        patterns = ['develop =', 'develop=', 'develop +=', 'develop+=']
        for pattern in patterns:
            if fileHasStr(buildout_config_path, pattern):
                PATTERN_FOUND = True
                addon_path = '    ' + addon_path + '\n'
                insertAfterLine(buildout_config_path, pattern, addon_path)
        if not PATTERN_FOUND:
            exit('No develop-section found in buildout, \
aborting now, nothing changed.')
        else: PATTERN_FOUND = False # reset for next block

    # In any case add addon to eggs-section:
    patterns = ['eggs =', 'eggs=', 'eggs +=', 'eggs+=']
    for pattern in patterns:
        if fileHasStr(buildout_config_path, pattern):
            PATTERN_FOUND = True
            addon_name = '    ' + addon_name + '\n'
            insertAfterLine(buildout_config_path, pattern, addon_name)
    if not PATTERN_FOUND:
        if DEVELOP_ADDON:
            exit('No eggs-section found in buildout, \
aborting now. Add-on was added to develop-section.')
        else:
            exit('No eggs-section found in buildout, \
aborting now, nothing changed.')

def addAddonToBinScripts(addon_path, instance_path):
    """Registers an add-on in every bin-script of the instance."""
    scripts_path = instance_path + 'bin/'
    script_paths = glob.glob(scripts_path + '*') # get all children
    for script_path in script_paths:
        addAddonToScript(addon_path, script_path)

def addAddonToInterpreterScript(addon_path, instance_path):
    """Registers an add-on in instance's interpreter."""
    script_path = instance_path + 'parts/instance/bin/interpreter'
    addAddonToScript(addon_path, script_path)

def delAddonOfScripts(addon_path, instance_path):
    """
    Remove add-on of instance's bin-scripts and of parts' interpreter-script.
    """
    if addon_path.endswith('/'): addon_path = addon_path[:-1]
    # Remove of bin-scripts:
    scripts_path = instance_path + 'bin/'
    script_paths = glob.glob(scripts_path + '*') # get all children
    for script_path in script_paths:
        removeLinesContainingPattern(script_path, addon_path)
    # Remove of interpreter:
    script_path = instance_path + 'parts/instance/bin/interpreter'
    removeLinesContainingPattern(script_path, addon_path)
    # Remove of buildout-conf:
    script_path = instance_path + 'buildout.cfg'
    addon_name = addon_path.split('/')[-1]
    if addon_name.endswith('.egg'):
        addon_name = addon_name.split('-')[0]
    removeLinesContainingPattern(script_path, addon_name)

def getAddonVersions(addon_paths):
    version = None
    versions = []
    for addon_path in addon_paths:
        if len(addon_path.split('-')) > 1: 
            version = addon_path.split('-')[1]
        else: # = development-egg
            version = None
        versions.append(version)
    return versions

def getDependencies(addon_path):
    """Exclude setuptools, as it's always a dependency."""
    dependencies = []
    if fileExists(addon_path + 'EGG-INFO/requires.txt'):
        lines = getLines(addon_path + 'EGG-INFO/requires.txt')
        for line in lines:
            if not line.startswith('[') and not line.startswith('setuptools'):
                if line.endswith('\n'): line = line[:-1] # remove linebreak
                if line != '':
                    # Check for brackets 'zope.security[untrustedpython]':
                    if line.find('[') > 0:
                        line = line.split('[')[0] # for now take name only
                        # TODO: We need to include brackets later!
                    dependencies.append(line)
            # A part-specific-decla starts here, we're done:
            if line.startswith('['):
                break
    if fileExists(addon_path + 'setup.py'):
        string = read(addon_path + 'setup.py')
        string = string.split('install_requires=[')[-1]
        string = string.split(']')[0]
        lines = string.split()
        for line in lines:
            if line.endswith(','):
                line = line[:-1]
            line = line[1:-1] # remove apostrophes
            if line != 'setuptools': # exclude setuptools
                dependencies.append(line)
    return dependencies

def getEggPath(addon_name, vs_pin='', egg_cache_paths=None):
    """
    Of all addon-versions, return the develop-vs, if no dev-vs exists,
    return the newest vs. If a version-pin is passed and no dev-egg available,
    return the newest version which satisfies the pin, unless pin is for a
    certain version, then return that one. Finally, return None for no success.
    """
    if not egg_cache_paths: egg_cache_paths = getEggCachePaths()
    addon_paths = getEggPaths(addon_paths)
    addon_path = addon_paths[-1]
    if addon_path.endswith('.egg'): # not a dev-vs
        # get newest:
        if vs_pin:
            pass#newest suffice pin?
    return addon_path

def getEggPaths(addon_name, egg_cache_paths=None):
    """
    Get addon-paths of all found versions, where egg_cache_paths
    points by default to '~/.buildut/eggs' and '~/.buildut/src'.
    Return dev-vs (if available) first, then sorted by newest vs.
    """
    addon_path = None
    addon_paths = []
    addon_vs = None
    # No egg_cache_paths passed, set defaults:
    if not egg_cache_paths: egg_cache_paths = getEggCachePaths()
    # For each egg-cache:
    for egg_cache_path in egg_cache_paths:
        # Get all egg-paths:
        egg_paths = glob.glob(egg_cache_path + '*') # get all children
        # For each egg:
        for egg_path in egg_paths:
            # Get its name of path:
            if egg_path.endswith('/'): egg_path = egg_path[:-1] # remove ending slash
            egg_name = egg_path.split('/')[-1]
            # Get vs:
            if egg_name.startswith(addon_name + '-'):
                addon_vs = egg_name.split('-')[1]
            # Stable version continue with a minus, dev-eggs are name-only:
            if egg_name.startswith(addon_name + '-') or egg_name == addon_name:
                addon_path = egg_cache_path + egg_name + '/'
                addon_paths.append(addon_path)
    # Sort to dev-vs first, followed by newest vesions:
    addon_paths = sorted(addon_paths, reverse=True)
    return addon_paths

