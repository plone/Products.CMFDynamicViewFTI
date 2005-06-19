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

from Products.CMFCore.interfaces.portal_types import ContentTypeInformation as \
    ITypeInformation

class IDynamicViewTypeInformation(ITypeInformation):
    """FTI with dynamic views
    """
    
    def getAvailableViewTemplates(context):
        """Get a list of registered view templates
        """

    def getViewTemplate(context):
        """Get view template name from context
        
        Return -- view template from context or default view name
        """
        
    def getDefaultPage(context):
        """Get the default page from a folderish object
        
        Non folderish objects don't have a default view
        
        Return -- None for no default page or a string
        """
    
    def getLayout(context):
        """Get the layout for an object
        
        Return -- a string containing the name of the layout
        """
