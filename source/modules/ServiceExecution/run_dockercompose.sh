#!/bin/sh
directory=$1;
cd $directory
docker-compose up -d
