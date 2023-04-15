from setuptools import find_packages
from setuptools import setup


version = "7.0.1"

long_description = open("README.rst").read()
long_description += "\n"
long_description += open("CHANGES.rst").read()


setup(
    name="Products.CMFDynamicViewFTI",
    version=version,
    description="CMFDynamicViewFTI is a product for dynamic views in CMF.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="Zope CMF Plone dynamic view",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/Products.CMFDynamicViewFTI",
    license="ZPL",
    packages=find_packages(),
    namespace_packages=["Products"],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            "Products.GenericSetup",
            "plone.base",
            "plone.app.testing >= 4.2.5",
            "plone.testing",
            "zope.publisher",
        ]
    ),
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "zope.browser",
        "zope.browsermenu",
        "Products.CMFCore",
        "ExtensionClass",
        "Zope",
    ],
)
