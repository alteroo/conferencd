# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from Products.CMFPlone.interfaces import constrains

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'jifsjm.site:uninstall',
        ]

def custom_setup(context):
    if True: return # COMMENT THIS LINE OUT SO THAT CUSTOMIZATIONS ACTUALLY RUN

    api.content.delete(api.content.get('/news'))
    api.content.delete(api.content.get('/Members'))
    api.content.delete(api.content.get('/front-page'))
    api.content.delete(api.content.get('/events'))

    portal = api.portal.get()
 
    #check for the existence of meetings and documents
    #
    if not api.content.get('/meetings'):
       meetings = api.content.create(
        portal,
        'Folder',
        id='meetings',
        title='Meetings'
        )
    api.content.transition(meetings, transition='publish')
    behavior = constrains.ISelectableConstrainTypes(meetings)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes([ 'Folder'])
    behavior.setImmediatelyAddableTypes([ 'Folder'])
 
    if not api.content.get('/documents'):
      documents = api.content.create(
       portal,
       'Folder',
       id='documents',
       title='Documents'
      )
    api.content.transition(documents, transition='publish')

def install_settings(context):
    """ install settings for the site """
    NAMESPACE = 'plone.app.theming.interfaces.IThemeSettings'
    api.portal.set_registry_record('%s.doctype' % NAMESPACE, '<!doctype html>')
    api.portal.set_registry_record('%s.readNetwork' % NAMESPACE, True)
    api.portal.set_registry_record(
        'plone.site_title', u"JIFS"
        )
    api.portal.set_registry_record('plone.nonfolderish_tabs', False)
    api.portal.set_registry_record('plone.smtp_host',u'smtp.mailgun.org')
    api.portal.set_registry_record(
        'plone.smtp_pass',u'changethis'
        )
    api.portal.set_registry_record('plone.smtp_port',587)
    api.portal.set_registry_record(
        'plone.smtp_userid',u'postmaster@mg.jifsjm.org'
        )
    api.portal.set_registry_record('plone.mark_special_links',False)
    # api.portal.set_registry_record('plone.toolbar_logo',u'/++resource++fitzritson.theme/ritsoniteflame.png')
    api.portal.set_registry_record(
                'plone.email_from_name', u'JIFS Website'
            )
    api.portal.set_registry_record(
            'plone.email_from_address', 'noreply@jifsjm.org'
        )

def setup_various(context):
    """Import script for customizations"""
    # run customizations
    if True: return

    if context.readDataFile('jifsjm.site.marker.txt') is None:
        return

def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    install_settings(context)
    custom_setup(context)
    
def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
