########################################################################
from adi.commons.commons import fileExists # DEV
from adi.commons.commons import delDirs # DEV
import shutil # DEV
########################################################################

import sys
from scripts.skels import addDefaultSkel

def devgen(addon_name=sys.argv[1]): # Fetch user's-input first-param.
    if fileExists(addon_name): 
        shutil.rmtree(addon_name) # DEV: Search and destroy. Destroy, especially.
# DEV: Omit for now:
#        print "A directory named '%s' already exists, aborting script-execution now, nothing has changed." %addon_name
#        exit()
    addon_path = addon_name + '/' # We want paths to always end with a slash.
    addDefaultSkel(addon_path)

