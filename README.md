# Conferenced
A conference and management engine

## Overview
Conferencd is a conference and event management engine.
It is a distribution of Plone, primarily distrubted using docker.

WARNING: This is absolutely alpha and is in a "works for us" state.

## Usage

### Running in production
We will be adding docker-compose.yml file shortly for production deployments

### In development:
1. Build the container
```
   docker build .
```
2. Get the data
```
pip install zc.buildout --user
buildout init
bin/buildout -c rsync.cfg
```
2a. Set permission on the data
```
setfacl  -R -m u:500:rwX var/
```
3. Launch the container
The resulting container can be launched on port 8080 with the data as follows:
```
 docker run -it -v $(pwd)/var/filestorage/Data.fs:/data/filestorage/Data.fs \ 
   -v $(pwd)/var/blobstorage:/data/blobstorage -p 8080:8080 alteroo/conferencd
```

### Sending the registry
