FROM alteroo/conferencd:version-0.0.2
 
COPY debug.cfg /plone/instance/
RUN gosu plone buildout -c debug.cfg
