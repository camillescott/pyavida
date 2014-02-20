#!/usr/bin/env sh

for folder in genarch_*_*; do
    echo `basename $folder`.sh
    sh build_genarch.sh `basename $folder` 2014-02-20-p 10
done 
