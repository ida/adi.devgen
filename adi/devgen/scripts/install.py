# -*- coding: utf-8 -*-

import os

from adi.commons.commons import addFile
from adi.commons.commons import addDirs
from adi.commons.commons import delFile
from adi.commons.commons import getFirstChildrenPaths
from adi.commons.commons import getHome
from adi.commons.commons import getStr
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
    extends-section, for more urls, until all configs are downloaded.
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

def replaceAbsoluteUrlsWithRelPath(string):
    """
    Replace an absolute URL like:
        'https://doma.in/folder/file.py'
    With:
        'file.py'
    """
    new_string = ''
    last_slash_pos = None
    i = 0
    while i < len(string):
        # The current position is the start of an url:
        if string[i:i+7] == 'http://' \
        or string[i:i+7] == 'https:/':
            # As long string lasts and it's not a space...
            while i < len(string) and string[i] != ' ':
            # ... move index-position in string one step forward:
                i += 1
                # If the character of the current position is a slash...
                if string[i] == '/':
                    # ... remember last found slash-pos:
                    last_slash_pos = i
            # Either string ended or a space is encountered, then URL-str
            # ended, collect relative-url to new_string:
            new_string += string[last_slash_pos + 1:i] # +1 to omit slash
        # The current position is not the start of an url ...
        else: # ... collect current character:
            new_string += string[i]
        i += 1
    return new_string

def makeConfigsUrlsLocal(configs_path):
    """
    A line containing one or more URLs, like e.g.:

    extends = http://dist.plone.org/versions/zope-2-13-24-versions.cfg

    Is replaced with orig-line as comment and a new-line containing rel-path:

    # extends = http://dist.plone.org/versions/zope-2-13-24-versions.cfg
    extends = zopeapp-versions.cfg

    TODO:
    This works as long as referenced filenames are not the same, in Plone-4.2.x
    two 'versions.cfg' are referenced. Would need url-comparison and changing
    file-names.
    """
    configs_paths = getFirstChildrenPaths(configs_path)
    for config_path in configs_paths:
        string = getStr(config_path)
        string = replaceAbsoluteUrlsWithRelPath(string)
        addFile(config_path, string, True)

def addBuildout(plone_vs):
    """
    Create $HOME/[path]. In it create default.cfg, eggs, deveggs, configs and a
    virtenv. Install buildout with the latter.
    """
    # Prep paths:
    config_url = 'http://dist.plone.org/release/' + plone_vs + '/versions.cfg'
    buildout_defaults_path = getHome() + '.buildout/'
    all_dir_paths = [
        buildout_defaults_path,
        buildout_defaults_path + 'eggs/',
        buildout_defaults_path + 'deveggs/',
        buildout_defaults_path + 'configs/']

    # Create dirs:
    for path in all_dir_paths: addDirs(path)

    # Create virtenv:
    if not fileExists(buildout_defaults_path + 'virtenv'):
        installBuildout(buildout_defaults_path + 'virtenv/')

    # Create confs:
    configs_path = buildout_defaults_path + 'configs/' + plone_vs + '/'
    if not fileExists(configs_path):
        addDirs(configs_path)
        getConfigs(config_url, configs_path)
        makeConfigsUrlsLocal(configs_path)

    # Create default-conf:
    addBuildoutDefaultConfig(plone_vs, buildout_defaults_path)

