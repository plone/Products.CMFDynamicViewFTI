from Products.CMFCore.permissions import ManagePortal

from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation
from Products.CMFDynamicViewFTI.fti import manage_addFactoryDynamivViewTIForm

def initialize(context):
    context.registerClass(
        DynamicViewTypeInformation,
        permission=ManagePortal,
        constructors=( manage_addFactoryDynamivViewTIForm, ),
        icon='images/typeinfo.gif',
        visibility=None)
