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

from Products.CMFDynamicViewFTI.tests import CMFDVFTITestCase

import zope.component 
import zope.component.testing
from zope.app.testing import setup
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.publisher.interfaces.browser import IBrowserView        
import zope.app.publisher.browser
import zope.publisher.browser

from Products.CMFCore.utils import getToolByName

from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from Interface.Verify import verifyObject
from Interface.Verify import verifyClass

class DummyFolder(BrowserDefaultMixin):

    def getTypeInfo(self):
        return self.fti

class IDummy(zope.interface.Interface):
    """ marker interface for a zope 3 view """

class BrowserView(zope.app.publisher.browser.BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request   

class TestBrowserDefault(CMFDVFTITestCase.CMFDVFTITestCase):

    def test_doesImplementISelectableBrowserDefault(self):
        iface = ISelectableBrowserDefault
        self.failUnless(iface.isImplementedByInstancesOf(BrowserDefaultMixin))
        self.failUnless(verifyClass(iface, BrowserDefaultMixin))

    def test_extendsInterface(self):
        self.failUnless(ISelectableBrowserDefault.extends(IBrowserDefault))

class TestAvailableLayouts(CMFDVFTITestCase.CMFDVFTITestCase):

    def afterSetUp(self):
        self.types = getToolByName(self.portal, 'portal_types')

        self.dfolder = DummyFolder()
        self.dfolder.fti = self.types['DynFolder']

        zope.component.testing.setUp(self)
        setup.setUpTraversal()
        zope.component.provideAdapter(
        BrowserView,
        (IDummy, IBrowserRequest), IBrowserView,
        name='zope3_view')              
        
    def test_Zope3View(self):
        dfolder = self.dfolder
        dfolder.layout = 'zope3_view'
        dfolder.REQUEST = zope.publisher.browser.TestRequest()
        view_methods = dfolder.getAvailableLayouts()
        view_ids = [ view_id for view_id, foo in view_methods ]
        self.failIf(dfolder.layout in view_ids)
        
        # Mark the object with interface connected to the zope 3 view
        zope.interface.directlyProvides(dfolder, IDummy)
        view_methods = dfolder.getAvailableLayouts()
        view_ids = [ view_id for view_id, foo in view_methods ]
        self.failIf(dfolder.layout not in view_ids)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBrowserDefault))
    suite.addTest(makeSuite(TestAvailableLayouts))    
    return suite
