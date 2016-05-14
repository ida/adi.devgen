Introduction
============

Yet another command-line Plone-Add-On-Generator.

Hop right to the chapters "Usage" and "Examples " below,
to get an impression of what it can do.


Motivation
==========

While paster and zopeskel have served us well for a long time, at some point
there were too often conflicts, due to some of its dependencies.
This package doesn't have any dependencies, so all ever possible occuring
problems can safely be attributed to itself.

Additionally it was desirable to be able to execute any Plone-addon-extending
command of within any location of an addon. Or, of outside of an addon, by
prependning the path to the addon to the command, so one doesn't necessarily
need to change directories and executing a command doesn't require you to be in
a certain directory.

Besides of Plone-addon-related helper-functions, there are also functions more
general related to developing, like `doOnRemote()`, `getRepos()`, 
`squashCommits()`, a.s.o.

Setting up a new Plone-instance is as easy as `addPlone()`, will download the
configs for buildout locally and set buildout's mode to 'offline', so we save
time, whenever running buildout, because it will not look up the configs of
remote addresses, like usually, as time is honey.


Installation
=============

Stable-version:
--------------

From the commandline execute::

    pip install adi.devgen


Develop-version:
----------------

::
    pip install -e git+https://github.com/ida/adi.devgen.git#egg=adi.devgen


The latest state of this package will be added to a directory (a.k.a. folder)
called 'src', which lives, where your pip lives. To find out where your pip
lives, type `which pip` into your console. You can then change the code inside
of the src-directory and get the effects immediately.



Configuration / Presettings
===========================

When creating a new addon and a file '~/.buildout/devgen.cfg' is present,
values will be read of it and inserted into the `setup.py` of the addon.
The file-contents' format must be like this::

author=Arbi Trary
author_email=arbi@tra.ry
url=https://github.com/arbitrary/your.addon


Usage
=====

Type the command alone, to get a list of the available generator-functions::

    devgen


To get a choosen function's help-text, type::

    devgen [FUNCTION_NAME] help


Examples
========

Create boilerplate for an addon, that can do nothing, but be installed in a Plonesite::

    devgen addProfile your.addon


Create it not in the directory, where you are, but somewhere else::

    devgen addProfile some/where/else/your.addon


Register another addon as a dependency to your addon::

    devgen addDep collective.bestaddonever some/where/your.addon

Or, first locate into your addon, then you can omit the appended path::

    cd your.addon
    devgen addDep collective.bestaddonever

By the way, most commands work of within any location inside of an addon
and no need to pass a path.

Register and add a browser-based stylesheet named 'main.css' in
'your.addon/your/addon/browser/resources'::

    devgen addCss

Register and add a browser-based Javascript named 'magic.js' in
'your.addon/your/addon/browser/resources'::

    devgen addJS magic

Register and add a browser-based Template named 'main.pt' and a
Python-script named 'main.py' with an example how to retrieve a
computed value of the script in the template via TAL, in:
'your.addon/your/addon/browser/resources'::

    devgen addView

The view can then be called in a browser like this::

    http://localhost:8080/Plone/++resource++your.addon.resources/your_addon_main_view

Where 'main' is the default name for the files, you can choose any other::

    devgen addView any_other

That'll result to::

    http://localhost:8080/Plone/++resource++your.addon.resources/your_addon_any_other_view


TODO
====

- Regard more than one-dotted-namespace for addon.

- Possibly transfer:
https://github.com/ida/skriptz/blob/master/plone/Dexterity/addField.py

