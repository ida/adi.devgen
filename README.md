Introduction
============

Yet another command-line Plone-Add-On-Generator, just the way I like it:

No dependencies, some Python-methods, that's all.


Installation
=============

With lovely pip, as easy as:

    $ pip install -e git+https://github.com/ida/adi.devgen.git#egg=adi.devgen


If you haven't installed pip, yet, do it. For Ubuntu that is:

    $ sudo apt-get install python-pip -y

Or for Fedora:

    $ sudo yum install python-pip -y


Usage
=====


Type the command alone, to get a help-text, what it can do for you:

    $ devgen


Examples
========


- Create boilerplate for an addon, that can do nothing,  but be installed in a Plonesite:

    $ devgen addProfileSkel your.addon

- Create it not in the driectory, where you are, but somewhere else:

    $ devgen addProfileSkel your.addon /some/where/else

- Register another addon as a dependency to your addon:

    $ devgen addDep collective.bestaddonever your.addon

- Or, first locate into your addon, then you can omit the appended path (defaults to '.'):

    $ cd your.addon
    $ devgen addDep collective.bestaddonever


- Create an installable Plone-Addon, with a stylesheet, a javascript and a template in a skin folder:

    $ devgen addSkinSkel your.addon

In contrary to browser-based resources, you won't need to empty the browser's cache on a reload, after changing your stylesheet or javascript.


- Create an installable Plone-Addon, with a stylesheet and a javascript in a browser's resource-folder.

    $ devgen addBrowserSkel your.addon


- Add docs-folder and read defaults for setup.py:

    $ devgen addMetaSkel

If a file '~/.buildout/devgen.cfg' is present, values will be read of it and inserted to setup.py.
Its format is expected to be like:

author=Arbi Trary
author_email=arbi@tra.ry
url=https://github.com/arbitrary/your.addon


TODO
====

- Regard more than one dotted namespace for addon.

- Split methods into smaller reusable chunks.

- Possibly transfer:
https://github.com/ida/skriptz/blob/master/plone/Dexterity/addField.py

