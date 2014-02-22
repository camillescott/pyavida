#!/usr/bin/env sh
# sh build.sh <name> <date>

cname=$1
py=/mnt/scratch/tg/w/pyavida

cfg=$py/config/genarch

cdir=$py/config/$cname
odir=$2_$cname

python $py/pyavida/avidasimbuilder.py -f --prefix $odir --outdir /mnt/scratch/tg/w/$odir --avidacfg $cdir/avida.cfg --events $cfg/events.cfg --env $cfg/environment.cfg --analyze $cfg/analyze.cfg --org $cfg/default-heads.org --inst $cfg/instset-heads.cfg -x $3 > $cdir/$odir.workspaces

cat $cdir/$odir.workspaces | python $py/pyavida/avidarunlauncher.py --resources nodes=1:ppn=1,mem=4gb,walltime=48:00:00 --buyin ged-intel11 --run --analyze --submit

