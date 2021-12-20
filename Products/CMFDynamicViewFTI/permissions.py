from AccessControl.Permission import addPermission

ModifyViewTemplate = "Modify view template"
addPermission(ModifyViewTemplate, ('Manager', 'Owner'))
