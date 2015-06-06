from adi.commons.commons import insertBeforeLastTag
from conventions import getAddonName

def addProfile(addon_path):
    addon_name = getAddonName(addon_path)
    last_lvl = getLastLvl(addon_path)
    profil_path = last_lvl + 'profiles/default/'
    addDirs(profil_path)
    addMetadata(profil_path)
    string = '\
\n\
  <genericsetup:registerProfile\n\
      name="default"\n\
      title="'+addon_name+'"\n\
      directory="profiles/default"\n\
      description="Installs the '+addon_name+' package"\n\
      provides="Products.GenericSetup.interfaces.EXTENSION"\n\
      />\n\
\n\
'

insertBeforeLastTag(last_lvl + 'configure.zcml', 'blah')

def addBrowser(addon_path):
    last_lvl = getLastLvl(addon_path)
    insertBeforeLastTag(last_lvl + 'configure.zcml', 'blah')

