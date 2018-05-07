# -*- coding: utf-8 -*-
from plone.app import testing
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.bbb import PloneTestCase
from Products.CMFCore.interfaces import ISiteRoot
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


class CMFDVFTITestCase(PloneTestCase):
    """This is a stub now, but in case you want to try
       something fancy on Your Branch (tm), put it here.
    """

    def setUp(self):
        """Set up before each test."""
        self.beforeSetUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        _createObjectByType('DynFolder', self.portal, id='folder')
        self.folder = self.portal.folder
        transaction.commit()
        self.afterSetUp()

    layer = CDV_FUNCTIONAL_TESTING
