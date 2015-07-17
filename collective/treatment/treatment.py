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
from plone.app.widgets.dx import DatetimeFieldWidget

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # # #
# !treatment specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.treatment import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# # Treatment schema  # #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

class ITreatment(form.Schema):

    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # #
    # Treatment details #
    # # # # # # # # # # #
    model.fieldset('treatment_details', label=_(u'Treatment'), 
        fields=['treatmentDetails_identification_treatmentNumber',
                'treatmentDetails_identification_treatmentType', 'treatmentDetails_identification_reversible',
                'treatmentDetails_identification_treatmentMethod', 'treatmentDetails_identification_conservator',
                'treatmentDetails_identification_material', 'treatmentDetails_progress_startDate',
                'treatmentDetails_progress_status', 'treatmentDetails_progress_recallDate',
                'treatmentDetails_progress_endDate', 'treatmentDetails_treatment_conditionDescription',
                'treatmentDetails_treatment_treatmentPlan', 'treatmentDetails_treatment_treatmentSummary',
                'treatmentDetails_digitalReferences', 'reproductions_reproduction', 'linkedObjects_linkedObjects',
                'treatmentDetails_notes']
    )

    # Identification
    treatmentDetails_identification_treatmentNumber = schema.TextLine(
        title=_(u'Treatment number'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_identification_treatmentNumber')

    treatmentDetails_identification_treatmentType = schema.Choice(
        vocabulary=treatmenttype_vocabulary,
        title=_(u'Treatment type'),
        required=False
    )
    dexteritytextindexer.searchable('treatmentDetails_identification_treatmentType')

    treatmentDetails_identification_reversible = schema.Bool(
        title=_(u'Reversible'),
        required=False
    )
    
    treatmentDetails_identification_treatmentMethod = ListField(title=_(u'Treatment method'),
        value_type=DictRow(title=_(u'Treatment method'), schema=ITreatmentMethod),
        required=False)
    form.widget(treatmentDetails_identification_treatmentMethod=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_identification_treatmentMethod')

    treatmentDetails_identification_conservator = ListField(title=_(u'Conservator'),
        value_type=DictRow(title=_(u'Conservator'), schema=IConversator),
        required=False)
    form.widget(treatmentDetails_identification_conservator=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_identification_conservator')

    treatmentDetails_identification_material = ListField(title=_(u'Material'),
        value_type=DictRow(title=_(u'Material'), schema=IMaterial),
        required=False)
    form.widget(treatmentDetails_identification_material=DataGridFieldFactory)
    dexteritytextindexer.searchable('treatmentDetails_identification_material')

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

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('treatment_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

