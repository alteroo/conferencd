time bin/instance run scripts/addSite.py Plone 
cp scripts/*.yaml content/
time bin/instance run scripts/importContent.py Plone 
bin/instance adduser admin admin 
cp scripts/*.zexp parts/instance/import/
bin/instance fg
