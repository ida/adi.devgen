import os
from adi.commons.commons import *
from conventions import *
from create import *

class AddSkel(object):

    def addBaseSkel(self, path, addon_name):
        """ Be avail- and installable for ZOPE.
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

    def addProfileSkel(self, path, addon_name):
        """ Be installable via a Plonesite's quickinstaller.
        """
        if not path.endswith('/'): path += '/'
        if path != './':
            addon_name = path.split('/')[-2]
            self.addBaseSkel(path, addon_name)

        last_lvl = getLastLvlPath(path)
        profil_path = getProfilePath(path)

        registerProfile(last_lvl)
        addDirs(profil_path)
        addMetadata(profil_path)

    def addSkinSkel(self, path, addon_name):
        """ Add a skins-based skel."""
        if not path.endswith('/'): path += '/'
        if path != './':
            addon_name = path.split('/')[-2]
            self.addProfileSkel(path, addon_name)
        name_underscored = getUnderscoredName(path)
        last_lvl = getLastLvlPath(path)
        if not fileExists(last_lvl + 'profiles'):
            self.addProfileSkel(path)
        addDirs(last_lvl + 'skins/' + name_underscored)
        addSkin(path)

    def addBrowserSkel(self, path, addon_name):
        """ Add a browser-based skel."""
        if not path.endswith('/'): path += '/'
        if path != './':
            addon_name = path.split('/')[-2]
            self.addProfileSkel(path, addon_name)
        addDirs(getResourcesPath(path))
        addBrowser(path)

    def addDep(self, dep_name, path):
        """ Add a dependency-addon to an addon."""
        if not path.endswith('/'): path += '/'
        addDependency(dep_name, path)

    def addInstallerScript(self, path='.'):
        """ Add and register a file called 'setuphandlers.py', 
            which will be executed on (re-)installs.
        """
        if not path.endswith('/'): path += '/'
        addSetuphandlers(path)


    def addBuildoutSkel(self, path='.'):
        """ Add a buildout skel."""
        if not path.endswith('/'): path += '/'
        path += 'plone-instance/'
        addDirs(path + 'src/')
        addBootstrap(path)
        addBuildout(path)

    def buildOut(self, path):
        """ Trigger bootstrapping and outbuilding."""
        buildout(path)
