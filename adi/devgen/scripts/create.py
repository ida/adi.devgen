from adi.commons.commons import *
from conventions import *

def addSetup(path):
    addon_name = path.split('/')[-2]
    addon_first_name = addon_name.split('.')[0]
    string = '\
from setuptools import setup, find_packages\n\
import os\n\
\n\
version = \'1.0\'\n\
\n\
setup(name=\'' + addon_name + '\',\n\
      version=version,\n\
      description="",\n\
      long_description="",\n\
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

def addProfile(path):
    string = '\n\
  <genericsetup:registerProfile\n\
      name="default"\n\
      title="' + getAddonName(path) + '"\n\
      directory="profiles/default"\n\
      description="Installs the ' + getAddonFirstName(path) + ' package"\n\
      provides="Products.GenericSetup.interfaces.EXTENSION"\n\
      />\n'
    if not fileExists(getLastLvlPath(path) + 'configure.zcml'): addConfig(getLastLvlPath(path))
    insertBeforeLastTag(getLastLvlPath(path) + 'configure.zcml', string)

def addMetadata(path):
    string = '\
<?xml version="1.0"?>\n\
<metadata>\n\
<version>1000</version>\n\
<dependencies>\n\
</dependencies>\n\
</metadata>\n'
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
    insertBeforeLine(path, pattern, string)
    path = getProfilePath(path) + 'metadata.xml'
    pattern = '</dependencies>'
    string = '<dependency>profile-' + dep_name + ':default</dependency>'
    insertBeforeLine(path, pattern, string)

#EOF
