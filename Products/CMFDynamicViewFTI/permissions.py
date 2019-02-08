# -*- coding: utf-8 -*-
from AccessControl.Permission import addPermission

ModifyViewTemplate = "Modify view template"
addPermission(ModifyViewTemplate, ('Manager', 'Owner'))
