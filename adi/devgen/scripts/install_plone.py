import os
from commons.commons import *

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
                    print 'OLD' + line
                    print 'NEW' + new_line
                    new_lines.append('#' + line + indent + new_line)
            else:
                new_lines.append(line)
        string = ''.join(new_lines)
        tmpfil = config_path + '.tmp'
        if fileExists(tmpfil):
            delFile(tmpfil)
        addFile(tmpfil, string)


def addPloneSkel(container, plone_version):

    # NAMES
    instance_name = 'plone-instance'
    shared_name = '.shared'
    
    deveggs_name = 'dev-addons'
    eggs_name = 'eggs'
    configs_name = 'configs/' + plone_version
    virtenv_name = 'virtenv'

    # PATHS
    instance_path = container + instance_name + '/'
    shared_path = container + shared_name + '/'
    
    deveggs_path = container + deveggs_name + '/'
    eggs_path = shared_path + eggs_name + '/'
    configs_path = shared_path + configs_name + '/'
    virtenv_path = shared_path + virtenv_name + '/'
    buildout_path = virtenv_path + 'bin/buildout'


    # ACTION
#    if fileExists(container): delDirs(container); print 'DEV: destroy' #DEV
#    paths = [instance_path, deveggs_path, shared_path, eggs_path, configs_path]
#    createFolders(paths)
#    installBuildout(virtenv_path)
#    getConfigs(configs_path, plone_version)
    makeConfigsUrlsLocal(configs_path)

def main(container, plone_version):
    if not container.endswith('/'): container += '/'
    addPloneSkel(container, plone_version)

if __name__ == '__main__':
    main('puildout', '4.3.4')
