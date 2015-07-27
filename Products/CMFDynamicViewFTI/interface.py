# -*- coding: utf-8 -*-
# BBB module will be removed at some point. We will still need it as long as
# we plan to support Plone 4.3.x
from Products.CMFDynamicViewFTI.interfaces import *
import warnings

warnings.warn(
    'import from Products.CMFDynamicViewFTI.interfaces instead',
    DeprecationWarning
)
