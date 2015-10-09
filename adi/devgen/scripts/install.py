import os

from adi.commons.commons import addFile
from adi.commons.commons import addDirs
from adi.commons.commons import delFile
from adi.commons.commons import getFirstChildrenPaths
from adi.commons.commons import getIndent
from adi.commons.commons import getLines
from adi.commons.commons import getUrls
from adi.commons.commons import getRealPath
from adi.commons.commons import fileExists
from adi.commons.commons import hasStr

from adi.devgen.scripts.create import addBuildoutConfig

def addBuildoutDefault(plone_version, path):
    string = """[buildout]
parts =
    instance
    plonesite

extends = configs/plone/""" + plone_version + """/versions.cfg

eggs-directory = """ + + """/.buildout/.eggs

versions = versions

#develop = src/dev.addon

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
#    dev.addon
    Pillow
    Plone
    plone.reload
zcml =
    plone.reload

[plonesite]
# Newest (1.9.1) breaks layout, when autoinstall devegg:
recipe = collective.recipe.plonesite == 1.9.0
#products = dev.addon

[versions]
# Overcome neverending setuptools-conflict-hell,
# thanks to thet and pbauer, see github.com/minimalplone4:
zc.buildout = >= 2.2.1
setuptools = >= 2.2
"""
    addFile(path + 'buildout.cfg', string)

def createFolders(paths):
    for path in paths:
        addDirs(path)

def installBuildout(virtenv_path):
    os.system('virtualenv ' + virtenv_path)
    os.system(virtenv_path + 'bin/pip install setuptools -U')
    os.system(virtenv_path + 'bin/pip install zc.buildout')

def getConfigs(configs_path, plone_version):
    """Downloads versions.cfg and also gets the other
       configs referenced in its 'extends'-var, too,
       so we can work offline and let buildout run even faster.
    """
    versions_name = 'versions.cfg'
    versions_url = 'http://dist.plone.org/release/' + plone_version + '/' + versions_name
    os.system('wget ' + versions_url + ' -P ' + configs_path)
    versions_path = configs_path + '/versions.cfg'
    string = open(versions_path).read();
    urls = getUrls(string)
    for url in urls:
        os.system('wget ' + url + ' -P ' + configs_path)

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


def addPloneSkel(plone_version, path='.'):

    path = getRealPath(path)

    # NAMES
    instance_name = 'plone-instance'
    shared_name = '.shared'
    
    deveggs_name = 'dev-addons'
    eggs_name = 'eggs'
    configs_name = 'configs/' + plone_version
    virtenv_name = 'virtenv'

    # PATHS
    instance_path = path + instance_name + '/'
    shared_path = path + shared_name + '/'
    
    deveggs_path = path + deveggs_name + '/'
    eggs_path = shared_path + eggs_name + '/'
    configs_path = shared_path + configs_name + '/'
    virtenv_path = shared_path + virtenv_name + '/'
    buildout_path = virtenv_path + 'bin/buildout'

    # ACTION
#    if fileExists(path): delDirs(path); print 'DEV: destroy' #DEV
    paths = [instance_path, deveggs_path, shared_path, eggs_path, configs_path]
    createFolders(paths)
    installBuildout(virtenv_path)
    getConfigs(configs_path, plone_version)
    makeConfigsUrlsLocal(configs_path)
    addBuildoutConfig(plone_version, instance_path)
    os.system('cd ' + instance_path + ';' + virtenv_path + 'bin/buildout;./bin/instance fg')
