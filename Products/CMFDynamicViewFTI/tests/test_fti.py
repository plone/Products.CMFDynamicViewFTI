# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from Products.CMFCore.interfaces import ITypeInformation
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation
from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation
from Products.CMFDynamicViewFTI.tests import CMFDVFTITestCase
from zope.interface.verify import verifyObject

import six
import transaction

fti_meta_type = DynamicViewTypeInformation.meta_type


class TestFTI(CMFDVFTITestCase.CMFDVFTITestCase):

    def _makeOne(self):
        # Create and return a DynFolder
        self.folder.invokeFactory('DynFolder', id='dynfolder')
        return self.folder.dynfolder

    def test_doesImplementITypeInformation(self):
        iface = ITypeInformation
        self.assertTrue(iface.providedBy(self.fti))
        self.assertTrue(verifyObject(iface, self.fti))

    def test_doesImplementIDynamicViewTypeInformation(self):
        iface = IDynamicViewTypeInformation
        self.assertTrue(iface.providedBy(self.fti))
        self.assertTrue(verifyObject(iface, self.fti))

    def test_meta_type(self):
        self.assertEqual(self.fti.meta_type, fti_meta_type)

    def test_paranoid_subclass_test(self):
        self.assertTrue(isinstance(self.fti, DynamicViewTypeInformation))

    def test_CreateDynFolder(self):
        dynfolder = self._makeOne()
        self.assertEqual(dynfolder.getPortalTypeName(), 'DynFolder')
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getId(), 'DynFolder')
        self.assertEqual(info.Title(), 'DynFolder')
        self.assertEqual(info.getDefaultViewMethod(dynfolder), 'index_html')
        self.assertEqual(
            info.getAvailableViewMethods(dynfolder),
            ('index_html', 'custom_view', 'zope3_view')
        )

    def test_DynFolderDefaultView(self):
        dynfolder = self._makeOne()
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getViewMethod(dynfolder), 'index_html')

    def test_DynFolderCustomView(self):
        dynfolder = self._makeOne()
        self.types.DynFolder.manage_changeProperties(
            default_view='custom_view'
        )
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
        self.assertEqual(
            info.getViewMethod(dynfolder, enforce_available=True),
            'custom_view'
        )

    def test_UnavailableLayoutReturnsDefaultView(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'bad_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(
            info.getViewMethod(dynfolder, enforce_available=True),
            'index_html'
        )

    def test_CheckLayoutExists(self):
        dynfolder = self._makeOne()
        dynfolder.manage_addDTMLMethod('custom_view', file='')
        dynfolder.layout = 'custom_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(
            info.getViewMethod(dynfolder, check_exists=True),
            'custom_view'
        )

    def test_MissingLayoutReturnsDefaultView(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'bad_view'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(
            info.getViewMethod(dynfolder, check_exists=True),
            'index_html'
        )

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

    def test_CheckDefaultPageExists(self):
        dynfolder = self._makeOne()
        dynfolder.manage_addDTMLMethod('custom_page', file='')
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(
            info.getDefaultPage(dynfolder, check_exists=True),
            'custom_page'
        )

    def test_MissingDefaultPageReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.default_page = 'bad_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(
            info.getDefaultPage(dynfolder, check_exists=True),
            None
        )

    def test_NonFolderishObjectReturnsNone(self):
        dynfolder = self._makeOne()
        dynfolder.isPrincipiaFolderish = 0
        dynfolder.default_page = 'custom_page'
        info = self.types.getTypeInfo(dynfolder)
        self.assertEqual(info.getDefaultPage(dynfolder), None)

    def test_DefaultViewWithBadLayoutUseFallback(self):
        dynfolder = self._makeOne()
        dynfolder.layout = 'bad_view'
        info = self.types.getTypeInfo(dynfolder)
        # fallback not returned if not activated
        self.assertFalse(info.default_view_fallback)
        self.assertEqual(
            info.defaultView(dynfolder),
            'bad_view'
        )
        # enable fallback
        info.default_view_fallback = True
        self.assertEqual(
            info.defaultView(dynfolder),
            info.default_view
        )

if six.PY2:
    # I have no idea what is or should be happending here.
    # In py2 this test works but in py3 it yields:
    # TypeError: 'ReplaceableWrapper' object is not callable

    class TestEmptyLayoutBug(CMFDVFTITestCase.CMFDVFTITestCase):
        # Finally, here is why we did all this...

        def setUp(self):
            super(TestEmptyLayoutBug, self).setUp()
            # Make a DynFolder
            self.folder.invokeFactory('DynFolder', id='dynfolder')
            self.dynfolder = self.folder.dynfolder
            self.dynfolder.layout = ''  # Empty layout triggers bug
            self.dynfolder_path = self.dynfolder.absolute_url(1)

            # Make a DynDocument
            self.folder.invokeFactory('DynDocument', id='dyndocument')
            self.dyndocument = self.folder.dyndocument
            self.dyndocument.layout = ''  # Empty layout triggers bug
            self.dyndocument_path = self.dyndocument.absolute_url(1)
            import transaction
            transaction.commit()
            from plone.testing.z2 import Browser
            self.browser = Browser(self.layer['app'])
            self.browser.handleErrors = False
            self.browser.addHeader(
                'Authorization', 'Basic %s:%s' %
                (TEST_USER_NAME, TEST_USER_PASSWORD,)
            )

        def test_FolderEmptyLayoutBug(self):
            self.browser.open(self.dynfolder.absolute_url() + '/view')
            self.assertEqual(self.browser._response.status_code, 200)

        def test_DocumentEmptyLayoutBug(self):
            self.browser.open(self.dyndocument.absolute_url() + '/view')
            self.assertEqual(self.browser._response.status_code, 200)


class TestModifyDefaultPage(CMFDVFTITestCase.CMFDVFTITestCase):

    def _makeOne(self):
        # Create and return a DynFolder
        self.folder.invokeFactory('DynFolder', id='dynfolder')
        dynfolder = self.folder.dynfolder
        dynfolder.invokeFactory('DynDocument', id='default_document')
        dynfolder.setDefaultPage('default_document')
        return dynfolder

    def test_rename_default_page(self):
        dynfolder = self._makeOne()
        self.assertEqual(dynfolder.getDefaultPage(), 'default_document')
        transaction.commit()
        dynfolder.manage_renameObject('default_document', 'renamed_default')
        self.assertFalse('default_document' in dynfolder.objectIds())
        self.assertTrue('renamed_default' in dynfolder.objectIds())
        self.assertEqual(dynfolder.getDefaultPage(), 'renamed_default')
        self.assertEqual(dynfolder.getProperty('default_page', ''),
                         'renamed_default')

    def test_delete_default_page(self):
        dynfolder = self._makeOne()
        self.assertEqual(dynfolder.getDefaultPage(), 'default_document')
        dynfolder.manage_delObjects(['default_document'])
        self.assertFalse('default_document' in dynfolder.objectIds())
        self.assertEqual(dynfolder.getDefaultPage(), None)
        self.assertEqual(dynfolder.getProperty('default_page', ''), '')

    def test_cut_default_page(self):
        dynfolder = self._makeOne()
        self.assertEqual(dynfolder.getDefaultPage(), 'default_document')
        transaction.commit()
        clipboard = dynfolder.manage_cutObjects(['default_document'])
        self.folder.manage_pasteObjects(clipboard)
        self.assertFalse('default_document' in dynfolder.objectIds())
        self.assertTrue('default_document' in self.folder.objectIds())
        self.assertEqual(dynfolder.getDefaultPage(), None)
        self.assertEqual(dynfolder.getProperty('default_page', ''), '')
