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
from Products.CMFCore.permissions import ManagePortal

from fti import DynamicViewTypeInformation
from fti import manage_addFactoryDynamivViewTIForm

def initialize(context):
    context.registerClass(
        DynamicViewTypeInformation,
        permission=ManagePortal,
        constructors=( manage_addFactoryDynamivViewTIForm, ),
        #icon='images/typeinfo.gif',
        visibility=None)
