Overview
========

CMFDynamicViewFTI is a product for dynamic views in CMF. The product contains
an additional base class for types and a new factory type information (FTI).

The FTI contains two new properties for the default view method and
supplementary view methods. The queryMethodID functionality used for
alias lookups is enhanced to support a new keyword (dynamic view).

The BrowserDefaultMixin class adds some methods to classes. It is not required
to make use of the basic features but it is recommend to subclass your types
from the class to gain more functionality.
