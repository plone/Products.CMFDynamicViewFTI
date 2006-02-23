##############################################################################
#
# CMFDynamicViewFTI
# Copyright (c) 2005 Plone Foundation. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
# Authors:  Martin Aspeli
#           Christian Heimes
#
##############################################################################
"""
"""

__author__ = 'Christian Heimes <tiran@cheimes.de>'
__docformat__ = 'restructuredtext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase # side effect import. leave it here.
from Products.PloneTestCase import PloneTestCase
PloneTestCase.setupPloneSite()

from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces.portal_types import ContentTypeInformation as \
    ITypeInformation

from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from Interface.Verify import verifyObject

fti_meta_type = DynamicViewTypeInformation.meta_type
typeinfo_name = "ATContentTypes: ATDocument (ATDocument)"
tests = []

class TestFTI(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)

        id = "fti_test"
        self.ttool = ttool = getToolByName(self.portal, 'portal_types')
        assert id not in ttool.objectIds()
        ttool.manage_addTypeInformation(fti_meta_type,
                                             id=id,
                                             typeinfo_name=typeinfo_name)
        self.fti = ttool[id]

    def test_doesImplementITypeInformation(self):
        iface = ITypeInformation
        self.failUnless(iface.isImplementedBy(self.fti))
        self.failUnless(verifyObject(iface, self.fti))

    def test_doesImplementIDynamicViewTypeInformation(self):
        iface = IDynamicViewTypeInformation
        self.failUnless(iface.isImplementedBy(self.fti))
        self.failUnless(verifyObject(iface, self.fti))

    def test_meta_type(self):
        self.failUnlessEqual(self.fti.meta_type,
                             'Factory-based Type Information with dynamic views')
    def test_paranoid_subclass_test(self):
        self.failUnless(isinstance(self.fti, DynamicViewTypeInformation))

tests.append(TestFTI)

if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
