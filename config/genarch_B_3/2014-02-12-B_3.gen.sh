#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --prefix 2014-02-12-B_3 --outdir /mnt/scratch/tg/w/2014-02-12-B_3 --avidacfg $py/config/genarch_B_3/avida.cfg --events $py/config/genarch_B_3/events.cfg --env $py/config/genarch_B_3/environment.cfg -x 10 -f > $py/config/genarch_B_3/2014-02-12-B_3.workspaces

cat $py/config/genarch_B_3/2014-02-12-B_3.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
