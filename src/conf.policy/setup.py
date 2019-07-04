from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='conf.policy',
      version=version,
      description="Policy product for Plone Conference 2106 website",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['conf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.PloneFormGen',
          'Products.RedirectionTool',
          # 'collective.embedly', # Not Plone 5 compatible
          'collective.addthis',
          'plone.app.mosaic',
          'Products.QuickImporter',
          'plone.api',
          'collective.fbshare',
          'collective.relatedslider',
          'plone.api',
          'collective.ambidexterity',
          'collective.captcha',
          'collective.documentviewer',
          'collective.easyform',
          'collective.lineage',
          'collective.ptg.flickr',
          'collective.routes',
          'collective.videolink',
          'collective.z3cform.norobots',
          'gloss.theme',
          'plone.patternslib',
          'rapido.plone',
          'lineage.themeselection',
          'wildcard.media',
          'Products.GenericSetup>=1.8.2',
          'setuptools',
          'z3c.jbot',
          'Products.QuickImporter',
          'plone.app.imagecropping',
          'plone.app.theming',
          'plone.app.themingplugins',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
