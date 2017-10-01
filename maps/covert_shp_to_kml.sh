#!/bin/sh

if [ $# -lt 1 ] ; then
    echo "$0: placename"
    exit 1 
fi

# python extract.py "$1"
ogr2ogr -where "key NOT IN ('1')" -select name,from,to  -f KML ${1}.kml data/${1}.shp/edges/edges.shp 
#  cp -i ${1}_edges.kml  ~/dev/runningsong/data/worthing_edges.kml
