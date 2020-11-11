HOST=plone@terre.alteroo.com

ssh $HOST bash -c "'
cd jifsjm.site
bash scripts/runbuild
bash scripts/rundeploy
'"
