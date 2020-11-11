# Create a Plone site. This is a "run" script.
import sys
import transaction
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from plone import api
from zope.component.hooks import setSite
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INavigationSchema
from Products.CMFPlone.interfaces.controlpanel import IImagingSchema
from Products.CMFPlone.interfaces.controlpanel import ISiteSchema
from zope.component import getUtility

site_id = sys.argv[3]
SITE_TITLE = u"Fly Jamaica Airways"
WEBSTATS_JS = u"""
<!-- Google Tag Manager -->

<noscript><iframe 
src="//www.googletagmanager.com/ns.html?id=GTM-KZP2FT"
height="0" width="0" 
style="display:none;visibility:hidden"></iframe></noscript>

<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KZP2FT');

</script>
<!-- End Google Tag Manager -->

<!--  remarketing ---------------------------------------------- -->
<script type="text/javascript">
/* <![CDATA[ */
var google_conversion_id = 989144367;
var google_custom_params = window.google_tag_params;
var google_remarketing_only = true;
/* ]]> */
</script>
<script type="text/javascript" src="//www.googleadservices.com/pagead/conversion.js">
</script>
<noscript>
<div style="display:inline;">
<img height="1" width="1" style="border-style:none;" alt="" src="//googleads.g.doubleclick.net/pagead/viewthroughconversion/989144367/?value=0&amp;guid=ON&amp;script=0"/>
</div>
</noscript>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-2704879-52']);
  _gaq.push(['_setDomainName', 'fly-jamaica.com']);
  _gaq.push(['_setAllowLinker', true]);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'stats.g.doubleclick.net/dc.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
<!-- Hotjar Tracking Code for http://www.fly-jamaica.com -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:155087,hjsv:5};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'//static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""

#language = "en-jm"
default_extension_profiles = (
    'plone.app.caching:default',
    'plonetheme.barceloneta:default',
    'Products.ATContentTypes:base',
    'flyjamaica.site:default',
#    '{{ addon }}',
)
print("----------> Initiating install of {} site".format(site_id))

if site_id in app.objectIds():
    print "The site was already installed"
    sys.exit(1)

site = addPloneSite(
    app, site_id,
    title=SITE_TITLE,
    profile_id=_DEFAULT_PROFILE,
    extension_ids=default_extension_profiles,
    setup_content=True,
#    default_language=language,
    )
    

# Sets the current site as the active site
print("----------> Setting {} as the active site".format(site_id))
setSite(app[site_id])
registry = getUtility(IRegistry)
navigation_settings = registry.forInterface(
    INavigationSchema,
    prefix='plone'
)
image_settings = registry.forInterface(
    IImagingSchema,
    prefix='plone'
)
site_settings = registry.forInterface(
    ISiteSchema,
    prefix='plone'
)

# set up navigation settings
print("----------> Setting Navigation settings")
navigation_settings.nonfolderish_tabs = False
navigation_settings.workflow_states_to_show = ('published',)
navigation_settings.filter_on_workflow = True
navigation_settings.displayed_types = ('Event', 'File', 'Folder', 
                                       'FormFolder', 'Image', 'Link', 
                                       'News Item', 'Document')
print("----------> Setting Site settings")
site_settings.enable_sitemap = True
site_settings.site_title = SITE_TITLE
site_settings.webstats_js = WEBSTATS_JS

print("----------> Setting Custom Image settings")
image_settings.allowed_sizes = [
                                u'large 768:768', u'preview 400:400', 
                                u'mini 200:200', u'thumb 128:128', 
                                u'tile 64:64', u'icon 32:32', 
                                u'listing 16:16', u'two_fifty 250:250',
                                u'custom 500:375']
# switch on the theme
print("----------> Enabling the custom diazo theme")
NAMESPACE = 'plone.app.theming.interfaces.IThemeSettings'
api.portal.set_registry_record('%s.absolutePrefix' % NAMESPACE,
                               u'/++theme++flyjamaica.theme')
api.portal.set_registry_record('%s.currentTheme' % NAMESPACE,
                               u'flyjamaica.theme')
api.portal.set_registry_record('%s.doctype' % NAMESPACE, '<!doctype html>')
api.portal.set_registry_record('%s.enabled' % NAMESPACE, True)
api.portal.set_registry_record('%s.readNetwork' % NAMESPACE, True)
api.portal.set_registry_record('%s.rules' % NAMESPACE,
                             u'/++theme++flyjamaica.theme/rules.xml')

"""
print("----------> Setting VirtualHost Mapping")
HOST='localhost'
print "-----> Plone site %s exists" % site_id
print "-----> Setting virtualhost settings"
vhosts = ['%s/%s' % (HOST,site_id), HOST + "/VirtualHostBase/https/%s/%s" % (HOST,site_id)]
rules = "\n".join(vhosts)
app.virtual_hosting.set_map(rules)
"""

transaction.commit()
