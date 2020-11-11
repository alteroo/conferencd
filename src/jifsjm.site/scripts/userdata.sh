#!/bin/bash
#groupadd www
#usermod -a -G www ec2-user
#!/bin/bash
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#cd $DIR


sudo apt-get update -y
sudo apt-get install python-dev python-virtualenv libjpeg-dev libssl-dev libxml2-dev git -y
sudo apt-get install  libav-tools libreadline-dev wv poppler-utils libxslt1-dev libpcre3-dev libbz2-dev python-pip python-tk python-gdbm -y
sudo apt-get install ruby graphicsmagick pdftk poppler-utils poppler-data ghostscript tesseract-ocr nginx -y
sudo gem install docsplit

git clone git@gitlab.com:alteroo-flyjamaica/flyjamaica.site.git
cd flyjamaica.site.git
./installSite.sh