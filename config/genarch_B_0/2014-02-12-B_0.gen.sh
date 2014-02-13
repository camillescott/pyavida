#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --prefix 2014-02-12-B_0 --outdir /mnt/scratch/tg/w/2014-02-12-B_0 --avidacfg $py/config/genarch_B_0/avida.cfg --events $py/config/genarch_B_0/events.cfg --env $py/config/genarch_B_0/environment.cfg -x 10 -f > $py/config/genarch_B_0/2014-02-12-B_0.workspaces

cat $py/config/genarch_B_0/2014-02-12-B_0.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
