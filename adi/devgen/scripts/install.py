import os

from adi.commons.commons import addFile
from adi.commons.commons import addDirs
from adi.commons.commons import delFile
from adi.commons.commons import getFirstChildrenPaths
from adi.commons.commons import getHome
from adi.commons.commons import getIndent
from adi.commons.commons import getLines
from adi.commons.commons import getUrls
from adi.commons.commons import getRealPath
from adi.commons.commons import fileExists
from adi.commons.commons import hasStr

from adi.devgen.scripts.create import addBuildoutDefaultConfig

def installBuildout(virtenv_path):
    os.system('virtualenv ' + virtenv_path)
    os.system(virtenv_path + 'bin/pip install setuptools -U')
    os.system(virtenv_path + 'bin/pip install zc.buildout')

def getConfigs(plone_version, path):
    """Downloads versions.cfg and also gets the other
       configs referenced in its 'extends'-var, too,
       so we can work offline and let buildout run even faster.
    """
    versions_url = 'http://dist.plone.org/release/' + plone_version + '/versions.cfg'
    os.system('wget ' + versions_url + ' -P ' + path)
    versions_path = path + '/versions.cfg'
    string = open(versions_path).read();
    urls = getUrls(string)
    print 'urls'
    print urls
    for url in urls:
        os.system('wget ' + url + ' -P ' + path)
    makeConfigsUrlsLocal(path)

def makeConfigsUrlsLocal(configs_path):
    """Changes 'http://blabla/config.cfg' to 'config.cfg'
       in the extends-parts of the configs.
    """
    configs_paths = getFirstChildrenPaths(configs_path)
    for config_path in configs_paths:
        new_line = ''
        new_lines = []
        lines = getLines(config_path)
        for line in lines:
            indent = getIndent(line)
            stripped_line = line.strip() # remove trailing spaces
            if not stripped_line.startswith('#') and hasStr(line, 'http://') or hasStr(line, 'https://'):
                urls = getUrls(line)
                if len(urls) > 1:
                    exit('Found several urls in one line, not considered, yet, until neccessary.')
                else:
                    url = urls[0]
                    local_path = url.split('/')[-1]
                    new_line = local_path + '\n'
                    if line.startswith('extends'):
                        new_line = 'extends = ' + new_line
                    new_lines.append('#' + line + indent + new_line)
            else:
                new_lines.append(line)
        string = ''.join(new_lines)
        if fileExists(config_path):
            delFile(config_path)
        addFile(config_path, string)


def addBuildoutSkel(plone_vs):
    """
    Create $HOME/[path]. In it create default.cfg, eggs, deveggs, configs and a
    virtenv. Install buildout with the latter.
    """

    path = getHome() + '.buildout/'

    paths = [path, path + 'eggs/', path + 'deveggs/', path + 'configs/']

    # Create dirs:
    for p in paths: addDirs(p)

    # Create virtenv:
    if not fileExists(path + 'virtenv'): installBuildout(path + 'virtenv'); print 'Add virt'

    # Create confs:
    conf_path = path + 'configs/' + plone_vs + '/'
    if not fileExists(conf_path): addDirs(conf_path); print 'Add ' + conf_path; getConfigs(plone_vs, conf_path)

    # Create default-conf:
    addBuildoutDefaultConfig(plone_vs, path)


def addPloneSkel(plone_vs, path):
    """Checks, if shared buildout-sources are available and adds a buildout.cfg to directory."""

    addBuildoutSkel(plone_vs)
    if not fileExists(path): addDirs(path)
    os.system('touch ' + path + 'buildout.cfg')


