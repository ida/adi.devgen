import os
from commons.commons import *
from adi.devgen.scripts.conventions import *
from adi.devgen.scripts.create import *

class AddSkel(object):

    def addBaseSkel(self, addon_name):
        """
            Minimum skel for a Plone-addon, expects at least an addon-name.

            Example:

            $ devgen addBaseSkel addon.name

            Optionally prepend a path, if you want the addon not to be 
            created in this folder:

            $ devgen addBaseSkel /path/to/target/folder/addon.name

            Registers egg in buildout's syspath and is thereby
            available to the instance's Python-interpreter. Can be
            used for addons, which don't need profiles.

        """

        addon_path = addon_name + '/'

        addon_first_name = addon_name.split('.')[0]
        addon_scnd_name = addon_name.split('.')[1]
        first_lvl = addon_path + addon_first_name + '/'
        last_lvl = first_lvl + addon_scnd_name + '/'

        addDirs(last_lvl)
        addSetup(addon_path)
        addFirstInit(first_lvl)
        addLastInit(last_lvl)

        return addon_path

    def addMetaSkel(self, path):
        """ Adds a README, a MANIFEST and a docs-folder with a history-file.
            Because.
            And to be publishable on pypi.
        """
        if not path.endswith('/'): path += '/'
        if path != './': path = self.addBaseSkel(path)
        addon_forename = getAddonFirstName(path)
        addFile(path + 'MANIFEST.in', 'recursive-include ' + addon_forename + ' *\nrecursive-include docs *\ninclude *\nglobal-exclude *.pyc\n')
        addFile(path + 'README.md', 'Introduction\n============\n\n\
An addon for Plone, aiming to [be so useful, you never want to miss it again].\n\nUsage\n=====\n\n')
        addDirs(path + 'docs')
        addFile(path + 'docs/HISTORY.txt', 'Changelog\n=========\n')
        setSetupPy(path + 'setup.py')

    def addProfileSkel(self, path):
        """ Be installable via a Plonesite's quickinstaller.
        """
        if not path.endswith('/'): path += '/'
        if path != './':
            self.addBaseSkel(path)

        registerProfile(getLastLvlPath(path))
        addDirs(getProfilePath(path))
        addMetadata(getProfilePath(path))

    def addSkinSkel(self, path):
        """ Add a skins-based skel."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfileSkel(path)
        if not fileExists(getProfilePath(path)):
            self.addProfileSkel('.')
        name_underscored = getUnderscoredName(path)
        last_lvl = getLastLvlPath(path)
        addDirs(last_lvl + 'skins/' + name_underscored)
        addSkin(path)

    def addBrowserSkel(self, path):
        """ Add a browser-based skel."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfileSkel(path)
        if not fileExists(getProfilePath(path)):
            self.addProfileSkel(path)
        addDirs(getResourcesPath(path))
        addBrowser(path)

    def addDep(self, dep_name, path):
        """ Add a dependency-addon to an addon."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfileSkel(path)
        addDependency(dep_name, path)

    def addInstallerScript(self, path):
        """ Add and register a file called 'setuphandlers.py', 
            in addon, which will be executed on (re-)installs.
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

    def getDevEggs(self, urls, path):
        """ Expects a str with with repo-urls,
            separated by commas, then downloads/clones/checks
            them out to this directory, or specify another path.
            Optionally prepend repo-type to address, available are:
            'git', 'svn' and 'fs', if it lives on the filesystem, defaults to git.
            If, url doesn't start with 'http://' and it's not of type 'fs', it will be appended.
            If you are forced to use SSL, type full adress: 'https://github.com/(...)'
            Example:
            $ devgen getDevEggs 'github.com/ida/adi.devgen --branch brunch, svn svn.plone.org/svn/collective/adi.suite/trunk/ adi.suite'
        """
        types = ['git', 'svn', 'fs'] # if omitted, defaults to first item
        urls = urls.split(',')
        for url in urls:
            url = url.strip() # remove trailing spaces

            if url.split(' ')[0] in types: # user specified type
                typ = url.split(' ')[0] # get type
                url = ' '.join(url.split(' ')[1:]) # remove type of url
            else:
                typ = types[0] # default to first type

            if not url.startswith('http') and not typ=='fs':
                url = 'http://' + url

            if typ=='git':
                os.system('git clone ' + url)
            elif typ=='svn':
                os.system('svn co ' + url)
            elif typ=='fs':
                os.system('cp -r ' + url + ' .')

    def getReposOfSameVCSUser(self, url, eggs, path='.'):
        """ Example usage:
        $ devgen getReposOfSameVCSUser 'github.com/collective' 'collective.portlet.sitemap -b 1.0.4, mailtoplone.base'
        """
        if not url.endswith('/'): url += '/'
        urls = []
        eggs = eggs.split(',')
        for egg in eggs:
            egg = egg.strip() # remove trailing spaces
            urls.append(url + egg)
        urls = ','.join(urls)
        self.getDevEggs(urls, '.')

