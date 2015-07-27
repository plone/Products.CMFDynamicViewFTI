# -*- coding: utf-8 -*-
#
# CMFDVFTITestCase
#
from plone.app import testing
from plone.app.testing import bbb
from Products.CMFCore.interfaces import ISiteRoot
from Products.GenericSetup import EXTENSION, profile_registry


class PloneTestCaseFixture(bbb.PloneTestCaseFixture):

    defaultBases = (bbb.PTC_FIXTURE, )

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

CDV_FIXTURE = PloneTestCaseFixture()
CDV_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CDV_FIXTURE, ), name='CMFDynamicViewFTI Testing:Functional')


class CMFDVFTITestCase(bbb.PloneTestCase):
    """This is a stub now, but in case you want to try
       something fancy on Your Branch (tm), put it here.
    """

    layer = CDV_FUNCTIONAL_TESTING
