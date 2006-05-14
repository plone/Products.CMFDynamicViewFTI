from Products.CMFCore.permissions import View

# Test portal types
factory_type_information = (
  { 'id'             : 'DynFolder'
  , 'title'          : 'DynFolder'
  , 'meta_type'      : 'DynFolder'
  , 'icon'           : 'folder_icon.gif'
  , 'product'        : 'CMFCore'
  , 'factory'        : 'manage_addPortalFolder'
  , 'global_allow'   : True
  , 'filter_content_types' : False
  , 'immediate_view' : 'folder_edit_form'
  , 'default_view'   : 'index_html'
  , 'view_methods'   : ('index_html', 'custom_view','zope3_view')
  , 'aliases'        : {'(Default)': '(Dynamic view)',
                        'view': '(Selected layout)',
                       }
  , 'actions'        : ( { 'id'            : 'view'
                         , 'name'          : 'View'
                         , 'action': 'string:${object_url}'
                         , 'permissions'   : (View,)
                         }
                       ,
                       )
  }
, { 'id'             : 'DynDocument'
  , 'title'          : 'DynDocument'
  , 'meta_type'      : 'DynDocument'
  , 'icon'           : 'document_icon.gif'
  , 'product'        : 'CMFDefault'
  , 'factory'        : 'addDocument'
  , 'global_allow'   : True
  , 'filter_content_types' : True
  , 'immediate_view' : 'metadata_edit_form'
  , 'default_view'   : 'document_view'
  , 'view_methods'   : ('document_view', 'custom_view')
  , 'aliases'        : {'(Default)': '(Dynamic view)',
                        'view': '(Selected layout)',
                       }
  , 'actions'        : ( { 'id'            : 'view'
                         , 'name'          : 'View'
                         , 'action': 'string:${object_url}/view'
                         , 'permissions'   : (View,)
                         }
                       ,
                       )
 }
,
)