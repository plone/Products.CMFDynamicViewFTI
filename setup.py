from setuptools import setup, find_packages

version = '4.0.1'

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
