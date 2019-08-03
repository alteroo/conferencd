FROM plone:5.1.5

COPY docker.cfg /plone/instance/
COPY sources.cfg /plone/instance/
COPY pins.cfg /plone/instance/
COPY --chown=plone:plone src/collective.videolink /plone/instance/src/collective.videolink
COPY --chown=plone:plone src/conf.policy /plone/instance/src/conf.policy

RUN buildDeps="dpkg-dev gcc git libbz2-dev libc6-dev libjpeg62-turbo-dev libopenjp2-7-dev libpcre3-dev libssl-dev libtiff5-dev libxml2-dev libxslt1-dev wget zlib1g-dev" \
 && runDeps="gosu libjpeg62 libopenjp2-7 libtiff5 libxml2 libxslt1.1 lynx netcat poppler-utils rsync wv" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $buildDeps \
 && cd /plone/instance 
# && gosu plone buildout -c docker.cfg \
# && apt-get purge -y --auto-remove $buildDeps \ 
RUN gosu plone buildout -c docker.cfg
RUN apt-get purge -y --auto-remove $buildDeps \
 && apt-get install -y --no-install-recommends $runDeps \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /plone/buildout-cache/downloads/*
 
COPY addons.cfg /plone/instance/
RUN gosu plone buildout -c addons.cfg

#COPY addSite.py /plone/instance/
#ENV NEW_SITE_ID Plone
#RUN gosu plone bin/instance run addSite.py 
