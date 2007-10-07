from setuptools import setup, find_packages
import sys, os

version = '3.0.2'

setup(name='Products.CMFDynamicViewFTI',
      version=version,
      description="CMFDynamicViewFTI is a product for dynamic views in CMF.",
      long_description="""\
      """,
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
      install_requires=[
        'setuptools',
      ],
)
