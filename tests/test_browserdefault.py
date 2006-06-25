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

import zope.component 
import zope.component.testing
from zope.app.testing import setup
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.publisher.interfaces.browser import IBrowserView        
import zope.app.publisher.browser
import zope.publisher.browser

from Products.CMFTestCase import CMFTestCase

CMFTestCase.installProduct('CMFDynamicViewFTI')
CMFTestCase.setupCMFSite()

from Products.CMFCore.utils import getToolByName

from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from Interface.Verify import verifyObject
from Interface.Verify import verifyClass

fti_meta_type = DynamicViewTypeInformation.meta_type
from data import factory_type_information

class DummyFolder(BrowserDefaultMixin):
    
    def getTypeInfo(self):
        return self.fti
    
class IDummy(zope.interface.Interface):
    """ marker interface for a zope 3 view """

    
class BrowserView(zope.app.publisher.browser.BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request   

class TestBrowserDefault(CMFTestCase.CMFTestCase):
          

    def test_doesImplementISelectableBrowserDefault(self):
        iface = ISelectableBrowserDefault
        self.failUnless(iface.isImplementedByInstancesOf(BrowserDefaultMixin))
        self.failUnless(verifyClass(iface, BrowserDefaultMixin))

    def test_extendsInterface(self):
        self.failUnless(ISelectableBrowserDefault.extends(IBrowserDefault))

    
class TestAvailableLayouts(CMFTestCase.CMFTestCase):
    
        
    def afterSetUp(self):
        self.app._getProducts().CMFCore.factory_type_information = factory_type_information
        # Create DynFolder FTI object in types tool
        self.types = types = getToolByName(self.portal, 'portal_types')
        types.manage_addTypeInformation(fti_meta_type, id='DynFolder',
                                        typeinfo_name='CMFCore: DynFolder (DynFolder)')

        self.dfolder = DummyFolder()
        self.dfolder.fti = types['DynFolder']
            
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

if __name__ == '__main__':
    framework()
