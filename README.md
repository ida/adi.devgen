Introduction
============

Yet another command-line Plone-Add-On-Generator, just the way I like it:

No dependencies, some Python-methods, that's all.


Installation
=============

Add 'adi.devgen' to the eggs-section in your buildout-config, run buildout.

As not released yet, clone it and add it as a development-egg, also to buildout.


Usage
=====

You'll now find an executable called 'devgen' in your instance's bin-folder,
type 'devgen' only, to get further help on how to use devgen:

    $ path/to/instance/bin/devgen


Some examples in the following...


    $ ./path/to/your/instance/bin/devgen addSkinSkel your.addon

Creates an installable Plone-Addon, with a stylesheet, a javascript and a template in a skin folder.
In contrary to browser-based resources, you won't need to empty the browser's cache on a reload, after changing your stylesheet or javascript.


    $ ./path/to/your/instance/bin/devgen addBrowserSkel your.addon

Creates an installable Plone-Addon, with a stylesheet and a javascript in a browser's resource-folder.
You'll want that for complex sites, where things are likely to go haywire and binding resources to an interface is a good idea.


    $ ./path/to/your/instance/bin/devgen addInstallSkel your.addon

Creates an installable add-on, that is: Holds a profile for the quickinstaller.


    $ ./path/to/your/instance/bin/devgen addBaseSkel your.addon

Creates a base skeleton for a Python-egg, installable via buildout.


Local commands (executed of within the addon)
---------------------------------------------

    $ ./path/to/your/instance/bin/devgen addDep collective.bestaddonever

Registers 'collective.bestaddonever' as a dependency to the addon.


Note
----

Optionally you can specify a path, just append it to the command as an additional argument,
otherwise it is assumed you are inside of the addon or for an addon-creation,
it'll create it in the current directory, where you execute `devgen`.


TODO
====

- Regard more than one dotted namespace for addon.

- Add meta-stuff like doc's folder, to be ready for publication.

- Split methods into smaller reusable chunks.

- Get setup.py-properties infos of a local default-config, say, if present in '$HOME/.buildout'.

- Possibly transfer:
https://github.com/ida/skriptz/blob/master/plone/addBrowser.py
and
https://github.com/ida/skriptz/blob/master/plone/Dexterity/addField.py


