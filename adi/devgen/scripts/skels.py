# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from adi.commons.commons import addDirs
from adi.commons.commons import addFile
from adi.commons.commons import appendToFile
from adi.commons.commons import fileExists
from adi.commons.commons import getHome
from adi.commons.commons import insertAfterNthLine
from adi.commons.commons import removeLinesContainingPattern
from adi.commons.commons import writeFile

from adi.devgen.scripts.buildout import addAddonToBinScripts
from adi.devgen.scripts.buildout import addAddonToBuildoutConfig
from adi.devgen.scripts.buildout import addAddonToInterpreterScript
from adi.devgen.scripts.buildout import delAddonOfScripts
from adi.devgen.scripts.buildout import getAddonVersions
from adi.devgen.scripts.buildout import getDependencies
from adi.devgen.scripts.buildout import getEggPaths

from adi.devgen.scripts.conventions import getAddonFirstName
from adi.devgen.scripts.conventions import getAddonPath
from adi.devgen.scripts.conventions import getLastLvlPath
from adi.devgen.scripts.conventions import getProfilePath
from adi.devgen.scripts.conventions import getResourcesPath
from adi.devgen.scripts.conventions import getUnderscoredName

from adi.devgen.scripts.create import addAndRegisterCss
from adi.devgen.scripts.create import addAndRegisterJs
from adi.devgen.scripts.create import addAndRegisterView
from adi.devgen.scripts.create import addBrowserFiles
from adi.devgen.scripts.create import addDocs
from adi.devgen.scripts.create import addDependency
from adi.devgen.scripts.create import addFirstInit
from adi.devgen.scripts.create import addLastInit
from adi.devgen.scripts.create import addMetadata
from adi.devgen.scripts.create import addSetuphandlers
from adi.devgen.scripts.create import addSetupPy
from adi.devgen.scripts.create import addSkinFiles
from adi.devgen.scripts.create import registerProfile
from adi.devgen.scripts.create import setSetupPy

from adi.devgen.scripts.git import checkForDiffs
from adi.devgen.scripts.git import checkForUnpushedCommits
from adi.devgen.scripts.git import createTag

from adi.devgen.scripts.install import addBuildout

class AddSkel(object):

    def addAddon(self, addon_name, vs_pin='', instance_path='./'):
        """
        Register an addon in all bin-scripts of the instance,
        in the parts/interpreter-script of the instance and
        add an entry in the buildout-config.
        Do the same with any dependency of the add-on.
        """
        INSTALLED_IN_INTERPRETER = False
        addon_name_and_vs_pin = addon_name + vs_pin
        addon_name_and_vs_pins = [addon_name_and_vs_pin]
        addon_paths = None
        addon_path = None
        vs_pin_pos = None
        for i, addon_name_and_vs_pin in enumerate(addon_name_and_vs_pins):
            INSTALLED_IN_INTERPRETER = False # reset

            # Extract addon_name and vs_pin:
            # vs-pin can start with '<, '>', '=' or ' ':
            for j, char in enumerate(addon_name_and_vs_pin):
                if char == '<' or char == '>' or char == '=' or char == ' ':
                    vs_pin_pos = j
                    break
            if vs_pin_pos:
                addon_name = addon_name_and_vs_pin[:vs_pin_pos]
                vs_pin = addon_name_and_vs_pin[vs_pin_pos:]
                vs_pin = vs_pin.strip() # remove trailing spaces
                vs_pin_pos = None # reset
            else:
                addon_name = addon_name_and_vs_pin
            addon_paths = getEggPaths(addon_name)

            # No addon-paths found, this can have several reasons:
            if len(addon_paths) < 1:
# The egg's name contains underscores and is represented in the addon-name with minus-signs:
                addon_paths = getEggPaths(addon_name.replace('-', '_'))
            if len(addon_paths) < 1:
# The egg's name is capitalized and is represented in the addon-name with lowercase:
                addon_paths = getEggPaths(addon_name.capitalize())
            if len(addon_paths) < 1:
# The egg is installed to the Python-interpreter, we'll then skip any further procedure with this addon:
                if os.system('python -m ' + addon_name) == 0: # check exit-code
                    INSTALLED_IN_INTERPRETER = True
