Changelog
=========

1.6 (unreleased)
----------------

- deploy()& doOnRemote(): Better docstrs.. [ida]
- deploy()/doOnRemote(): Add ssh_port as para in case it doesn't default to 22.. [ida]
- Add convention getEggCachePaths().. [ida]
- Nothing changed yet.


1.5 (2017-06-07)
----------------

- Do not reference versions.cfg in versions.cfg, results in infinite loop. [ida]


1.4 (2017-06-06)
----------------

- Adjust addBuildout() to parse extends-sections, instead of unsharply finding patterns,
  now works also for Plone-5-builds.

- Fix addPlone(): Add extends-part to a build's default buildout.cfg,
  pointing to the used versions.cfg, defining the Plone-version.


1.3 (2017-05-11)
----------------

- Improve addPlone() and deploy(). [ida]

- Add isView() and improve idExists-methods. [ida]

- Add getChildPosInParent() and getChildPosInParents() [ida]


1.2 (2016-10-21)
----------------

- Add workflow-related helper-methods. [ida]


1.1 (2016-07-10)
----------------

- Last release was a brown bag, pardon.

- Add addNChildrenRecursive(), delDep(), deploy(), getField(), getFields(),
  getUserId(),

- Fix skin-path name, so templates get immediately callable after added to product.

- Fix isIniInstall() in addInstallScript().

- Improve addInstallScript()

- Regard if browser-skel is missing in addView().

- Show complete name, not just first name in quickinstaller.

- Add eggtractor, add develop-section in default-buildout-conf,
  increase default plone-vs.


1.0 (2016-05-14)
----------------

- Add doOnRemote(), squash() and getUnpushedCommits().

- Fix "cannot find virtenv" in addPlone().

- Re-add default-filename "main" for generating stylesheet, Javascript,
  Python-script and a template via addOn().

- Fix, if browserlayer is missing in addCss() and addJs().


0.9 (2015-11-18)
----------------

- Add addView().

- Add default-values of a function's expected arguments to help-msg.

- Fix path: Use dot instead of slash, for a resources' paths in
  js-registry-generation.

- Let getAddonPath() fail with an exit, to prevent further
  code-executions.

- Rename addBrowserSkel() to addBrowser(), addSkinSkel() to addSkin,
  and so on, for less typing.

- Fix addBrowser() and addSkin() from scratch – if not added on top of existing
  addon.

- Improve addAndRegisterView().


0.8 (151002)
------------

- Generate missing browser-slug in config.

- Change docs from MD-format to RST, as pypi requires.

- Add addCss() and addJs().


0.7 (150926)
------------

- Fix missing import and typo in setup.py-generation, which broke addons-installs.


0.6 (150923)
------------

- Update README, improve installPlone().


0.5 (150921)
------------

- Fix imports, better hlp-msgs, improve installPlone().


0.4 (150920)
------------

- Update README


0.3 (150920)
------------

- Fix changed import-paths.


0.2 (150920)
------------

- Add adi.commons as dependency.


0.1 (150920)
------------

- Initial release

