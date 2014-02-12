import os

SRCDIR = os.path.abspath('../config/base')

DEF_REPLICATES=10

CONFIG_FILES = {'exe': 'avida', 
                'analyze': 'analyze.cfg', 
                'avidacfg': 'avida.cfg', 
                'org': 'default-heads.org', 
                'env': 'environment.cfg', 
                'events': 'events.cfg', 
                'instset': 'instset-heads.cfg'}
CONFIG_FILES = {key:os.path.join(SRCDIR,value) for key, value in CONFIG_FILES.items()}

RESOURCES='walltime=12:00:00,nodes=1:ppn=1,mem=4gb'
BUYIN=''
JOB_PREFIX='run_'
