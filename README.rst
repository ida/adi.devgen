Introduction
============

Yet another command-line Plone-Add-On-Generator, just the way I like it:

No dependencies, no possible conflicts, some Python-methods, that's all.



Installation
=============

    pip install adi.devgen


Development-versions:

    pip install -e git+https://github.com/ida/adi.devgen.git#egg=adi.devgen
    pip install -e git+https://github.com/ida/adi.commons.git#egg=adi.commons


Alternatively add `adi.devgen` as an egg to your buildout, then
the `devgen`-executable will be available in its bin-directory, of
which you can call it then, like: `./bin/devgen`.


Configuration
=============

If a file '~/.buildout/devgen.cfg' is present, values will be read of it and
inserted into the `setup.py` of an addon. Its format is expected to be like:

author=Arbi Trary

author_email=arbi@tra.ry

url=https://github.com/arbitrary/your.addon


Usage
=====

Type the command alone, to get a list of the available generator-functions:

    $ devgen


To get a choosen function's help-text, type:

    $ devgen [FUNCTION_NAME] help


Examples
========

Create boilerplate for an addon, that can do nothing, but be installed in a Plonesite:

    $ devgen addProfileSkel your.addon


Create it not in the directory, where you are, but somewhere else:

    $ devgen addProfileSkel /some/where/else/your.addon


Register another addon as a dependency to your addon:

    $ devgen addDep collective.bestaddonever some/where/your.addon

Or, first locate into your addon, then you can omit the appended path:

    $ cd your.addon
    $ devgen addDep collective.bestaddonever

Register and add a browser-based stylesheet named 'main.css' in
'your.addon/your/addon/browser/resources':

    $ devgen addCss

Register and add a browser-based Javascript named 'magic.js' in
'your.addon/your/addon/browser/resources':

    $ devgen addJS magic


TODO
====

- Regard more than one dotted namespace for addon.

- Possibly transfer:
https://github.com/ida/skriptz/blob/master/plone/Dexterity/addField.py

