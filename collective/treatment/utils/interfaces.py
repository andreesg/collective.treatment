#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.treatment import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.app.widgets.dx import AjaxSelectFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form
priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

## Treatment details

class ITreatmentMethod(Interface):
    term = schema.TextLine(title=_(u'Treatment method'), required=False)

class IConversator(Interface):
    name = RelationList(
        title=_(u'Conservator'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('name', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

class IMaterial(Interface):
    term = schema.TextLine(title=_(u'Material'), required=False)

class IConditionDescription(Interface):
    description = schema.TextLine(title=_(u'Condition description'), required=False)

class ITreatmentPlan(Interface):
    plan = schema.TextLine(title=_(u'Treatment plan'), required=False)

class ITreatmentSummary(Interface):
    summary = schema.TextLine(title=_(u'Treatment summary'), required=False)

class IDigitalReferences(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class INotes(Interface):
    notes = schema.Text(title=_(u'Notes'), required=False)

## Linked Objects
class ILinkedObjects(Interface):
    form.widget('objectNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    objectNumber = RelationList(
        title=_(u'Object number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object')
        ),
        required=False
    )
    #creator = schema.TextLine(title=_(u'Creator'), required=False)
    #objectName = schema.TextLine(title=_(u'Object name'), required=False)
    #title = schema.TextLine(title=_(u'Title'), required=False)


## Reproductions
class IReproduction(Interface):
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    format = schema.TextLine(title=_(u'Format'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    identifierURL = schema.TextLine(title=_(u'Identifier (URL)'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