# No other case thinkable, the egg is actually not available:
            if len(addon_paths) < 1 and not INSTALLED_IN_INTERPRETER:
                exit('The addon "' + addon_name + '" seems not to exist, you \
probably wanna run buildout to get it."')

            # There are addon_paths (= addon not installed in py-interpreter):
            if len(addon_paths) > 0:
                addon_path = addon_paths[0] # first is either a dev-vs or newest stable-vs
                # TODO: Regard version-pinning.
                dependencies = getDependencies(addon_path)
                for dependency in dependencies:
                    if not dependency in addon_name_and_vs_pins:
                        addon_name_and_vs_pins.append(dependency)
                addAddonToBinScripts(addon_path, instance_path)
                addAddonToInterpreterScript(addon_path, instance_path)
                # Add only the intital add-on to buildout-conf:
                if i == 0:
                    addAddonToBuildoutConfig(addon_path, instance_path)

    def addOn(self, path):
        """
        Create addon with browser-based 'main.css', 'main.js',
        'main.py' and 'main.pt'. Include metadata.
        """
        filename = 'main'
        self.addMeta(path)
        self.addCss(filename, path)
        self.addJs(filename, path)
        self.addView(filename, path)

    def addBase(self, path):
        """
        Create minimum-skel: Root folder with setup.py,
        first-level and second-level-folder and their '__init__.py'-s.
        Register egg in buildout's syspath and be thereby
        available to the ZOPE-instance's Python-interpreter. Can be
        used for addons, which don't need profiles.

        """
        if not path.endswith('/'): path += '/'
        if not fileExists(path):
            addon_name = path[:-1] # omit last slash
            # If a path to addon was prepended, extract addon_name of path:
            if addon_name.find('/') != -1: addon_name.split('/')[-1]
            # Prep path for creating dirs:
            addon_first_name = addon_name.split('.')[0]
            addon_scnd_name = addon_name.split('.')[1]
            first_lvl = path + addon_first_name + '/'
            last_lvl = first_lvl + addon_scnd_name + '/'
            # Create dirs:
            addDirs(last_lvl)
            # Create files:
            addSetupPy(path)
            addFirstInit(first_lvl)
            addLastInit(last_lvl)

    def addBrowser(self, path='.'):
        """ Add browser-skel."""
        if not path.endswith('/'): path += '/'
        if path != './' and not fileExists(path):
            path = path.split('/')[-2]
            self.addProfile(path)
        if not fileExists(getProfilePath(path)):
            self.addProfile(path)
        addDirs(getResourcesPath(path))
        addBrowserFiles(path)

    def addMeta(self, path='.'):
        """ Add 'README.rst', 'MANIFEST.in' and a docs-folder with further files.
            To inform your users and to be possibly publishable on pypi.
        """
        if not path.endswith('/'): path += '/'
        if path != './': self.addBase(path)
        addon_forename = getAddonFirstName(path)
        addFile(path + 'MANIFEST.in', 'recursive-include ' + addon_forename + ' *\nrecursive-include docs *\ninclude *.rst\nglobal-exclude *.pyc\nglobal-exclude *.pyo\n')
        addFile(path + 'README.rst', 'Introduction\n============\n\n\
An addon for Plone, aiming to [be so useful, you never want to miss it again].\n')
        addDirs(path + 'docs')
        addDocs(path)
        setSetupPy(path + 'setup.py')

    def addProfile(self, path='.'):
        """ Be installable via a Plonesite's quickinstaller.
        """
        if not path.endswith('/'): path += '/'
        if not fileExists(path) and path != './':
            self.addBase(path)
        if not fileExists(getProfilePath(path)):
            registerProfile(getLastLvlPath(path))
            addDirs(getProfilePath(path))
        if not fileExists(getProfilePath(path) + 'metadata.xml'):
            addMetadata(getProfilePath(path))

    def addSkin(self, path='.'):
        """ Add skins-skel."""
        if not path.endswith('/'): path += '/'
        if path != './' and not fileExists(path):
            path = path.split('/')[-2]
            self.addProfile(path)
        if not fileExists(getProfilePath(path)):
            self.addProfile(path)
        name_underscored = getUnderscoredName(path)
        last_lvl = getLastLvlPath(path)
        addDirs(last_lvl + 'skins/' + name_underscored)
        addSkinFiles(path)

    def addCss(self, filename='main', path='.'):
        """Register and add a browser-based CSS-file."""
        if not path.endswith('/'): path += '/'
        if path != './' or not fileExists(getResourcesPath(path)):
            self.addBrowser(path)
        addAndRegisterCss(filename, path)

    def addJs(self, filename='main', path='.'):
        """Register and add a browser-based JS-file."""
        if not path.endswith('/'): path += '/'
        if path != './' or not fileExists(getResourcesPath(path)):
            self.addBrowser(path)
        addAndRegisterJs(filename, path)

    def addView(self, filename='main', path='.'):
        """Register and add a browser-based view with a template."""
        if not path.endswith('/'): path += '/'
        if path != './' or fileExists(getResourcesPath(path)) == False:
            self.addBrowser(path)
        addAndRegisterView(filename, path)

    def addDep(self, dep_name, path='.'):
        """ Add a dependency-addon to an addon."""
        if not path.endswith('/'): path += '/'
        if path != './':
            path = path.split('/')[-2]
            self.addProfile(path)
        addDependency(dep_name, path)

    def delDep(self, dep_name, path='.'):
        """Remove a dependency-addon off an addon."""
        fil = getProfilePath(path) + 'metadata.xml'
        removeLinesContainingPattern(fil, dep_name)
        fil = getAddonPath(path) + 'setup.py'
        removeLinesContainingPattern(fil, dep_name)

    def addInstallScript(self, path='.'):
        """
        Add and register a file called 'setuphandlers.py', 
        in addon, which will be executed on (re-)installs.
        """
        self.addProfile(path)
        addSetuphandlers(path)

    def addPlone(self, path='.', plone_version='4.3.9'):
        """
        Check, if shared buildout-sources are available in $HOME/.buildout,
        add buildout.cfg to path, run buildout, raise server.
        """
        if not path.endswith('/'): path += '/'
        if not fileExists(path): addDirs(path)
        addBuildout(plone_version)
        os.system('echo """[buildout]\n\
extends = ' + getHome() + '.buildout/configs/' + plone_version + '/versions.cfg\
""" > ' + path + 'buildout.cfg')
        self.buildOut(path)
        self.run(path)

    def delAddon(self, addon_name, instance_path='./'):
        """
        Unregister an add-on.
        Add-on name can contain a specified version, starting with a '='.
        Otherwise a found development-version will preceed a found stable
        version, when no development-version is found, then the newest
        found version will be taken.
        """
        addon_versions = None
        addon_names = [addon_name]
        for addon_name in addon_names:
            addon_paths = getEggPaths(addon_name)
            addon_versions = getAddonVersions(addon_paths)
            addon_path = getEggPaths(addon_name)[-1] # latest found
            dependencies = getDependencies(addon_path)
            for dependency in dependencies:
                if not dependency in addon_names:
                    addon_names.append(dependency)
            delAddonOfScripts(addon_path, instance_path)

    def buildOut(self, path='.'):
        """
        Run buildout in passed path.
        """
        if not path.endswith('/'): path += '/'
        os.system(getHome() + '.buildout/virtenv/bin/buildout -c ' + path + 'buildout.cfg')

    def run(self, path='.'):
        """
        Raise server-client, a.k.a. instance, in passed path.
        """
        if not path.endswith('/'): path += '/'
        os.system(path + 'bin/instance fg')

