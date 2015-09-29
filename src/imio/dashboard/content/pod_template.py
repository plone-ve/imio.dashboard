# -*- coding: utf-8 -*-

from collective.documentgenerator.content.condition import ConfigurablePODTemplateCondition
from collective.documentgenerator.content.pod_template import ConfigurablePODTemplate
from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate

from imio.dashboard import ImioDashboardMessageFactory as _
from imio.dashboard.utils import getCurrentCollection

from plone.autoform import directives as form

from z3c.form.browser.select import SelectWidget

from zope import schema
from zope.interface import implements


import logging
logger = logging.getLogger('imio.dashboard: DashboardPODTemplate')


class IDashboardPODTemplate(IConfigurablePODTemplate):
    """
    DashboardPODTemplate dexterity schema.
    """

    form.widget('dashboard_collections', SelectWidget, multiple='multiple', size=15)
    dashboard_collections = schema.List(
        title=_(u'Allowed dashboard collections'),
        description=_(u'Select for which dashboard collections the template will be available.'),
        value_type=schema.Choice(source='imio.dashboard.collectionsvocabulary'),
        required=True,
    )


class DashboardPODTemplate(ConfigurablePODTemplate):
    """
    DashboardPODTemplate dexterity class.
    """

    implements(IDashboardPODTemplate)


class DashboardPODTemplateCondition(ConfigurablePODTemplateCondition):
    """
    """

    def evaluate(self):
        """
        Check:
        - Previous conditions.
        - That we are on an allowed dashboard collection (if any defined).
        """
        current_collection = getCurrentCollection(self.context)
        allowed_collections = self.pod_template.dashboard_collections
        if not current_collection or \
           (allowed_collections and not current_collection.UID() in allowed_collections):
            return False

        return super(DashboardPODTemplateCondition, self).evaluate()
