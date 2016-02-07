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
    if not virtenv_path.endswith('/'): virtenv_path += '/'
    os.system('virtualenv ' + virtenv_path)
    os.system(virtenv_path + 'bin/pip install setuptools -U')
    os.system(virtenv_path + 'bin/pip install zc.buildout')

def getConfigs(versions_url, configs_path):
    """
    Download versions.cfg, looks for the referenced other configs in its
    extends-section, also downloads these configs  and looks in their
    extends-section, for more urls, until all configs are downoladed.
    """
    urls = [versions_url]
    while urls:
        url = urls.pop(0)
        fname = url.split('/')[-1]
        fpath = configs_path + fname
        if not fileExists(fpath):
            os.system('wget ' + url + ' -P ' + configs_path)
            string = open(fpath).read();
            read_urls = getUrls(string)
            for read_url in read_urls:
                read_name = read_url.split('/')[-1]
                if not fileExists(configs_path + read_name):
                    urls.append(read_url)

def makeConfigsUrlsLocal(configs_path):
    """
    Change 'http://blabla/config.cfg' to 'config.cfg'
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

def addBuildout(plone_vs):
    """
    Create $HOME/[path]. In it create default.cfg, eggs, deveggs, configs and a
    virtenv. Install buildout with the latter.
    """
    # Prep paths:
    url = 'http://dist.plone.org/release/' + plone_vs + '/versions.cfg'
    path = getHome() + '.buildout/'
    paths = [path, path + 'eggs/', path + 'deveggs/', path + 'configs/']

    # Create dirs:
    for p in paths: addDirs(p)

    # Create virtenv:
    if not fileExists(path + 'virtenv'): installBuildout(path + 'virtenv/')

    # Create confs:
    configs_path = path + 'configs/' + plone_vs + '/'
    if not fileExists(configs_path):
        addDirs(configs_path)
        getConfigs(url, configs_path)
        makeConfigsUrlsLocal(configs_path)

    # Create default-conf:
    addBuildoutDefaultConfig(plone_vs, path)

def addPlone(plone_vs, path):
    """Checks, if shared buildout-sources are available and adds a buildout.cfg to directory."""
    addBuildoutSkel(plone_vs)
    if not fileExists(path): addDirs(path)
    os.system('touch ' + path + 'buildout.cfg')

