#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory
from collective.z3cform.datagridfield.interfaces import IDataGridField

#
# plone.app.widgets dependencies
#
from plone.app.z3cform.widget import DatetimeFieldWidget

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit
from plone.app.z3cform.widget import AjaxSelectFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder

# # # # # # # # # # # # # # # # # #
# !treatment specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.treatment import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from Acquisition import aq_inner
from zc.relation.interfaces import ICatalog

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# # Treatment schema  # #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

from plone.app.content.interfaces import INameFromTitle
class INameFromTreatmentNumber(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromTreatmentNumber(object):
    implements(INameFromTreatmentNumber)
    
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

class ITreatment(form.Schema):

    priref = schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    dexteritytextindexer.searchable('priref')

    # # # # # # # # # # #
    # Treatment details #
    # # # # # # # # # # #
    model.fieldset('treatment_details', label=_(u'Treatment details'), 
        fields=['title',
                'treatmentDetails_identification_treatmentType', 'treatmentDetails_identification_reversible',
                'treatmentDetails_identification_treatmentMethod', 'treatmentDetails_identification_conservator',
                'treatmentDetails_identification_material', 'treatmentDetails_progress_startDate',
                'treatmentDetails_progress_status', 'treatmentDetails_progress_recallDate',
                'treatmentDetails_progress_endDate', 'treatmentDetails_treatment_conditionDescription',
                'treatmentDetails_treatment_treatmentPlan', 'treatmentDetails_treatment_treatmentSummary',
                'treatmentDetails_digitalReferences',
                'treatmentDetails_notes']
    )

    # Identification
    title = schema.TextLine(
        title=_(u'Treatment number'),
        required=True
    )
    dexteritytextindexer.searchable('title')

    treatmentDetails_identification_treatmentType = schema.Choice(
        vocabulary=treatmenttype_vocabulary,
        title=_(u'Treatment type'),
        required=True,
        default="No value",
        missing_value=" "
    )
    dexteritytextindexer.searchable('treatmentDetails_identification_treatmentType')

    treatmentDetails_identification_reversible = schema.Bool(
        title=_(u'Reversible'),
        required=False
    )
    
    treatmentDetails_identification_treatmentMethod = schema.List(
        title=_(u'Treatment method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('treatmentDetails_identification_treatmentMethod', AjaxSelectFieldWidget, vocabulary="collective.treatment.treatmentmethod")

    treatmentDetails_identification_conservator = ListField(title=_(u'Conservator'),
        value_type=DictRow(title=_(u'Conservator'), schema=IConversator),
        required=False)
    form.widget(treatmentDetails_identification_conservator=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_identification_conservator')

    treatmentDetails_identification_material = schema.List(
        title=_(u'Material'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('treatmentDetails_identification_material', AjaxSelectFieldWidget, vocabulary="collective.treatment.material")

    # Progress
    treatmentDetails_progress_startDate = schema.TextLine(
        title=_(u'Start date'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_progress_startDate')
    #form.widget(treatmentDetails_progress_startDate=DatetimeFieldWidget)

    treatmentDetails_progress_status = schema.TextLine(
        title=_(u'Status'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_progress_status')

    treatmentDetails_progress_recallDate = schema.TextLine(
        title=_(u'Recall date'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_progress_recallDate')
    #form.widget(treatmentDetails_progress_recallDate=DatetimeFieldWidget)

    treatmentDetails_progress_endDate = schema.TextLine(
        title=_(u'End date'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_progress_endDate')
    #form.widget(treatmentDetails_progress_endDate=DatetimeFieldWidget)

    # Treatment
    treatmentDetails_treatment_conditionDescription = ListField(title=_(u'Condition description'),
        value_type=DictRow(title=_(u'Condition description'), schema=IConditionDescription),
        required=False)
    form.widget(treatmentDetails_treatment_conditionDescription=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_treatment_conditionDescription')

    treatmentDetails_treatment_treatmentPlan = ListField(title=_(u'Treatment plan'),
        value_type=DictRow(title=_(u'Treatment plan'), schema=ITreatmentPlan),
        required=False)
    form.widget(treatmentDetails_treatment_treatmentPlan=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_treatment_treatmentPlan')

    treatmentDetails_treatment_treatmentSummary = ListField(title=_(u'Treatment summary'),
        value_type=DictRow(title=_(u'Treatment summary'), schema=ITreatmentSummary),
        required=False)
    form.widget(treatmentDetails_treatment_treatmentSummary=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_treatment_treatmentSummary')

    # (Digital) references
    treatmentDetails_digitalReferences = ListField(title=_(u'(Digital) references'),
        value_type=DictRow(title=_(u'(Digital) references'), schema=IDigitalReferences),
        required=False)
    form.widget(treatmentDetails_digitalReferences=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_digitalReferences')

    # Notes
    treatmentDetails_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(treatmentDetails_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_notes')


    # # # # # # # # # # #
    # Reproduction      #
    # # # # # # # # # # #
    model.fieldset('reproductions', label=_(u'Reproductions'), 
        fields=['reproductions_reproduction']
    )

    # Reproduction
    reproductions_reproduction = ListField(title=_(u'Reproduction'),
        value_type=DictRow(title=_(u'Reproduction'), schema=IReproduction),
        required=False)
    form.widget(reproductions_reproduction=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductions_reproduction')

    # # # # # # # # # # #
    # Linked objects    #
    # # # # # # # # # # #
    model.fieldset('linked_objects', label=_(u'Linked Objects'), 
        fields=['linkedObjects_linkedObjects']
    )

    """linkedObjects_temp = schema.TextLine(
        title=_(u'Object number'),
        required=False,
        default=u"",
        missing_value=u""
    )"""

    linkedObjects_linkedObjects = ListField(title=_(u'Linked Objects'),
        value_type=DictRow(title=_(u'Linked Objects'), schema=ILinkedObjects),
        required=False)
    form.widget(linkedObjects_linkedObjects=DataGridFieldFactory)
    dexteritytextindexer.searchable('linkedObjects_linkedObjects')


# # # # # # # # # # # # # #
# Treatment declaration   #
# # # # # # # # # # # # # #

class Treatment(Container):
    grok.implements(ITreatment)
    pass

# # # # # # # # # # # # # # # # 
# Treatment add/edit views    # 
# # # # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('treatment_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

    def getRelatedObjects(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        source_object = self.context

        relations = catalog.findRelations(
            dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute="conditionConservation_conservationTreatments")
        )

        structure = ""
        for rel in list(relations):
            from_object = rel.from_object
            title = getattr(from_object, 'title', '')
            obj_number = getattr(from_object, 'identification_identification_objectNumber', '')
            url = from_object.absolute_url()
            structure += "<p><a href='%s'><span>%s</span> - <span>%s</span></a></p>" %(url, obj_number, title)

        return structure

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('treatment_templates/edit.pt')
    
    def getRelatedObjects(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        source_object = self.context

        relations = catalog.findRelations(
            dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute="conditionConservation_conservationTreatments")
        )

        structure = ""
        for rel in list(relations):
            from_object = rel.from_object
            title = getattr(from_object, 'title', '')
            obj_number = getattr(from_object, 'identification_identification_objectNumber', '')
            url = from_object.absolute_url()
            structure += "<p><a href='%s'><span>%s</span> - <span>%s</span></a></p>" %(url, obj_number, title)

        return structure

    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

