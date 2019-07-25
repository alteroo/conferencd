from plone.supermodel import model
from Products.Five import BrowserView


class IFormExternal(model.Schema):
    model.load('models/form_external.xml')


class FormExternalView(BrowserView):
    pass
