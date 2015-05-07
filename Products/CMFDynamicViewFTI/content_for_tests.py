from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AddPortalFolders
from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.PortalContent import PortalContent
from App.class_init import InitializeClass

from browserdefault import BrowserDefaultMixin


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
