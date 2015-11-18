import os

from adi.commons.commons import addFile
from adi.commons.commons import fileHasStr
from adi.commons.commons import fileExists
from adi.commons.commons import getLines
from adi.commons.commons import getHome
from adi.commons.commons import insertAfterFirstLine
from adi.commons.commons import insertAfterLine
from adi.commons.commons import insertBeforeLine
from adi.commons.commons import insertBeforeLastTag

from adi.devgen.scripts.conventions import getAddonName
from adi.devgen.scripts.conventions import getAddonFirstName
from adi.devgen.scripts.conventions import getAddonPath
from adi.devgen.scripts.conventions import getBrowserPath
from adi.devgen.scripts.conventions import getConfigPath
from adi.devgen.scripts.conventions import getLastLvlPath
from adi.devgen.scripts.conventions import getProfilePath
from adi.devgen.scripts.conventions import getResourcesPath
from adi.devgen.scripts.conventions import getSkinPath
from adi.devgen.scripts.conventions import getUnderscoredName
from adi.devgen.scripts.conventions import getUppercasedName

def addSetupPy(path):
    """Add skel for setup.py in root-folder of addon."""
    addon_name = path.split('/')[-2]
    addon_first_name = addon_name.split('.')[0]
    string = '\
from setuptools import setup, find_packages\n\
import os\n\
\n\
version = \'0.1.dev0\'\n\
\n\
long_description = \'\'\n\
if os.path.exists("README.rst"):\n\
    long_description = open("README.rst").read()\n\
\n\
setup(name=\'' + addon_name + '\',\n\
      version=version,\n\
      description="",\n\
      long_description=long_description,\n\
      classifiers=[\n\
        "Framework :: Plone",\n\
        "Programming Language :: Python",\n\
        ],\n\
      keywords=\'\',\n\
      author=\'\',\n\
      author_email=\'\',\n\
      url=\'https://github.com/collective/\',\n\
      license=\'GPL\',\n\
      packages=find_packages(exclude=[\'ez_setup\']),\n\
      namespace_packages=[\'' + addon_first_name + '\'],\n\
      include_package_data=True,\n\
      zip_safe=False,\n\
      install_requires=[\n\
          \'setuptools\',\n\
      ],\n\
      entry_points="""\n\
      # -*- Entry points: -*-\n\
\n\
      [z3c.autoinclude.plugin]\n\
      target = plone\n\
      """,\n\
      )\n'
    addFile(path + 'setup.py', string)

def addDocs(path):
    """Add doc-folder containing 'CHANGES.rst', 'INSTALL.rst' and 'USAGE.rst'."""
    addFile(path + 'docs/CHANGES.rst', """Changelog for """ + getAddonName(path) + """\n==================
0.1.dev0 (unreleased)
---------------------

- Initial commit.
    
""")
    addFile(path + 'docs/INSTALL.rst', 'Installation\n===========\n')
    addFile(path + 'docs/USAGE.rst', 'Usage\n=====\n')

def addFirstInit(path):
    string = '\
# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages\n\
try:\n\
    __import__(\'pkg_resources\').declare_namespace(__name__)\n\
except ImportError:\n\
    from pkgutil import extend_path\n\
    __path__ = extend_path(__path__, __name__)\n'
    addFile(path + '__init__.py', string)

def addLastInit(path):
    string = '\
def initialize(context):\n\
    """Initializer called when used as a Zope 2 product."""\n'
    addFile(path + '__init__.py', string)

def addConfig(path):
    addon_name = getAddonName(path)
    string = '\
<configure\n\
    xmlns="http://namespaces.zope.org/zope"\n\
    xmlns:five="http://namespaces.zope.org/five"\n\
    xmlns:i18n="http://namespaces.zope.org/i18n"\n\
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"\n\
    i18n_domain="' + getAddonName(path) + '">\n\
\n\
  <five:registerPackage package="." initialize=".initialize" />\n\
\n\
</configure>\n'
    addFile(path + 'configure.zcml', string)

def registerBrowser(path):
    """Register 'browser'-directory in an addon's main configure.zcml."""
    string = '<include package=".browser" />'
    if not fileHasStr(getConfigPath(path), string):
        insertBeforeLine(getConfigPath(path), '</configure>', string)

