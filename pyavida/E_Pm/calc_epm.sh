#!/usr/bin/env sh

qsub -t `python -c "print ','.join([str(x) for x in range(14,200,4)])"` calc_epm.pbs
