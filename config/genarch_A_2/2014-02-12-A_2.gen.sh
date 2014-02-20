#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --analyze $py/config/genarch_A_2/analyze.cfg --prefix 2014-02-12-A_2 --outdir /mnt/scratch/tg/w/2014-02-12-A_2 --avidacfg $py/config/genarch_A_2/avida.cfg --events $py/config/genarch_A_2/events.cfg --env $py/config/genarch_A_2/environment.cfg -x 10 -f > $py/config/genarch_A_2/2014-02-12-A_2.workspaces

cat $py/config/genarch_A_2/2014-02-12-A_2.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
