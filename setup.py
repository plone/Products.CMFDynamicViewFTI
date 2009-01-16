from setuptools import setup, find_packages
import sys, os

version = '4.0'

setup(name='Products.CMFDynamicViewFTI',
      version=version,
      description="CMFDynamicViewFTI is a product for dynamic views in CMF.",
      long_description=open("README.txt").read() +  "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone dynamic view',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/collective/CMFDynamicViewFTI/trunk',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/cmfdynamicviewfti/releases',
      extras_require=dict(
        test=[
            'plone.app.contentmenu',
            'zope.publisher',
            'Products.CMFTestCase',
        ]
      ),
      install_requires=[
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.app.publisher',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Acquisition',
        'ExtensionClass',
        'Zope2',
      ],
)
