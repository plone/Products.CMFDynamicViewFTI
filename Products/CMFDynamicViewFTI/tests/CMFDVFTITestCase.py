from plone.app import testing
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.base.utils import unrestricted_construct_instance
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

import transaction
import unittest


class CMFDynamicViewFTIFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        profile_registry.registerProfile(
            "CMFDVFTI_sampletypes",
            "CMFDynamicViewFTI Sample Content Types",
            "Extension profile including CMFDVFTI sample content types",
            "profiles/sample_types",
            "CMFDynamicViewFTI",
            EXTENSION,
            for_=ISiteRoot,
        )
        import Products.CMFDynamicViewFTI.tests

        self.loadZCML(
            name="browserdefault.zcml", package=Products.CMFDynamicViewFTI.tests
        )

        from plone.testing.zope import _INSTALLED_PRODUCTS

        if "Products.CMFDynamicViewFTI" not in _INSTALLED_PRODUCTS.keys():
            # replicate plone.testing.zope.installProduct
            # when running the tests via tox Products.CMFDynamicViewFTI
            # folder location is different than the other Products.*
            # packages.
            # `installProduct` checks for that and bails out otherwise.
            from AccessControl.class_init import InitializeClass
            from OFS.Application import get_folder_permissions
            from OFS.Application import install_product
            from OFS.Folder import Folder
            from pathlib import Path

            import inspect

            module_path = Path(inspect.getfile(Products.CMFDynamicViewFTI))
            product_folder = str(module_path.parent.parent)

            install_product(
                app,
                product_folder,
                "CMFDynamicViewFTI",
                [],
                get_folder_permissions(),
                raise_exc=1,
            )
            InitializeClass(Folder)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "CMFDynamicViewFTI:CMFDVFTI_sampletypes")


CDV_FIXTURE = CMFDynamicViewFTIFixture()
CDV_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CDV_FIXTURE,), name="CMFDynamicViewFTI Testing:Functional"
)


class CMFDVFTITestCase(unittest.TestCase):
    """This is a stub now, but in case you want to try
    something fancy on Your Branch (tm), put it here.
    """

    layer = CDV_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up before each test."""
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        unrestricted_construct_instance("DynFolder", self.portal, id="folder")
        self.folder = self.portal.folder
        self.types = getToolByName(self.portal, "portal_types")
        self.fti = self.types["DynFolder"]
        transaction.commit()
