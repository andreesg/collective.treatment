#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.treatment import MessageFactory as _

# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createTreatmentTypeVocabulary():
    treatment_types = {
        "conservation": _(u"conservation"),
        "restauration": _(u"restauration"),
    }

    for key, name in treatment_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createInsuranceTypeVocabulary():
    insurance_types = {
        "commercial": _(u"Commercial"),
        "indemnity": _(u"Indemnity"),
    }

    for key, name in insurance_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createPriorityVocabulary():
    priorities = {
        "low": _(u"low"),
        "medium": _(u"medium"),
        "high": _(u"high"),
        "urgent": _(u"urgent")
    }

    for key, name in priorities.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
treatmenttype_vocabulary = SimpleVocabulary(list(_createTreatmentTypeVocabulary()))
