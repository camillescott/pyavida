#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

cat $py/config/genarch_A_1/2014-02-12-A_1.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --analyze --submit
