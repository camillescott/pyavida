#!/usr/bin/env sh
py=/mnt/scratch/tg/w/pyavida

python $py/pyavida/avidasimbuilder.py --prefix 2014-02-12-A_0 --outdir /mnt/scratch/tg/w/2014-02-12-A_0 --avidacfg $py/config/genarch_A_0/avida.cfg --events $py/config/genarch_A_0/events.cfg --env $py/config/genarch_A_0/environment.cfg --analyze $py/config/genarch_A_0/analyze.cfg -x 10 > $py/config/genarch_A_0/2014-02-12-A_0.workspaces
