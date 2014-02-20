#!/usr/bin/env sh
cname=genarch_A_0
py=/mnt/scratch/tg/w/pyavida

cdir=$py/config/$cname
odir=2014-02-14_$cname

python $py/pyavida/avidasimbuilder.py -f --prefix $odir --outdir /mnt/scratch/tg/w/$odir --avidacfg $cdir/avida.cfg --events $cdir/events.cfg --env $cdir/environment.cfg --analyze $cdir/analyze.cfg --org $cdir/default-heads.org --inst $cdir/instset-heads.cfg -x 10 > $cdir/$odir.workspaces

cat $cdir/$odir.workspaces | python $py/pyavida/avidarunlauncher.py --buyin ged-intel11 --run --analyze --submit

