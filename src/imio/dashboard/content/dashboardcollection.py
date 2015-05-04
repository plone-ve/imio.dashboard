# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import registerType
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from plone.app.collection.collection import Collection
from plone.app.collection.config import ATCT_TOOLNAME
from imio.dashboard.config import PROJECTNAME
from imio.dashboard.interfaces import ICustomViewFieldsVocabulary


class DashboardCollection(Collection):
    """A Collection used in our dashboards"""

    meta_type = "DashboardCollection"
    security = ClassSecurityInfo()

    security.declareProtected(View, 'listMetaDataFields')

    def listMetaDataFields(self, exclude=True):
        """
          Return a list of metadata fields from portal_catalog.
          Wrap the vocabulary in an adapter so it can be easily overrided by another package
          this is made so a package can add it's own custom columns, not only metadata.
        """
        return ICustomViewFieldsVocabulary(self).listMetaDataFields(exclude=exclude)

    security.declareProtected(View, 'selectedViewFields')

    def selectedViewFields(self):
        """
          Get which metadata field are selected.
          Override as it is used by the tabular_view and there, we do not display
          the additional fields or it breaks the view."""
        tool = getToolByName(self, ATCT_TOOLNAME)
        metadatas = [metadata.index for metadata in tool.getEnabledMetadata()]
        _mapping = {}
        for field in self.listMetaDataFields().items():
            if not field[0] in metadatas:
                continue
            _mapping[field[0]] = field
        return [_mapping[field] for field in self.customViewFields if field in metadatas]


registerType(DashboardCollection, PROJECTNAME)