###########
#  REPOS  #
###########

    def addLog(self, comment, path='.'):
        """
        Add passed comment to docs/CHANGES.rst with auto-appended current
        username and execute git-commit with the same comment, applying to
        all modified git-indexed files.
        """
        if not path.endswith('/'): path += '/'
        path = getAddonPath(path) + 'docs/CHANGES.rst'
        if not fileExists(path): addFile(path)
        insertAfterNthLine(path, '- ' + comment + '. [' + os.getenv('USER') + ']\n', 6)
        os.system('git commit -am "' + comment + '"')

    def checkoutLatestTag(self, path='.'):
        """
        Fetch newest tag of remote-master-repo
        and switch local branch to newest tag.
        """
        os.system('cd ' + path + ';\
        git checkout master; git pull --rebase origin master; git fetch; git checkout tags/$(git describe)')


    def deploy(self, host, repo_path, instance_path=None, ssh_port='22'):
        """
        Creates an annotated tag in a local repo, then fetches it on an existing
        remote clone, and switches branch to this newest tag with a checkout.

        If instance_path is given, restarts instance after changes.

        Example:

        devgen deploy user@example.org /path/to/repo /path/to/instance

        Where the paths must be absolut.

        Assumes you are located in the local repo, when executing this.
        Assumes you have a local repo and a clone of it on a remote machine.
        Assumes adi.devgen is also installed on remote.
        Assumes remote instance lives in instance_path and is called 'instance'.
        Assumes authentication is done automagically by an ssh-agent, pubkey
        is deposited and registered as allowed on remote.
        """
        createTag()
        kommand = 'cd ' + repo_path + '; devgen checkoutLatestTag;'
        if instance_path: kommand += 'cd ' + instance_path + '; ./bin/instance restart'
        os.system('devgen doOnRemote ' + host + ' "' + kommand + '"' + ' ' + ssh_port)


    def getRepos(self, urls, path='.'):
        """
        Expects a str with with repo-urls,
        separated by commas, then downloads/clones/checks
        them out to this directory, or specify another path.
        Optionally prepend repo-type to address, available are:
        'git', 'svn' and 'fs', if it lives on the filesystem, defaults to git.
        If, url doesn't start with 'http://' and it's not of type 'fs', it will be prepended.
        If you are forced to use SSL, type full adress: 'https://github.com/(...)'
        Example:
        $ devgen getRepos 'github.com/ida/adi.devgen --branch brunch, svn svn.plone.org/svn/collective/adi.suite/trunk/ adi.suite'
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

    def squash(self, amount_of_backwardsteps, new_commit_msg=''):
        """
        Unify several git-commits into one. Optionally pass new commit-msg,
        otherwise the msg of the oldest commit of the squashed commits is used.
        Thanks to Chris Johnson:
        http://stackoverflow.com/questions/5189560/squash-my-last-x-commits-together-using-git/5201642#5201642
        """
        # Remove last n commit-logs:
        os.system('git reset --soft HEAD~' + amount_of_backwardsteps)
        # Add new log:
        os.system('git commit -m "' + new_commit_msg + '"')
        # If no new_commit_msg was passed, default
        # to msg of oldest squashed commit:
        # Nota: To have all msgs of all commits unified in the new msg,
        # simply change amount_of_backwardsteps to 1, in the following lines:
        if not new_commit_msg:
            new_commit_msg = os.system(
                'git commit -m"$(git log --format=%B HEAD..HEAD@{' +
                amount_of_backwardsteps + '})"')

    def getGitReport(self, path='.'):
        """
        Perform a diff- and unpushed-commits-check,
        for each directory in the given path. Write each check
        into reportfiles 'git-diff-report.txt' and 'git-unpushed-commits.txt'.
        """
        if not path.endswith('/'): path += '/'
        checkForDiffs(path)
        checkForUnpushedCommits(path)


############
#  REMOTE  #
############

    def doOnRemote(self, host, command, ssh_port='22'):
        """
        Example:
        $ devgen doOnRemote username@example.org "ls -al"

        A file named 'report.txt' will be created in the same directory where
        you execute this, containing all output the commands on the remote-
        machine return. Additionally there's also a file 'prompt.txt',
        containing returned errors only and prompt them immediately to the
        user. Otherwise no news are good news.

        Found inspiration here:
        https://gist.github.com/bortzmeyer/1284249
        """

        ERRORS = False
        ssh_connection = None
        results = ''
        prompt = ''
        report = ''
        passed_command = command # keep orig before altering it

        report += 'STA ' + passed_command + '\n'

        # If we have a git-command, we have to deal with it returning
        # non-error-msgs to stderr, the error-channel ('pipe') of a shell.
        # We overcome this by additionally prepending 'echo $?' as a command,
        # which will return the exit-code of the git-command, only, to be able
        # to doublecheck, if we really have an error, or not:
        if command.startswith('git '):
            command = command.strip() # remove trailing spaces
            if not command.endswith(';'): # add commands-separator
                command += ';'
            command += 'echo $?' # add command
        # Open a connection and excute command-line on remote host:
        args = ['ssh', '-p', ssh_port, host, command]
        ssh_connection = subprocess.Popen(args,
                                          shell=False,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

        # Read results:
        results = ssh_connection.stdout.readlines()

        # No results, probably an error:
        if results == []:
            ERRORS = True
            errors = ssh_connection.stderr.readlines()
            # We probably should pipe the return into our local shell's stderr:
            # print >>sys.stderr, "ERROR: %s" % error
            # But we (her royal majesty and their multiple personalities)
            # prefer another prompt-style:
            for error in errors:
                prompt += error
                report += 'ERR ' + error
        else:
            for result in results:
                # Regard a program might have piped a success to stderr, exitcode tells
                # us, there really went something wrong:
                if result == '1\n' or result == '128\n':
                    ERRORS = True
                    report += 'ERR ' + result
                    prompt += result
                # Regard a program might have piped a success to stderr, exitcode tells
                # us, everything went allright, we omit prompting the exitcode:
                elif result != '0\n':
                    report += 'SCS ' + result
                # Otherwise proceed as usual:
                else:
                    report += 'SCS ' + result
                    prompt += result

        report += 'END ' + passed_command + '\n\n'

        # Add report:
        appendToFile('report.txt', report)
        # Write prompt to file:
        writeFile('prompt.txt', prompt)
        # Prompt prompt-txt:
        os.system('cat prompt.txt')

