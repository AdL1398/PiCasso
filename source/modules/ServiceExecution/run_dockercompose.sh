#!/bin/sh
directory=$1;
cd $directory
chmod 777 $directory/docroot/rows.json
chmod 777 -R $directory/docroot/uploads
docker-compose up -d
