echo "configuring a plone user for docker"
sudo addgroup --gid 500 plone
sudo adduser --system --gid 500 plone
sudo usermod -G plone,docker $USER
echo "We've added you to two new groups (plone and docker)"
echo "Please logout and log back in or launch a new terminal to continue"
