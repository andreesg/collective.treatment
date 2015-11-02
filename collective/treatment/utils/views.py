#!/usr/bin/python
# -*- coding: utf-8 -*-

from collective.leadmedia.adapters import ICanContainMedia
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from collective.treatment import MessageFactory as _
from plone.dexterity.browser.view import DefaultView

from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from plone.app.widgets.dx import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser import add, edit
from collective.z3cform.datagridfield.interfaces import IDataGridField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class TreatmentView(edit.DefaultEditForm):
    """ View class """

    template = ViewPageTemplateFile('../treatment_templates/view.pt')

    def update(self):
        super(TreatmentView, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = False
                widget.allow_reorder = True
            alsoProvides(widget, IFormWidget)

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False