from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AddPortalFolders
from Products.CMFDynamicViewFTI import content_for_tests
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation


def initialize(context):
    # (DynamicViewTypeInformation factory is created from ZCML)
    cmf_utils.registerIcon(
        DynamicViewTypeInformation,
        'images/typeinfo.gif',
        globals()
    )

    context.registerClass(
        content_for_tests.DynFolder,
        permission=AddPortalFolders,
        constructors=(
            ('addDynFolder', content_for_tests.addDynFolder),
        ),
        icon='images/typeinfo.gif'
    )

    context.registerClass(
        content_for_tests.DynDocument,
        permission=AddPortalContent,
        constructors=(
            ('addDynDocument', content_for_tests.addDynDocument),
        ),
        icon='images/typeinfo.gif'
    )
