#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --analyze $py/config/genarch_B_1/analyze.cfg --prefix 2014-02-12-B_1 --outdir /mnt/scratch/tg/w/2014-02-12-B_1 --avidacfg $py/config/genarch_B_1/avida.cfg --events $py/config/genarch_B_1/events.cfg --env $py/config/genarch_B_1/environment.cfg -x 10 -f > $py/config/genarch_B_1/2014-02-12-B_1.workspaces

cat $py/config/genarch_B_1/2014-02-12-B_1.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
