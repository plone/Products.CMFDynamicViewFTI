from plone.app import testing
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.GenericSetup import EXTENSION, profile_registry
import transaction
import unittest


class CMFDynamicViewFTIFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        profile_registry.registerProfile(
            'CMFDVFTI_sampletypes',
            'CMFDynamicViewFTI Sample Content Types',
            'Extension profile including CMFDVFTI sample content types',
            'profiles/sample_types',
            'CMFDynamicViewFTI',
            EXTENSION,
            for_=ISiteRoot
        )
        import Products.CMFDynamicViewFTI.tests
        self.loadZCML(name='browserdefault.zcml',
                      package=Products.CMFDynamicViewFTI.tests)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'CMFDynamicViewFTI:CMFDVFTI_sampletypes')


    def tearDownZope(self, app):
        pass

CDV_FIXTURE = CMFDynamicViewFTIFixture()
CDV_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CDV_FIXTURE, ), name='CMFDynamicViewFTI Testing:Functional')


class CMFDVFTITestCase(unittest.TestCase):
    """This is a stub now, but in case you want to try
       something fancy on Your Branch (tm), put it here.
    """
    layer = CDV_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up before each test."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        _createObjectByType('DynFolder', self.portal, id='folder')
        self.folder = self.portal.folder
        self.types = getToolByName(self.portal, 'portal_types')
        self.fti = self.types['DynFolder']
        transaction.commit()
