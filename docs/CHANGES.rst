Changelog
=========

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

