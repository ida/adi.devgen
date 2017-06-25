#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from adi.commons.commons import addDirs
from adi.commons.commons import getFirstChildrenPaths
from adi.commons.commons import getHome
from adi.commons.commons import getStr
from adi.commons.commons import fileExists
from adi.commons.commons import isUpcomingWord
from adi.commons.commons import writeFile

from adi.devgen.scripts.create import addBuildoutDefaultConfig


def addBuildout(plone_vs):
    """
    Create $HOME/[path]. In it create default.cfg, eggs, deveggs, configs and a
    virtenv. Install buildout with the latter.
    """
    local_configs_names = []
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
        # Replace extends-section with local-paths of all configs:
        configs_paths = getFirstChildrenPaths(configs_path)
        for cpath in configs_paths:
            cpath = cpath.split('/')[-1]
            if cpath != 'versions.cfg': # exclude possible ref of main-config
                local_configs_names.append(cpath)
        replaceExtends(configs_path + 'versions.cfg', local_configs_names)

    # Create default-conf:
    addBuildoutDefaultConfig(plone_vs, buildout_defaults_path)

def getConfigs(versions_url, configs_path):
    """
    Download versions.cfg, look for the referenced other configs in its
    extends-section, also downloads these configs and look in their
    extends-section, for more urls, until all configs are downloaded.
    Replaces all found extends-section with nothing and sets the extends-
    section of versions.cfg with all local paths of found configs in
    config-directory.
    With local-paths we can operate in offline-mode when running buildout,
    which makes running buildout much faster.
    """
    all_urls = [versions_url]
    urls = [versions_url]
    while urls:
        url = urls.pop(0)
        file_name = url.split('/')[-1]
        file_path = configs_path + file_name
        if not fileExists(file_path):
            os.system('wget ' + url + ' -P ' + configs_path)
            string = getStr(file_path)
            posis = getExtendsPosis(string)
            extends_content = string[posis[0]:posis[1]]
            read_urls = getExtendsUrls(extends_content)
            replaceExtends(file_path, []) # empty extends-section
            for read_url in read_urls:
                read_name = read_url.split('/')[-1]
                if not fileExists(configs_path + read_name):
                    urls.append(read_url)

def getExtendsPosis(string):
    """
    Return start- and end-position of a buildout-config's
    extends-section's content.
    """
    extends_content_end_pos = 0
    extends_content_start_pos = 0
    i = 0
    while i < len(string):
        if isUpcomingWord(string, i, 'extends'):
            while string[i] != '=':
                i += 1
            i += 2
            extends_content_start_pos = i
        if extends_content_start_pos > 0:
            if string[i] == '[':
                extends_content_end_pos = i - 1
                break
            elif string[i] == '=':
                while string[i-1] == ' ':
                    i -= 1
                i -= 1
                while i < 0 and string[i] != ' ' or string[i] != '\n':
                    i -= 1
                extends_content_end_pos = i
                break
        i += 1
    return extends_content_start_pos, extends_content_end_pos

def getExtendsUrls(extends_content):
    """Extract the urls of the extends-section as a list."""
    urls  = []
    extends_content = extends_content.split() # split by spaces
    for url in extends_content:
        if url.endswith(','): # remove possible commas of one-liners
            url = url[:-1]
        urls.append(url)
    return urls

def installBuildout(virtenv_path):
    if not virtenv_path.endswith('/'): virtenv_path += '/'
    os.system('virtualenv ' + virtenv_path)
    os.system(virtenv_path + 'bin/pip install setuptools -U')
    os.system(virtenv_path + 'bin/pip install zc.buildout')

def replaceExtends(path, configs_paths):
    """
    Replace the extends-section of a buildout-config with
    the stringified passed list of paths.
    """
    string = getStr(path)
    posis = getExtendsPosis(string)
    configs_paths = '\n    ' + '\n    '.join(configs_paths) + '\n'
    string = string[:posis[0]] + configs_paths + string[posis[1]:]
    writeFile(path, string)

