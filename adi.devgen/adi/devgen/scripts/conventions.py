def getAddonName(addon_path):
    return addon_path.split('/')[-2]

def getAddonFirstName(addon_path):
    addon_name = getAddonName(addon_path)
    return addon_name.split('.')[0]

def getAddonLastName(addon_path):
    addon_name = getAddonName(addon_path)
    return addon_name.split('.')[1]

def getFirstLvl(addon_path):
    return addon_path + getAddonFirstName(addon_path) + '/'

def getLastLvl(addon_path):
    return getFirstLvl(addon_path) + getAddonLastName(addon_path) + '/'

