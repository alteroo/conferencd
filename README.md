# Conferenc'd
A conference and management engine

## Overview
Conferenc'd is a conference and event management engine.
It is a distribution of Plone, primarily distributed using Docker.

WARNING: This is in early development. It has been used to host 7 conference events for customers, however we still consider it to be in a "works for us" state.

## Usage

### Running in production
We will be adding docker-compose.yml file shortly for production deployments

### In development:
1. Build the container
```
   docker build .
```
2. Get the data

If you're starting from scratch, just create your own.
```
mkdir -p data/filestorage
mkdir -p data/blobstorage
```
2a. Set permission on the data directory
```
setfacl  -R -m u:500:rwX data/
```
3. Launch the container
The resulting container can be launched on port 8080 with the data as follows:
```
 docker run -it -v $(pwd)/data/filestorage:/data/filestorage \ 
   -v $(pwd)/data/blobstorage:/data/blobstorage -p 8080:8080 alteroo/conferencd
```
