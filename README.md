Introduction
============

Yet another command-line Plone-Add-On-Generator, just the way I like it:

No dependencies, no possible conflicts, some Python-methods, that's all.



Installation
=============

    pip install adi.devgen


Alternatively add `adi.devgen` as an egg to your buildout, then
the `devgen`-executable should be available in its bin-directory.

Development-versions:

    pip install -e git+https://github.com/ida/adi.devgen.git#egg=adi.devgen
    pip install -e git+https://github.com/ida/adi.commons.git#egg=adi.commons


Usage
=====

Type the command alone, to get a help-text, what it can do for you:

    $ devgen


That'll also lists the available generator-functions, to get a function's help-text, type:

    $ devgen [FUNCTION_NAME]


Examples
========

Create boilerplate for an addon, that can do nothing, but be installed in a Plonesite:

    $ devgen addProfileSkel your.addon


Create it not in the directory, where you are, but somewhere else:

    $ devgen addProfileSkel /some/where/else/your.addon


Register another addon as a dependency to your addon:

    $ devgen addDep collective.bestaddonever your.addon

Or, first locate into your addon, then you can omit the appended path (defaults to '.'):

    $ cd your.addon
    $ devgen addDep collective.bestaddonever


Create an installable Plone-Addon, with a stylesheet, a javascript and a template in a skin folder:

    $ devgen addSkinSkel your.addon

In contrary to browser-based resources, you won't need to empty the browser's cache on a reload, after changing your stylesheet or javascript.


Create an installable Plone-Addon, with a stylesheet and a javascript in a browser's resource-folder.

    $ devgen addBrowserSkel your.addon


Add docs-folder and read defaults for setup.py of a config:

    $ devgen addMetaSkel

If a file '~/.buildout/devgen.cfg' is present, values will be read of it and inserted to setup.py. Its format is expected to be like:

author=Arbi Trary

author_email=arbi@tra.ry

url=https://github.com/arbitrary/your.addon


TODO
====

- Regard more than one dotted namespace for addon.

- Split functions into smaller reusable chunks.

- Possibly transfer:
https://github.com/ida/skriptz/blob/master/plone/Dexterity/addField.py

