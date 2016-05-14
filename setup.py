from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='adi.devgen',
      version=version,
      description="Misc helper-scripts for creating and expanding Plone-Add-Ons.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "CHANGES.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ida Ebkes',
      author_email='contact@ida-ebkes.eu',
      url='https://github.com/ida/adi.devgen/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'adi.commons',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      devgen = adi.devgen.devgen:devgen

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