def registerProfile(path):
    """Register 'profiles/default' in an addon's main configure.zcml."""
    string = '\n\
  <genericsetup:registerProfile\n\
      name="default"\n\
      title="' + getAddonName(path) + '"\n\
      directory="profiles/default"\n\
      description="Installs the ' + getAddonFirstName(path) + ' package"\n\
      provides="Products.GenericSetup.interfaces.EXTENSION"\n\
      />\n'
    fil = getLastLvlPath(path) + 'configure.zcml'
    if not fileExists(fil): addConfig(getLastLvlPath(path))
    insertBeforeLastTag(fil, string)
    
def addMetadata(path):
    """Add metadata.xml to a profile."""
    string = '\
<?xml version="1.0"?>\n\
<metadata>\n\
  <version>1000</version>\n\
  <dependencies>\n\
  </dependencies>\n\
</metadata>\n'
    if not fileExists(getProfilePath(path) + 'metadata.xml'):
        addFile(getProfilePath(path) + 'metadata.xml', string)

def addSkinFiles(path):
    """Register skin-folder in configure.zcml and add metadata.xml to profile."""
    conf = getLastLvlPath(path) + 'configure.zcml'
    if not fileExists(conf): addConfig(getLastLvlPath(path))
    insertAfterFirstLine(conf, '    xmlns:cmf="http://namespaces.zope.org/cmf"\n')
    insertBeforeLastTag(conf, '\n  <cmf:registerDirectory name="' + getUnderscoredName(path) + '"/>\n\n')
    string = '\
<object name="portal_skins">\n\
<object name="' + getUnderscoredName(path) + '"\n\
meta_type="Filesystem Directory View"\n\
directory="' + getAddonName(path) + ':skins/' + getUnderscoredName(path) + '"/>\n\
\n\
<skin-path name="' + getAddonName(path) + '" based-on="Sunburst Theme">\n\
<layer name="' + getUnderscoredName(path) + '" insert-after="custom"/>\n\
\n\
</skin-path>\n\
\n\
</object>'
    addFile(getProfilePath(path) + 'skins.xml', string)
    addSkinResources(path)

def addSkinResources(path):
    """ Adds a stylesheet, a javascript and a template to the skin
        and registers them.
    """
    # Add stylesheet:
    string = 'body:before{content:"Congrats, ' + getUnderscoredName(path) + '.css has been loaded succesfully!"}'
    addFile(getSkinPath(path) + getUnderscoredName(path) + '.css', string)
    # Register stylesheet:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_css">\n\
 <stylesheet title=""\n\
    id="portal_skins/'+ getUnderscoredName(path) + '/' + getUnderscoredName(path) + '.css"\n\
    media="screen" rel="stylesheet" rendering="link"\n\
    cacheable="True" compression="safe" cookable="True"\n\
    enabled="1" expression=""/>\n\
\n\
</object>'
    addFile(getProfilePath(path) + 'cssregistry.xml', string)
    # Add javascript:
    string = '\
(function($) {\n\
        $(document).ready(function() {\n\
            $("#visual-portal-wrapper").prepend("Congrats, ' + getUnderscoredName(path) + '.js has been loaded succesfully!")\n\
        }); //docready\n\
})(jQuery);'
    addFile(getSkinPath(path) + getUnderscoredName(path) + '.js', string)
    # Register javascript:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_javascripts">\n\
 <javascript authenticated="False" cacheable="True" compression="none"\n\
    conditionalcomment="" cookable="True" enabled="True" expression=""\n\
    id="portal_skins/'+ getUnderscoredName(path) + '/' + getUnderscoredName(path) + '.js"\n\
    inline="False"/>\n\
</object>'
    addFile(getProfilePath(path) + 'jsregistry.xml', string)
    # Add template:
    addFile(getSkinPath(path) + getUnderscoredName(path) + '.pt', 'Soyo templado di addon.')
    # Will be accessible via: 'http://host:8080/site/[...]/portal_skins/example_addon/example_addon')

