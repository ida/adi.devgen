from adi.commons.commons import addFile
from conventions import getAddonName
from conventions import getAddonFirstName
from conventions import getLastLvl

def addSetup(addon_path):
    addon_name = getAddonName(addon_path)
    addon_first_name = getAddonFirstName(addon_path)
    string = '\
from setuptools import setup, find_packages\n\
import os\n\
\n\
version = \'1.0\'\n\
\n\
setup(name=\''+addon_name+'\',\n\
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
      namespace_packages=[\''+addon_first_name+'\'],\n\
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
      setup_requires=["PasteScript"],\n\
      paster_plugins=["ZopeSkel"],\n\
      )\n\
'
    addFile(addon_path + 'setup.py', string)

def addFirstInit(path):
    string = '\
# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages\n\
try:\n\
    __import__(\'pkg_resources\').declare_namespace(__name__)\n\
except ImportError:\n\
    from pkgutil import extend_path\n\
    __path__ = extend_path(__path__, __name__)\n\
'
    addFile(path + '__init__.py', string)

def addLastInit(path):
    string = '\
def initialize(context):\n\
    """Initializer called when used as a Zope 2 product."""\n\
'
    addFile(path + '__init__.py', string)

def addConfig(addon_path):
    addon_name = getAddonName(addon_path)
    last_lvl = getLastLvl(addon_path)
    string = '\
<configure\n\
    xmlns="http://namespaces.zope.org/zope"\n\
    xmlns:five="http://namespaces.zope.org/five"\n\
    xmlns:i18n="http://namespaces.zope.org/i18n"\n\
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"\n\
    i18n_domain="'+addon_name+'">\n\
\n\
  <five:registerPackage package="." initialize=".initialize" />\n\
\n\
  <genericsetup:registerProfile\n\
      name="default"\n\
      title="'+addon_name+'"\n\
      directory="profiles/default"\n\
      description="Installs the '+addon_name+' package"\n\
      provides="Products.GenericSetup.interfaces.EXTENSION"\n\
      />\n\
</configure>\n\
'
    addFile(last_lvl + 'configure.zcml', string)

def addMetadata(path):
    string = '\
<?xml version="1.0"?>\n\
<metadata>\n\
  <version>1000</version>\n\
</metadata>\n\
'
    addFile(path + 'metadata.xml', string)

#EOF
