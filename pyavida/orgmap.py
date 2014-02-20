import numpy as np
import pandas as pd
import sys

def parse_taskmap(fn, usecols=[4]):
    '''
    Parses the map file and produces an array of the values of
    each instruction. Value is defined as the number of task
    completions that instruction enables; ie, the task count
    minus the number of times the task is completed when 
    that instruction is knocked out.

    Values are clipped at 0 and taskcount, meaning that if
    knocking out an instruction actually enables additional
    task completions, we don't consider it. An interesting
    analysis might look at how often such improvements
    are realized within the lineage, but that is another project ;)
    '''

    M_o = np.loadtxt(fn, skiprows=1, usecols=usecols)
    org_id = -1
    with open(fn, 'rb') as fp:
        ln = fp.readline()
        ln = ln.split()
        org_id = int(ln[2])
        u_born = int(ln[3])
        task_count = float(ln[-1])
    #print task_count
    M_o = task_count - M_o
    M_o = np.clip(M_o, 0.0, task_count)
    #print M_o
    return org_id, M_o

def get_org_mat(fn, skiprows=11, 
                cols=['u_birth','org_id','merit','eff','fitness','t_gest']):
    '''
    Wrapper to get a DataFrame of organism data, with the given
    column names and rows to skip
    '''
    print >>sys.stderr, 'loading {fn}...'.format(fn=fn)
    orgs_df = pd.read_csv(fn, header=None, names=cols, delimiter=' ',
                            skiprows=skiprows, dtype=np.float64,
                            usecols=range(0,6))
    return orgs_df
