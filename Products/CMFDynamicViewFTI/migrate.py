from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation
fti_meta_type = DynamicViewTypeInformation.meta_type

def migrateFTI(portal, id, ti_name, fti_meta_type):
    """Migrates a single FTI to DynamicViewFTI

    portal - context (portal root)
    id - id of the type information
    ti_name - name of the type information
    fti_meta_type - name of the fti type
    """
    ttool = getToolByName(portal, 'portal_types')
    ti = ttool[id]

    # copy all data like actions and properties
    actions = []
    for action in getattr(ti, '_actions', ()):
        actions.append(action._getCopy(action))
    actions = tuple(actions)
    properties = dict(ti.propertyItems())

    # delete the old fti and create a new one
    ttool._delObject(id)

    ttool.manage_addTypeInformation(fti_meta_type,
                                    id=id,
                                    typeinfo_name=ti_name)

    # assign actions and properties from the old fti
    # NOTE: aliases are ignored and security settings are not copied
    new_ti = ttool[id]
    new_ti._actions = actions
    new_ti.manage_changeProperties(**properties)


def migrateFTIs(portal, product=None, fti_meta_type=fti_meta_type):
    """Migrates all FTIs in portal types

    migrateFTIs checks all FTIs if they have to be migrated. The product argument
    can be used to restrict migration to a single product
    """
    ttool = getToolByName(portal, 'portal_types')
    migrated = []

    # create a list of type informations that might need migration
    # (product, meta_type) -> type info name
    ftis = {}
    for name, ti in ttool.listDefaultTypeInformation():
        ti_product = ti.get('product', None)
        ti_mt = ti.get('meta_type', None)
        if product and ti_product != product:
            continue
        if ti.get('fti_meta_type') != fti_meta_type:
            continue
        ftis[(ti_product, ti_mt)] = name

    # check all FTIs in portal_types
    for obj in ttool.objectValues():
        if obj.meta_type == fti_meta_type:
            continue # already migrated

        ti_product = getattr(aq_base(obj), 'product', None)
        ti_mt = getattr(aq_base(obj), 'content_meta_type', None)
        if not ti_product or not ti_mt:
            continue # strange/broken ti object or no FTI

        ti_name = ftis.get((ti_product, ti_mt), None)
        if ti_name is None:
            continue # not in list of FTIs to be migrated

        # match - migrated FTI
        id = obj.getId()
        migrateFTI(portal, id, ti_name, fti_meta_type)
        migrated.append(id)

    return migrated
