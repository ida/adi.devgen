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
    versions_name = 'versions.cfg'
    versions_url = 'http://dist.plone.org/release/' + plone_version + '/' + versions_name
    os.system('wget ' + versions_url + ' -P ' + path)
    versions_path = path + '/versions.cfg'
    string = open(versions_path).read();
    urls = getUrls(string)
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
        tmpfil = config_path + '.tmp'
        if fileExists(tmpfil):
            delFile(tmpfil)
        addFile(tmpfil, string)

def addBuildoutSkel(plone_vs, path):
    """
    Create $HOME/.buildout. In it create default.cfg, eggs, deveggs, configs and a
    virtenv. Install buildout with the latter.
    """
    paths = [path,
             path + 'eggs/',
             path + 'deveggs/',
             path + 'configs/']

    for p in paths:
        addDirs(p)

    addBuildoutDefaultConfig(path)

    path += 'configs/' + plone_vs + '/'
    if not fileExists(path): addDirs(path); getConfigs(plone_vs, path)

    os.system('ln -s ' + path + 'versions.cfg ' + paths[-1] + 'versions.cfg')


def addPloneSkel(plone_vs, path):
    """ """
    os.system('touch ' + path + 'buildout.cfg')

    path = getHome() + '.virtenv/'
    if not fileExists(path): installBuildout(path)

    path = getHome() + '.buildout/'
    if not fileExists(path): addBuildoutSkel(plone_vs, path)


