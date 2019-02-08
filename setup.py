# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '6.0.1'

long_description = open("README.rst").read()
long_description += "\n"
long_description += open("CHANGES.rst").read()


setup(
    name='Products.CMFDynamicViewFTI',
    version=version,
    description="CMFDynamicViewFTI is a product for dynamic views in CMF.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords='Zope CMF Plone dynamic view',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/Products.CMFDynamicViewFTI',
    license='ZPL',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.contentmenu',
            'zope.publisher',
            'plone.app.testing >= 4.2.5',
        ]
    ),
    install_requires=[
        'setuptools',
        'six',
        'zope.browsermenu',
        'zope.component',
        'zope.interface',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Acquisition',
        'ExtensionClass',
        'Zope2',
    ],
)
