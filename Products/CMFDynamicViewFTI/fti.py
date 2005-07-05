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

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Globals import DTMLFile
from Acquisition import aq_base

from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.TypesTool import TypesTool
from Products.CMFCore.TypesTool import typeClasses
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import _dtmldir
from Products.CMFCore.utils import _wwwdir
from Products.CMFCore.utils import getToolByName

from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation

try:
    from DocumentTemplate.cDocumentTemplate import safe_callable
except ImportError:
    def safe_callable(ob):
        # Works with ExtensionClasses and Acquisition.
        if hasattr(ob, '__class__'):
            if hasattr(ob, '__call__'):
                return 1
            else:
                return isinstance(ob, types.ClassType)
        else:
            return callable(ob)

try:
    import Products.CMFPlone
except:
    HAS_PLONE2 = False
else:
    HAS_PLONE2 = True

class DynamicViewTypeInformation(FactoryTypeInformation):
    """FTI with dynamic views
    
    A value of (dynamic view) as alias is replaced by the output of defaultView()
    """

    __implements__ = (IDynamicViewTypeInformation,)

    meta_type = 'Factory-based Type Information with dynamic views'
    security = ClassSecurityInfo()

    _properties = FactoryTypeInformation._properties + (
        { 'id': 'default_view', 'type': 'string', 'mode': 'w',
          'label': 'Default view method'
        },
        { 'id': 'view_methods', 'type': 'lines', 'mode': 'w',
          'label': 'Available view methods'
        },
    )

    default_view = ''
    view_methods = ()

    def manage_changeProperties(self, **kw):
        """Overwrite change properties to verify that default_view is in the method
        list
        """
        FactoryTypeInformation.manage_changeProperties(self, **kw)
        default_view = self.default_view
        view_methods = self.view_methods
        if not default_view:
            # TODO: use view action 
            self.default_view = default_view = self.immediate_view
        if not view_methods:
            self.view_methods = view_methods = (default_view,)
        if default_view and default_view not in view_methods:
            raise ValueError, "%s not in %s" % (default_view, view_methods)

    security.declareProtected(View, 'getAvailableViewMethods')
    def getAvailableViewMethods(self, context):
        """Get a list of registered view methods
        """
        methods = self.view_methods
        if isinstance(methods, basestring):
            methods = (methods,)
        return tuple(methods)

    security.declareProtected(View, 'getViewMethod')
    def getViewMethod(self, context, enforce_available = True):
        """Get view method (aka layout) name from context
        
        Return -- view method from context or default view name
        """
        default = self.default_view
        layout = getattr(aq_base(context), 'layout', None)

        if layout is not None:
            if safe_callable(layout):
                layout = layout()
            if not isinstance(layout, basestring):
                raise TypeError, "layout of %s must be a string, got %s" % (
                                  repr(context), type(layout))
            if enforce_available:
                available = self.getAvailableViewMethods(context)
                if layout in available:
                    return layout
                else:
                    return default
            else:
                return layout
        else:
            return default

    security.declareProtected(View, 'getDefaultViewMethod')
    def getDefaultViewMethod(self, context):
        """Get the default view method from the FTI
        """
        return str(self.default_view)

    security.declareProtected(View, 'getDefaultPage')
    def getDefaultPage(self, context, check_exists=False):
        """Get the default page from a folderish object
        
        Non folderish objects don't have a default view.
        
        If check_exists is enabled the method makes sure the object with the default
        page id exists.
        
        Return -- None for no default page or a string
        """

        if not getattr(aq_base(context), 'isPrincipiaFolderish', False):
            return None # non folderish objects don't have a default page per se

        default_page = getattr(context, 'default_page', None)
        if default_page is None:
            return None

        if safe_callable(default_page):
            default_page = default_page()
        if not default_page:
            return None
        if isinstance(default_page, (tuple, list)):
            default_page = default_page[0]
        if not isinstance(default_page, str):
            raise TypeError, ("default_page must be a string, got %s(%s):" % 
                              (default_page, type(default_page)))

        if check_exists:
            try:
                # BTreeFolder2 optimization
                if not aq_base(context).has_key(default_page):
                    return None
            except AttributeError:
                # standard ObjectManager api
                if default_page not in context.objectIds():
                    return None

        return default_page

    security.declareProtected(View, 'defaultView')
    def defaultView(self, context):
        """Get the current view to use for an object. If a default page is  set,
        use that, else use the currently selected view method/layout.
        """

        # Delegate to PloneTool's version if we have it else, use own rules
        if HAS_PLONE2:
            obj, path = getToolByName(self, 'plone_utils').browserDefault(context)
            return path[-1]
        else:
            default_page = self.getDefaultPage(context, check_exists = True)
            if default_page is not None:
                return default_page
            return self.getViewMethod(context)

    security.declarePublic('queryMethodID')
    def queryMethodID(self, alias, default=None, context=None):
        """ Query method ID by alias.
        
        Use "(dynamic view)" as the alias target to look up as per defaultView()
        Use "(selected layout)" as the alias target to look up as per 
            getViewMethod()
        """
        methodTarget = FactoryTypeInformation.queryMethodID(self, alias,
                                                         default=default,
                                                         context=context)
        if not isinstance(methodTarget, basestring):
            # nothing to do, method_id is probably None
            return methodTarget

        if context is None or default == '':
            # the edit zpts like typesAliases don't apply a context and set the 
            # default to ''. We do not want to resolve (dynamic view) for these
            # methods.
            return methodTarget

        # Our two special targets:

        if methodTarget.lower() == "(dynamic view)":
            methodTarget = self.defaultView(context)

        if methodTarget.lower() == "(selected layout)":
            methodTarget = self.getViewMethod(context)

        return methodTarget

InitializeClass(DynamicViewTypeInformation)

def manage_addFactoryDynamivViewTIForm(self, REQUEST):
    """ Get the add form for factory-based type infos.
    """
    addTIForm = DTMLFile('addTypeInfo', _dtmldir).__of__(self)
    ttool = getToolByName(self, 'portal_types')
    return addTIForm( self, REQUEST,
                      add_meta_type=DynamicViewTypeInformation.meta_type,
                      types=ttool.listDefaultTypeInformation() )


# BBB: the following lines are required to register the new FTI in CMF 1.5 and may
# be removed after switching to CMF 1.6
setattr(TypesTool, 'manage_addFactoryDynamivViewTIForm',
                    manage_addFactoryDynamivViewTIForm)

setattr(TypesTool, 'manage_addFactoryDynamivViewTIForm__roles__',
                    ('Manager', ))

typeClasses.append(
    {'class' : DynamicViewTypeInformation,
     'name' : DynamicViewTypeInformation.meta_type,
     'action' : 'manage_addFactoryDynamivViewTIForm',
     'permission' : ManagePortal,
     },
    )
