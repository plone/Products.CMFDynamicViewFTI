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
from Interface import Attribute
from Interface import Interface

from Products.CMFCore.interfaces.portal_types import ContentTypeInformation as \
    ITypeInformation

class IDynamicViewTypeInformation(ITypeInformation):
    """Interface for FTI with dynamic views
    
    A value of (dynamic view) as alias is replaced by the output of getLayout()
    """
    
    def getAvailableViewMethods(context):
        """Get a list of registered view methods
        """

    def getViewMethod(context, enforce_available = True):
        """Get view method name from context
        
        Return -- view method from context or default view name
        """
    
    def getDefaultViewMethod(context):
        """Get the default view method from the FTI
        """
        
    def getDefaultPage(context, check_exists=False):
        """Get the default page from a folderish object
        
        Non folderish objects don't have a default view.
        
        If check_exists is enabled the method makes sure the object with the default
        page id exists.
        
        Return -- None for no default page or a string
        """
    
    def getLayout(context):
        """Get the layout for an object
        
        At first it tries to get the default page from the context. A default page
        must be listed on the folder or else it is ignored.
        
        At last it get the view method.
        
        Return -- a string containing the name of the layout
        """

class IBrowserDefault(Interface):
    """
    Interface for content supporting different views on a per-instance basis, 
    either as a page template, or as the id of a contained object (inside a 
    folderish item only). 
    """
        
    def defaultView(request=None):
        """
        Get the actual view to use. If a default page is set, its id will
        be returned. Else, the current layout's page template id is returned.
        """
    
    # Note that Plone's browserDefault is very scary. This method should delegate
    # to PloneTool.browserDefault() if at all possible. browserDefault() is
    # aware of IBrowserDefault and will do the right thing wrt. layouts and
    # default pages. 
    
    def __browser_default__(request):
        """
        Resolve what should be displayed when viewing this object without an
        explicit template specified. Returns a tuple (obj, [path, path]), where
        obj is the object to publish (usually self), and the list of paths is
        the list of page templates/object ids to try to use as the view for 
        this object.
        """
        
    # see __call__ in PortalObject
    #def __call__():
    #    """Resolve the selected layout template, i.e. self.getLayout()() wrapped
    #    in the current acquisition context.
    #    """

    def getDefaultPage():
        """
        Return the id of the default page, or None if none is set. The default
        page must be contained within this (folderish) item.
        """

    def getLayout(**kw):
        """
        Get the selected layout template. Note that a selected default page
        will override the layout template.
        """
        
    def getDefaultLayout():
        """
        Get the default layout template.
        """
    
class ISelectableBrowserDefault(IBrowserDefault):
    """
    Interface for content supporting operations to explicitly set the default
    layoute template or default page object.
    """
    
    def canSetDefaultPage():
        """
        Return True if the user has permission to select a default page on this
        (folderish) item, and the item is folderish.
        """

    def setDefaultPage(objectId):
        """
        Set the default page to display in this (folderish) object. The objectId
        must be a value found in self.objectIds() (i.e. a contained object).
        This object will be displayed as the default_page/index_html object
        of this (folderish) object. This will override the current layout
        template returned by getLayout(). Pass None for objectId to turn off
        the default page and return to using the selected layout template.
        """

    def setLayout(layout):
        """
        Set the layout as the current view. 'layout' should be one of the list
        returned by getAvailableLayouts(). If a default page has been set
        with setDefaultPage(), it is turned off by calling setDefaultPage(None).
        """
        
    def canSetLayout():
        """
        Return True if the current authenticated user is permitted to select
        a layout.
        """
        
    def getAvailableLayouts():
        """
        Get the layouts registered for this object.
        
        This should return a list of tuples: (id, title), where id is the id
        of the page template providing the layout and title is the title of
        that page template as it will be displayed to the user.
        """
