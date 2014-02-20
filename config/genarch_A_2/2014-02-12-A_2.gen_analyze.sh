#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

cat $py/config/genarch_A_2/2014-02-12-A_2.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --analyze --submit
