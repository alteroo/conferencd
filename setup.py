# -*- coding: utf-8 -*-
"""Installer for the jifsjm.site package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='jifsjm.site',
    version='1.0a1',
    description="JIFS 2017",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1b3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='david',
    author_email='david@alteroo.com',
    url='',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['jifsjm'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       # 'collective.themesitesetup',
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
        'plone.app.mosaic',
        'plone.patternslib',
        'rapido.plone',
        'lineage.themeselection',
        'wildcard.media',
        'Products.GenericSetup>=1.8.2',
        'Products.PloneFormGen',
        'setuptools',
        'z3c.jbot',
        'conf.policy',
        'Products.QuickImporter',
        'plone.app.imagecropping',
        'plone.app.theming',
        'plone.app.themingplugins',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
