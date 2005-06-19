##############################################################################
#
# Copyright (c) 2005 Christian Heimes and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
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

from interfaces import IDynamicViewTypeInformation

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

    
class DynamicViewTypeInformation(FactoryTypeInformation):
    """FTI with dynamic views
    """
    __implements__ = (IDynamicViewTypeInformation,)
    
    meta_type = 'Factory-based Type Information with dynamic views'
    security = ClassSecurityInfo()
    
    _properties = FactoryTypeInformation._properties + (
        { 'id': 'default_view', 'type': 'string', 'mode': 'w',
          'label': 'Default view methods'
        },
        { 'id': 'view_templates', 'type': 'lines', 'mode': 'w',
          'label': 'Available view methods'
        },
    )
    
    default_view = ''
    view_templates = ()
    
    def manage_changeProperties(self, **kw):
        """Overwrite change properties to verify that default_view is in the template
        list
        """
        FactoryTypeInformation.manage_changeProperties(self, **kw)
        default_view = self.default_view
        view_templates = self.view_templates
        if not default_view:
            # TODO: use view action 
            self.default_view = default_view = self.immediate_view
        if not view_templates:
            self.view_templates = view_templates = (default_view,)
        if default_view and default_view not in view_templates:
            raise ValueError, "%s not in %s" % (default_view, view_templates)
            
    security.declareProtected(View, 'getAvailableViewTemplates')
    def getAvailableViewTemplates(self, context):
        """Get a list of registered view templates
        """
        return tuple(self.view_templates)
        
    security.declareProtected(View, 'getViewTemplate')
    def getViewTemplate(self, context):
        """Get view template name from context
        
        Return -- view template from context or default view name
        """
        available = self.getAvailableViewTemplates(context)
        default = self.default_view
        has_layout = getattr(aq_base(context), 'layout', None) is not None
        
        if has_layout:
            layout = getattr(context, 'layout')
            if safe_callable(layout):
                layout = layout()
            if not isinstance(layout, basestring):
                raise ValueError, "layout of %s is %s but must be a string" % (
                                  repr(context), type(layout))
            if layout in available:
                return layout
            else:
                return default
        else:
            return default
    
    security.declareProtected(View, 'getDefaultPage')
    def getDefaultPage(self, context):
        """Get the default page from a folderish object
        
        Non folderish objects don't have a default view
        
        Return -- None for no default page or a string
        """
        if not getattr(aq_base(context), 'isPrincipiaFolderish', False):
            return None # non folderish objects don't have a default page per se
        
        has_default = getattr(aq_base(context), 'default_page', None) is not None
        if not has_default:
            return None
        
        default = getattr(context, 'default_page')
        if safe_callable(default):
            default = default()
        if isinstance(default, (tuple, list)):
               default = default[0]
        if not default:
            return None
        
        return default

    security.declareProtected(View, 'getLayout')
    def getLayout(self, context):
        """Get the layout for an object
        
        Return -- a string containing the name of the layout
        """
        default_page = self.getDefaultPage(context)
        if default_page is not None:
            return default_page
        return self.getViewTemplate(context)

    security.declarePublic('queryMethodID')
    def queryMethodID(self, alias, default=None, context=None):
        """ Query method ID by alias.
        
        Use (dynamic view) as alias method name to enable dynamic views 
        """
        method_id = FactoryTypeInformation.queryMethodID(self, alias,
                                                         default=default,
                                                         context=context)
        if not isinstance(method_id, basestring):
            # nothing to do, method_id is probably None
            return method_id
        
        if context is None or default == '':
            # the edit zpts like typesAliases don't apply a context and set the 
            # default to ''. We do not want to resolve (dynamic view) for these
            # templates.
            return method_id
        
        if method_id.lower() == "(dynamic view)":
            method_id = self.getLayout(context)
        
        return method_id

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