def addBrowserConf(path):
    """Add configure.zcml to browser-directory."""
    addon_name = getAddonName(path)
    string= '<configure\n\
 xmlns="http://namespaces.zope.org/zope"\n\
 xmlns:five="http://namespaces.zope.org/five"\n\
 xmlns:browser="http://namespaces.zope.org/browser"\n\
 i18n_domain="' + addon_name + '">\n\
\n\
    <include package="plone.app.contentmenu" />\n\
    <browser:resourceDirectory\n\
        name="' + addon_name + '.resources"\n\
        directory="resources"\n\
      />\n\
\n\
\n</configure>'
    addFile(getBrowserPath(path) + 'configure.zcml', string)

def addAndRegisterCss(filename, path):
    """Register and add browser-based CSS-file with 'has-loaded'-content."""
    string = '<stylesheet title=""\n\
    id="++resource++' + getAddonName(path) + '.resources/' + filename + '.css"\n\
    media="screen" rel="stylesheet" rendering="import"\n\
    cacheable="True" compression="safe" cookable="True"\n\
    enabled="1" expression=""/>\n'
    insertBeforeLastTag(getProfilePath(path) + 'cssregistry.xml', string)
    string = '#visual-portal-wrapper:before{content:"++resource++' +\
              getAddonName(path) + '.resources/' + filename + '.css loaded"}'
    addFile(getResourcesPath(path) + filename + '.css', string)

def addAndRegisterJs(filename, path):
    """Register and add browser-based JS-file with 'has-loaded'-content."""
    string = '<javascript authenticated="False" cacheable="True" compression="none"\n\
    conditionalcomment="" cookable="True" enabled="True" expression=""\n\
    id="++resource++' + getAddonName(path) + '.resources/' + filename + '.js"\n\
    inline="False"/>\n'
    insertBeforeLastTag(getProfilePath(path) + 'jsregistry.xml', string)
    string = '\
(function($) {\n\
        $(document).ready(function() {\n\
            $("<div>++resource++' + getAddonName(path) + '.resources/' + \
filename + '.js loaded</div>").insertBefore("#visual-portal-wrapper")\n\
        }); //docready\n\
})(jQuery);\n'
    addFile(getResourcesPath(path) + filename + '.js', string)

def addAndRegisterView(filename, path):
    """Register and add browser-based view with an associated template."""
    addFile(getResourcesPath(path) + '__init__.py', '')
    string = '''
    <browser:page
        for="*"
        name="''' + getUnderscoredName(path) + '''_''' + filename + '''_view"
        class=".resources.''' + filename + '''.View"
        permission="zope2.View"
        layer="''' + getAddonName(path) + '''.interfaces.I''' +\
        getUppercasedName(path) + '''"
      />

'''
    insertBeforeLastTag(getBrowserPath(path) + 'configure.zcml', string)
    string = '''from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("''' + filename + '''.pt")

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def hello(self):
        return "Hello!"

'''
    addFile(getBrowserPath(path) + 'resources/' + filename + '.py', string)
    string = '''
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      metal:use-macro="context/main_template/macros/master"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="plone">
    <metal:block fill-slot="content">
        <div tal:define="hello nocall: view/hello">
            <span tal:content="hello" />
        </div>
    </metal:block>
</html>
'''
    addFile(getBrowserPath(path) + 'resources/' + filename + '.pt', string)

def addBrowserFiles(path):
    # Register browser-dir:
    registerBrowser(path)
    # Add init to browser-dir:
    addFile(getBrowserPath(path) + '__init__.py', '')
    # Add interface:
    addFile(getLastLvlPath(path) + 'interfaces.py', 'from zope.interface import Interface\n\n\
class I' + getUppercasedName(path) + '(Interface):\n\
    """Interface for layer-specific customisation.\n\
    """\n')
    # Add browserlayer: 
    addFile(getProfilePath(path) + 'browserlayer.xml', '<?xml version="1.0"?>\n\
    <layers>\n\
        <layer name="' + getAddonName(path)  + '.layer"\n\
                   interface="' + getAddonName(path)  + '.interfaces.I' + getUppercasedName(path)  + '" />\n\
    </layers>')
    # Register resources in config:
    addBrowserConf(path)
    # Add CSS-config:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_css">\n\
