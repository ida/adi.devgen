from adi.commons.commons import *
from conventions import *
from create import *

class AddSkel(object):

    def addBaseSkel(self, path):
        """ Be installable and available to ZOPE
            (addable to buildout or droppable to an
            oldschool-products-folder), thereyby also
            available to Plonesites and callable of
            other addons/eggs (registered in syspath).
        """
        if not path.endswith('/'): path += '/'
        addon_name = path.split('/')[-2]
        addon_first_name = addon_name.split('.')[0]
        addon_scnd_name = addon_name.split('.')[1]
        first_lvl = path + addon_first_name + '/'
        last_lvl = first_lvl + addon_scnd_name + '/'
        addDirs(last_lvl)
        addSetup(path)
        addFirstInit(first_lvl)
        addLastInit(last_lvl)

    def addProfileSkel(self, path='.'):
        """ Be installable via a Plonesite's quickinstaller,
            or pulled as dependency of another addon,
            or of collective.recipe.plonesite.
        """
        if not path.endswith('/'): path += '/'
        self.addBaseSkel(path)
        last_lvl = getLastLvlPath(path)
        profil_path = getProfilePath(path)
        addDirs(profil_path)
        addMetadata(profil_path)
        if not fileExists(last_lvl + 'configure.zcml'):
            addConfig(last_lvl)
        addProfile(last_lvl)

    def addSkinSkel(self, path='.'):
        """ Add a skins-based skel."""
        if not path.endswith('/'): path += '/'
        self.addProfileSkel(path)
        name_underscored = getUnderscoredName(path)
        last_lvl = getLastLvlPath(path)
        addDirs(last_lvl + 'skins/' + name_underscored)
        addSkin(path)

    def addBrowserSkel(self, path='.'):
        """ Add a browser-based skel."""
        if not path.endswith('/'): path += '/'
        self.addProfileSkel(path)
        addDirs(getResourcesPath(path))
        addBrowser(path)

    def addDep(self, dep_name, path='.'):
        """ Add a dependency."""
        if not path.endswith('/'): path += '/'
        addDependency(dep_name, path)


