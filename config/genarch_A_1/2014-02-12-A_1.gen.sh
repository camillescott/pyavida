#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --prefix 2014-02-12-A_1 --analyze $py/config/genarch_A_0/analyze.cfg --outdir /mnt/scratch/tg/w/2014-02-12-A_1 --avidacfg $py/config/genarch_A_1/avida.cfg --events $py/config/genarch_A_1/events.cfg --env $py/config/genarch_A_1/environment.cfg -x 10 -f > $py/config/genarch_A_1/2014-02-12-A_1.workspaces

cat $py/config/genarch_A_1/2014-02-12-A_1.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
