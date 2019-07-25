FROM alteroo/conferencd:version-5.2.0c0
 
COPY debug.cfg /plone/instance/
RUN gosu plone buildout -c debug.cfg
