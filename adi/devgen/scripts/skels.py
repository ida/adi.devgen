import os

from adi.commons.commons import addDirs
from adi.commons.commons import addFile
from adi.commons.commons import fileExists

from adi.devgen.scripts.conventions import getAddonFirstName
from adi.devgen.scripts.conventions import getLastLvlPath
from adi.devgen.scripts.conventions import getProfilePath
from adi.devgen.scripts.conventions import getResourcesPath
from adi.devgen.scripts.conventions import getUnderscoredName

from adi.devgen.scripts.create import addBrowser
from adi.devgen.scripts.create import addBuildoutConfig
from adi.devgen.scripts.create import addDocs
from adi.devgen.scripts.create import addDependency
from adi.devgen.scripts.create import addFirstInit
from adi.devgen.scripts.create import addLastInit
from adi.devgen.scripts.create import addMetadata
from adi.devgen.scripts.create import addSetupPy
from adi.devgen.scripts.create import addSkin
from adi.devgen.scripts.create import registerProfile
from adi.devgen.scripts.create import setSetupPy

from adi.devgen.scripts.install import addPloneSkel

class AddSkel(object):

    def addBaseSkel(self, path):
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

        if not path.endswith('/'): path += '/'
        
        if path != './':

            addon_name = path[:-1]

            addon_first_name = addon_name.split('.')[0]
            addon_scnd_name = addon_name.split('.')[1]
            first_lvl = path + addon_first_name + '/'
            last_lvl = first_lvl + addon_scnd_name + '/'

            addDirs(last_lvl)
            addSetupPy(path)
            addFirstInit(first_lvl)
            addLastInit(last_lvl)

            return path

        else:
            exit('No setup.py found. Please specify a path to the addon, by appending it as an additional argument.')

    def addMetaSkel(self, path='.'):
        """ Add 'README.md', 'MANIFEST.in' and a docs-folder with further files.
            To inform your users and to be possibly publishable on pypi.
        """
        if not path.endswith('/'): path += '/'
        if path != './': path = self.addBaseSkel(path)
        addon_forename = getAddonFirstName(path)
        addFile(path + 'MANIFEST.in', 'recursive-include ' + addon_forename + ' *\nrecursive-include docs *\ninclude *.md\nglobal-exclude *.pyc\nglobal-exclude *.pyo\n')
        addFile(path + 'README.md', 'Introduction\n============\n\n\
An addon for Plone, aiming to [be so useful, you never want to miss it again].\n')
        addDirs(path + 'docs')
        addDocs(path)
        setSetupPy(path + 'setup.py')

    def addProfileSkel(self, path='.'):
        """ Be installable via a Plonesite's quickinstaller.
        """
        if not path.endswith('/'): path += '/'
        if path != './':
            self.addBaseSkel(path)

        registerProfile(getLastLvlPath(path))
        addDirs(getProfilePath(path))
        addMetadata(getProfilePath(path))

    def addSkinSkel(self, path='.'):
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

    def addBrowserSkel(self, path='.'):
        """ Add a browser-based skel."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfileSkel(path)
        if not fileExists(getProfilePath(path)):
            self.addProfileSkel(path)
        addDirs(getResourcesPath(path))
        addBrowser(path)

    def addDep(self, dep_name, path='.'):
        """ Add a dependency-addon to an addon."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfileSkel(path)
        addDependency(dep_name, path)

    def addInstallScript(self, path='.'):
        """ Add and register a file called 'setuphandlers.py', 
            in addon, which will be executed on (re-)installs.
        """
        if not path.endswith('/'): path += '/'
        addSetuphandlers(path)


    def getRepos(self, urls, path='.'):
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
        repos_path = path
        if repos_path == '.' or repos_path == './': repos_path = ''
        types = ['git', 'svn', 'fs'] # if omitted, defaults to first item
        urls = urls.split(',')
        for url in urls:
            url = url.strip() # remove trailing spaces
            repo_name = url.split('/')[-1].split('.git')[0]
            path = repos_path + repo_name
            if url.split(' ')[0] in types: # user specified type
                typ = url.split(' ')[0] # get type
                url = ' '.join(url.split(' ')[1:]) # remove type of url
            else:
                typ = types[0] # default to first type

            if not url.startswith('http') and not typ=='fs':
                url = 'http://' + url

            if typ=='git':
                os.system('git clone ' + url + ' ' + path)
            elif typ=='svn':
                os.system('svn co ' + url + ' ' + path)
            elif typ=='fs':
                os.system('cp -r ' + url + ' ' + path)


    def getReposOfUser(self, url, eggs, path='.'):
        """
        Usage:
        $ devgen getReposOfUser [user_address] [repos as CSV-str]
        Example:
        $ devgen getReposOfUser 'github.com/collective' 'collective.portlet.sitemap -b 1.0.4, mailtoplone.base'
        """

        if not url.endswith('/'): url += '/'
        if not path.endswith('/'): path += '/'
        urls = []
        eggs = eggs.split(',')
        for egg in eggs:
            egg = egg.strip() # remove trailing spaces
            urls.append(url + egg)
        urls = ','.join(urls)
        self.getRepos(urls, path)

    def installPlone(self, plone_version, path='.'):
        if not path.endswith('/'): path += '/'
        addPloneSkel(plone_version, path)


