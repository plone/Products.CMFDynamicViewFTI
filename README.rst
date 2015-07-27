Overview
========

CMFDynamicViewFTI is a product for dynamic views in CMF.
The product contains an additional base class for types and a new factory type information (FTI).

The FTI contains two new properties for the default view method and supplementary view methods.
The queryMethodID functionality used for alias lookups is enhanced to support a new keyword (dynamic view).

The BrowserDefaultMixin class adds some methods to classes.
It is not required to make use of the basic features
but it is recommend to subclass your types from the class to gain more functionality.

There are two event subscribers registered:

``zope.container.interfaces.IContainerModifiedEvent``
    unset default page if target no longer exists

``zope.lifecycleevent.interfaces.IObjectMovedEvent``
    rename default page if target was renamed


Source Code
===========

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/Products.CMFDynamicViewFTI>`_.
