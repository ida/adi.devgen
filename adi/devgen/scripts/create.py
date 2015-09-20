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
from adi.devgen.scripts.conventions import getBrowserPath
from adi.devgen.scripts.conventions import getConfigPath
from adi.devgen.scripts.conventions import getLastLvlPath
from adi.devgen.scripts.conventions import getProfilePath
from adi.devgen.scripts.conventions import getResourcesPath
from adi.devgen.scripts.conventions import getUnderscoredName
from adi.devgen.scripts.conventions import getUppercasedName

def addSetupPy(path):
    addon_name = path.split('/')[-2]
    addon_first_name = addon_name.split('.')[0]
    string = '\
from setuptools import setup, find_packages\n\
import os\n\
\n\
version = \'0.1.dev0\'\n\
\n\
setup(name=\'' + addon_name + '\',\n\
      version=version,\n\
      description="",\n\
      long_description=open("README.md").read() + "\n" +\n\
                             open(os.path.join("docs", "INSTALL.md")).read(),\n\
                             open(os.path.join("docs", "USAGE.md")).read(),\n\
                             ",\n\
      classifiers=[\n\
        "Framework :: Plone",\n\
        "Programming Language :: Python",\n\
        ],\n\
      keywords=\'\',\n\
      author=\'\',\n\
      author_email=\'\',\n\
      url=\'http://svn.plone.org/svn/collective/\',\n\
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
    """Add doc-folder containing 'CHANGES.md', 'INSTALL.md' and 'USAGE.md'."""
    addDirs(path + 'docs')
    addFile(path + 'docs/CHANGES.md', 'Changelog\n=========\n')
    addFile(path + 'docs/INSTALL.md', 'Installation\n===========\n')
    addFile(path + 'docs/USAGE.md', 'Usage\n=====\n')

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

def registerProfile(path):
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
    string = '\
<?xml version="1.0"?>\n\
<metadata>\n\
  <version>1000</version>\n\
  <dependencies>\n\
  </dependencies>\n\
</metadata>\n'
    if not fileExists(getProfilePath(path) + 'metadata.xml'):
        addFile(getProfilePath(path) + 'metadata.xml', string)

def addSkin(path):
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
    #addFile(getSkinPath(path) + 'public.css', 'body{background:red}') # DEV
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
    name = getAddonName(path)
    string= '<configure\n\
 xmlns="http://namespaces.zope.org/zope"\n\
 xmlns:five="http://namespaces.zope.org/five"\n\
 xmlns:browser="http://namespaces.zope.org/browser"\n\
 i18n_domain="'+name+'">\n\
\n\
    <include package="plone.app.contentmenu" />\n\
    <browser:resourceDirectory\n\
        name="'+name+'.resources"\n\
        directory="resources"\n\
      />\n\
\n\
<!--\n\
    <include package="plone.app.contentmenu" />\n\
    <browser:page\n\
        for="*"\n\
        name="adi_popadi_view_view"\n\
        template="resources/adi_popadi_view.pt"\n\
        permission="zope2.View"\n\
        layer=".interfaces.IAdiPopadi"\n\
      />\n\
\n\
    <browser:page\n\
        for="*"\n\
        name="adi_popadi_view_helpers"\n\
        class=".adi_popadi_viewhelpers.View"\n\
        permission="zope2.View"\n\
        layer=".interfaces.IAdiPopadi"\n\
      />\n\
-->\n\
\n</configure>'
    addFile(getBrowserPath(path) + 'configure.zcml', string)

def addBrowser(path):
    # Add interface:
    addFile(getLastLvlPath(path) + 'interfaces.py', 'from zope.interface import Interface\n\n\
class I' + getUppercasedName(path) + '(Interface):\n\
    """Interface for layer-specific customisation.\n\
    """\n')
    # Add browserlayer: 
    addFile(getProfilePath(path) + 'browserlayer.xml', '<?xml version="1.0"?>\n\
    <layers>\n\
        <layer name="' + getAddonName(path)  + 'browser.layer"\n\
                   interface="' + getAddonName(path)  + '.interfaces.I' + getUppercasedName(path)  + '" />\n\
    </layers>')
    # Register resources in config:
    addBrowserConf(path)
    # Register resources in profile:
    # CSS:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_css">\n\
 <stylesheet title=""\n\
    id="++resource++' + getAddonName(path) + 'resources/' + getUnderscoredName(path) + '.css"\n\
    media="screen" rel="stylesheet" rendering="import"\n\
    cacheable="True" compression="safe" cookable="True"\n\
    enabled="1" expression=""/>\n\
\n\
</object>'
    addFile(getProfilePath(path) + 'cssregistry.xml', string)
    # JS:
    string = '\
<?xml version="1.0"?>\n\
<object name="portal_javascripts">\n\
 <javascript authenticated="False" cacheable="True" compression="none"\n\
    conditionalcomment="" cookable="True" enabled="True" expression=""\n\
    id="++resource++' + getAddonName(path) + 'resources/' + getUnderscoredName(path) + '.js"\n\
    inline="False"/>\n\
</object>'
    addFile(getProfilePath(path) + 'jsregistry.xml', string)
    # Create resources:
    # CSS:
    addFile(getResourcesPath(path) + getUnderscoredName(path) + '.css', '#visual-portal-wrapper:before{content:"++resource++' + getAddonName(path) + 'resources/' + getUnderscoredName(path) + '.css loaded"}')
    # JS:
    string = '\
(function($) {\n\
        $(document).ready(function() {\n\
            $("<div>++resource++' + getAddonName(path) + 'resources/' + getUnderscoredName(path) + '.js loaded</div>").insertBefore("#visual-portal-wrapper")\n\
        }); //docready\n\
})(jQuery);'
    addFile(getResourcesPath(path) + getUnderscoredName(path) + '.js', string)

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


def addBuildoutConfig(plone_version, path):
    string = """[buildout]
parts =
    instance
    plonesite

extends = ../.shared/configs/""" + plone_version + """/versions.cfg

eggs-directory = /home/ida/.buildout/eggs

#develop = src/dev.addon

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
#    dev.addon
    Pillow
    Plone
    plone.reload
zcml =
    plone.reload

[plonesite]
# Newest (1.9.1) breaks layout, when autoinstall devegg:
recipe = collective.recipe.plonesite == 1.9.0
#products = dev.addon
"""
    addFile(path + 'buildout.cfg', string)

def addSetuphandlers(path):
    string = '<genericsetup:importStep\n\
      name="' + getAddonName(path) + '"\n\
      title="' + getAddonName(path) + ' special import handlers"\n\
      description=""\n\
      handler="' + getAddonName(path) + '.setuphandlers.setupVarious" />\n\
      />\n\n'
    if not fileHasStr(getConfigPath(path), string):
        insertBeforeLine(getConfigPath(path), '</configure>', string)
    else:
        print 'Skipped registration of setuphandlers, already exists.'
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
