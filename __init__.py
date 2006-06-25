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

from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import registerIcon

from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation
from Products.CMFDynamicViewFTI.fti import manage_addFactoryDynamivViewTIForm

try:
    from Products.CMFTestCase.interfaces import ICMFTestSiteRoot
    from Products.GenericSetup import EXTENSION, profile_registry
    HAS_GENERICSETUP = True
except ImportError:
    HAS_GENERICSETUP = False


def initialize(context):
    # BBB remove registerIcon after we have switched to CMF 1.6
    registerIcon(DynamicViewTypeInformation,
                 'images/typeinfo.gif', globals())
    context.registerClass(
        DynamicViewTypeInformation,
        permission=ManagePortal,
        constructors=( manage_addFactoryDynamivViewTIForm, ),
        icon='images/typeinfo.gif',
        visibility=None)

    if HAS_GENERICSETUP:
        profile_registry.registerProfile('CMFDVFTI_sampletypes',
                'CMFDynamicViewFTI Sample Content Types',
                'Extension profile including CMFDVFTI sample content types',
                'profiles/sample_types',
                'CMFDynamicViewFTI',
                EXTENSION,
                for_=ICMFTestSiteRoot)
