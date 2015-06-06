from adi.commons.commons import addDirs
from adi.commons.commons import addFile
from adi.commons.commons import insertBeforeLastTag

from conventions import getFirstLvl
from conventions import getLastLvl

from create import addSetup
from create import addFirstInit
from create import addLastInit
from create import addConfig
from create import addMetadata

from clusters import addProfile

def addMinimalstSkel(addon_path):
    first_lvl = getFirstLvl(addon_path)
    last_lvl = getLastLvl(addon_path)
    addDirs(last_lvl)
    addSetup(addon_path)
    addFirstInit(first_lvl)
    addFile(last_lvl + '__init__.py')

def addMinimalSkel(addon_path):
    addMinimalstSkel(addon_path)
    addConfig(addon_path)
    addProfile(last_lvl)

def addMinimumSkel(addon_path):
    addMinimalSkel(addon_path)
    addBrowser(addon_path)

def addDefaultSkel(addon_path):
    addMinimumSkel(addon_path)

#EOF
