# -*- coding: utf-8 -*-
from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class DynFolder(PortalFolder, BrowserDefaultMixin):
    pass


class DynDocument(PortalContent, BrowserDefaultMixin):

    def __init__(self, id, title):
        self.id = id
        self.title = title


def addDynFolder(self, id, title='', REQUEST=None):
    """Add a new DynFolder object with id *id*.
    """
    ob = DynFolder(id, title)
    self._setObject(id, ob, suppress_events=True)


def addDynDocument(self, id, title='', REQUEST=None):
    """Add a new DynDocument object with id *id*.
    """
    ob = DynDocument(id, title)
    self._setObject(id, ob, suppress_events=True)
