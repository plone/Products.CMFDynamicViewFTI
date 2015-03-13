from setuptools import setup, find_packages

version = '4.0.6'

setup(name='Products.CMFDynamicViewFTI',
      version=version,
      description="CMFDynamicViewFTI is a product for dynamic views in CMF.",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
      ],
      keywords='Zope CMF Plone dynamic view',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.CMFDynamicViewFTI',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'plone.app.contentmenu',
            'zope.publisher',
            'plone.app.testing',
            'Products.Archetypes',
        ]
      ),
      install_requires=[
        'setuptools',
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