</object>\n'
    addFile(getProfilePath(path) + 'cssregistry.xml', string)
    # Add JS-config:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_javascripts">\n\
</object>\n'
    addFile(getProfilePath(path) + 'jsregistry.xml', string)

def addDependency(dep_name, path):
    path = getAddonPath(path) + 'setup.py'
    pattern = "'setuptools',"
    string = "'" + dep_name + "',\n"
    insertAfterLine(path, pattern, string)
    path = getProfilePath(path) + 'metadata.xml'
    pattern = '</dependencies>'
    string = '  <dependency>profile-' + dep_name + ':default</dependency>\n'
    insertBeforeLine(path, pattern, string, KEEP_INDENT=False)

def setSetupPyProp(path, prop, val):
    """Expects path to setup.py, a prop and a val and exchanges the val in file.
    """
    lines = getLines(path)
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith(prop + '='):
            line_splits = line.split('=')
            line = line_splits[0] + "='" + val + "',\n"
            lines[i] = line
    string = ''.join(lines)
    addFile(path, string, OVERWRITE=True)

def setSetupPy(path, defaults_path=getHome() + '.buildout/devgen.cfg'):
    """Writes default-values into setup.py.
    Expects a path to the addon's setup.py and a path to a defaults-file.
    Defaults-file must be in this format:
    prop=val
    author=Jane Austin
    author_email=jane@aust.in
    Line by line, no quotes or commas needed.
    """

    if not fileExists(defaults_path): exit('No defaults provided, "' + defaults_path + '" doesn\'t exist. Aborting now.')


    default_lines = getLines(defaults_path)
    for default in default_lines:
        default = default.strip()
        if default is not '':
            pair = default.split('=')
            prop = pair[0]
            val = pair[1]
            setSetupPyProp(path, prop, val)


def addBuildoutDefaultConfig(plone_vs, path):
    string = """[buildout]
parts =
    instance
    plonesite

extends = configs/""" + plone_vs + """/versions.cfg

eggs-directory = eggs

versions = versions

#develop = src/dev.addon

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
#    dev.addon
    Pillow
    Plone
    plone.api
    plone.reload
zcml =
    plone.reload

[plonesite]
# Newest (1.9.1) breaks layout, when autoinstall devegg:
recipe = collective.recipe.plonesite == 1.9.0
#products = dev.addon

[versions]
# Overcome neverending setuptools-conflict-hell,
# thanks to thet and pbauer, see github.com/minimalplone4:
zc.buildout = >= 2.2.1
setuptools = >= 2.2
"""
    addFile(path + 'default.cfg', string)

def addSetuphandlers(path):
    string = '<genericsetup:importStep\n\
      name="' + getAddonName(path) + '"\n\
      title="' + getAddonName(path) + ' special import handlers"\n\
      description=""\n\
      handler="' + getAddonName(path) + '.setuphandlers.setupVarious" />\n\
      />\n\n'
    if not fileHasStr(getConfigPath(path), string):
        insertBeforeLine(getConfigPath(path), '</configure>', string)
    string = "from Products.CMFCore.utils import getToolByName\n\
\n\
def doOnInstall(context):\n\
    # Put your code, to be executed on an install, here.\n\
    # If you want this to happen only on the initial, very first install,\n\
    # uncomment the next lines:\n\
#    qi = getToolByName(context, 'portal_quickinstaller')\n\
#    prods = qi.listInstallableProducts(skipInstalled=False)\n\
#    for prod in prods:\n\
#        if (prod['id'] == '" + getAddonName(path) + "') and (prod['status'] == 'uninstalled'):\n\
\n\
def setupVarious(context):\n\
    portal = context.getSite()\n\
    # The text-file is a flag, the following will only be excecuted, if it's present in an imported profile:\n\
    if context.readDataFile('" + getAddonName(path) + ".marker.txt') is None:\n\
        return\n\
\n\
    doOnInstall(portal)"

    addFile(getLastLvlPath(path) + 'setuphandlers.py', string)
    addFile(getProfilePath(path) + getAddonName(path) + '.marker.txt')

