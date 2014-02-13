#!/usr/bin/env sh
python pyavida/avidasimbuilder.py --prefix 2014-02-12-A --outdir /mnt/scratch/tg/w/2014-02-12-A --avidacfg config/genarch_A/avida.cfg --events config/genarch_A/events.cfg --env config/genarch_A/environment.cfg -x 10 -f > config/genarch_A/2014-02-12-A.workspaces

cat config/genarch_A/2014-02-12-A.workspaces | python pyavida/avidarunlauncher.py --buyin ged-intel11 --no-analyze --submit
