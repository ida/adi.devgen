from adi.commons.commons import getRealPath
from adi.commons.commons import getParentDirPath
from adi.commons.commons import fileExists

def getAddonPath(path):
    """ 'path' must point to addon or a child of it. """
    max_exceed = 27
    path = getRealPath(path)
    while not fileExists(path + 'setup.py'):
        path = getParentDirPath(path)
        max_exceed -= 1
        if max_exceed < 1:
            print "No setup.py found. Please specify a path to the addon, by appending it as an additional argument."
            path = None
    return path

def getFirstLvlPath(path):
    path = getAddonPath(path) + getAddonFirstName(path) + '/'
    return path

def getLastLvlPath(path):
    path = getFirstLvlPath(path) + getAddonLastName(path) + '/'
    return path

def getConfigPath(path):
    path = getLastLvlPath(path) + 'configure.zcml'
    return path

def getProfilePath(path):
    path = getLastLvlPath(path) + 'profiles/default/'
    return path

def getSkinPath(path):
    path = getLastLvlPath(path) + 'skins/' + getUnderscoredName(path) + '/'
    return path

def getBrowserPath(path):
    path = getLastLvlPath(path) + 'browser/'
    return path

def getResourcesPath(path):
    path = getBrowserPath(path) + 'resources/'
    return path

def getAddonName(path):
    path = getAddonPath(path)
    name = path.split('/')[-2]
    return name

def getAddonFirstName(path):
    name = getAddonName(path).split('.')[0]
    return name

def getAddonLastName(path):
    name = getAddonName(path).split('.')[1]
    return name

def getUnderscoredName(path):
    name = getAddonFirstName(path) + '_' + getAddonLastName(path)
    return name
    
def getUppercasedName(path):
    name = getAddonFirstName(path).title() + getAddonLastName(path).title()
    return name
    
#EOF
