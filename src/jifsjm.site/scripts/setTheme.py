import os
import sys
import transaction
from plone import api
from zope.component.hooks import setSite

""" 
This is a very simple approach which uses positional arguments passed to a script
the first argument is the id of your plone site.
the second argument is the name of your theme

usage:

    bin/instance run scripts/setTheme.py test texasbusinesslaw-june-01-2018rev
"""
site_id = sys.argv[3]
new_theme = sys.argv[4]
if site_id in app.objectIds():
    print "The {} Plone site was found".format(site_id)
else:
    print "No Plone site was found with id {}".format(site_id)
    sys.exit(1)

# Sets the current site as the active site
setSite(app[site_id])

def set_theme():
    portal = api.portal.get()
    registry = api.portal.get_tool(name='portal_registry')
    registry['plone.app.theming.interfaces.IThemeSettings.currentTheme'] = u'{}'.format(new_theme)
    transaction.commit()

#################################
# This is where we do stuff
##################################
print("----------> -- Setting the Theme")
set_theme()
print("----------> -- Theme set to {}".format(new_theme))