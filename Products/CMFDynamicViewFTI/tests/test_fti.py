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

from Products.CMFTestCase import CMFTestCase

CMFTestCase.installProduct('CMFDynamicViewFTI')
if CMFTestCase.hasProduct('Five'):
    CMFTestCase.installProduct('Five')
CMFTestCase.setupCMFSite()

from Testing.ZopeTestCase import transaction

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces.portal_types import ContentTypeInformation as \
    ITypeInformation

from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from Interface.Verify import verifyObject

fti_meta_type = DynamicViewTypeInformation.meta_type

from data import factory_type_information


class TestFTI(CMFTestCase.CMFTestCase):

    def afterSetUp(self):
        # "Register" the DynFolder FTI definition
        self.app._getProducts().CMFCore.factory_type_information = factory_type_information
        # Create DynFolder FTI object in types tool
        self.types = types = getToolByName(self.portal, 'portal_types')
        types.manage_addTypeInformation(fti_meta_type, id='DynFolder',
                                        typeinfo_name='CMFCore: DynFolder (DynFolder)')
        self.fti = types['DynFolder']

    def _makeOne(self):
        # Create and return a DynFolder
        self.folder.invokeFactory('DynFolder', id='dynfolder')
        return self.folder.dynfolder

    def test_doesImplementITypeInformation(self):
        iface = ITypeInformation
        self.failUnless(iface.isImplementedBy(self.fti))
        self.failUnless(verifyObject(iface, self.fti))

    def test_doesImplementIDynamicViewTypeInformation(self):
        iface = IDynamicViewTypeInformation
        self.failUnless(iface.isImplementedBy(self.fti))
        self.failUnless(verifyObject(iface, self.fti))

    def test_meta_type(self):
        self.failUnlessEqual(self.fti.meta_type, fti_meta_type)

    def test_paranoid_subclass_test(self):
        self.failUnless(isinstance(self.fti, DynamicViewTypeInformation))

    def test_CreateDynFolder(self):
        dynfolder = self._makeOne()
        self.assertEqual(dynfolder.getPortalTypeName(), 'DynFolder')
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getId(), 'DynFolder')
        self.assertEqual(info.Title(), 'DynFolder')
        self.assertEqual(info.getDefaultViewMethod(dynfolder), 'index_html')
        self.assertEqual(info.getAvailableViewMethods(dynfolder), ('index_html', 'custom_view', 'zope3_view'))

    def test_DynFolderDefaultView(self):
        dynfolder = self._makeOne()
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'index_html')

    def test_DynFolderCustomView(self):
        dynfolder = self._makeOne()
        self.types.DynFolder.manage_changeProperties(default_view='custom_view')
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'custom_view')

    def test_DynFolderViewFromLayout(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'custom_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'custom_view')

    def test_DynFolderViewFromCallableLayout(self):
        dynfolder = self._makeOne()
        dynfolder.layout = lambda: 'custom_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'custom_view')

    def test_NoneLayoutReturnsDefaultView(self):
        dynfolder = self._makeOne()
        dynfolder.layout = None
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'index_html')

    def test_EmptyLayoutReturnsDefaultView(self):
        dynfolder = self._makeOne()
        dynfolder.layout = ''
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'index_html')

    def test_InvalidLayoutRaisesTypeError(self):
        dynfolder = self._makeOne()
        dynfolder.layout = object()
        info = self.types.getTypeInfo(dynfolder)
        self.assertRaises(TypeError, info.getViewMethod, dynfolder)

    def test_EnforceLayoutAvailable(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'custom_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder, True), 'custom_view')

    def test_UnavailableLayoutReturnsDefaultView(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'unavailable_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder, True), 'index_html')

    def test_DynFolderDefaultPage(self):
        dynfolder = self._makeOne()
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), None)

    def test_DynFolderDefaultPageFromAttribute(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), 'custom_page')

    def test_DynFolderDefaultPageFromCallable(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = lambda: 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), 'custom_page')

    def test_NoneDefaultPageReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = None
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), None)

    def test_EmptyDefaultPageReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = ''
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), None)

    def test_InvalidDefaultPageRaisesTypeError(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = object()
        info = self.types.getTypeInfo(dynfolder)
        self.assertRaises(TypeError, info.getDefaultPage, dynfolder)

    def test_EnforceDefaultPageAvailable(self):
        dynfolder = self._makeOne()
        dynfolder.manage_addDTMLMethod('custom_page', file='')
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder, True), 'custom_page')

    def test_UnavailableDefaultPageReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder, True), None)

    def test_NonFolderishObjectReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.isPrincipiaFolderish = 0
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), None)


class TestEmptyLayoutBug(CMFTestCase.FunctionalTestCase):
    # Finally, here is why we did all this...

    def afterSetUp(self):
        # "Register" the DynFolder FTI definitions
        self.app._getProducts().CMFCore.factory_type_information = factory_type_information
        self.app._getProducts().CMFDefault.factory_type_information = factory_type_information

        # Create FTI objects in types tool
        self.types = types = getToolByName(self.portal, 'portal_types')
        types.manage_addTypeInformation(fti_meta_type, id='DynFolder',
                                        typeinfo_name='CMFCore: DynFolder (DynFolder)')
        types.manage_addTypeInformation(fti_meta_type, id='DynDocument',
                                        typeinfo_name='CMFDefault: DynDocument (DynDocument)')

        # Make a DynFolder
        self.folder.invokeFactory('DynFolder', id='dynfolder')
        self.dynfolder = self.folder.dynfolder
        self.dynfolder.layout = '' # Empty layout triggers bug
        transaction.commit() # Make sure publish sees this change
        self.dynfolder_path = self.dynfolder.absolute_url(1)

        # Make a DynDocument
        self.folder.invokeFactory('DynDocument', id='dyndocument')
        self.dyndocument = self.folder.dyndocument
        self.dyndocument.layout = '' # Empty layout triggers bug
        transaction.commit() # Make sure publish sees this change
        self.dyndocument_path = self.dyndocument.absolute_url(1)

        self.basic = '%s:%s' % (CMFTestCase.default_user, CMFTestCase.default_password)

    def test_FolderEmptyLayoutBug(self):
        response = self.publish(self.dynfolder_path+'/view', basic=self.basic)
        self.assertEqual(response.getStatus(), 200)

    def test_DocumentEmptyLayoutBug(self):
        response = self.publish(self.dyndocument_path+'/view', basic=self.basic)
        self.assertEqual(response.getStatus(), 200)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFTI))
    suite.addTest(makeSuite(TestEmptyLayoutBug))
    return suite

if __name__ == '__main__':
    framework()
