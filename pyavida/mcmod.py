#import scipy as sp
import numpy as np
import os
import sys
import orgmap

def check_region(G, x, y, t=1):
    for i in xrange(x,y):
        if G[i] < t:
            return False
    return True


def P_m(G, N=1000, t=1, S=2):
    results = np.zeros(N)
    coding = np.where(G >= t)[0]
    if len(coding) >= S:
        for i in xrange(N):
            N_s = 0.0
            samples = np.sort(np.random.choice(coding, size=S, replace=False))
            for j in xrange(1,S):
                if check_region(G, samples[j-1], samples[j]):
                    N_s += 1.0
            results[i] = N_s / (S-1)
    
    results += np.random.normal(loc=0.0, scale=.00001, size=N)
    results = np.clip(results, 0.0, 1.0)
    
    return np.array([np.mean(results), np.var(results)])


def random_genome(L, N_c):
    '''
    Generate a random (binary) array of length L with N_c coding instructions
    '''
    
    coding = np.random.choice(L, size=N_c, replace=False)
    G = np.zeros(L)
    np.put(G, coding, 1)
    return G


def random_modular_genome(L, N_c, M=.25):
    '''
    Generate a random genome with P_m > .25
    WARNING: This function is terrible and takes a long time to run,
        because modular genomes are exceedingly rare
    '''
    
    M_c=0
    i=0
    while(M_c < M):
        G = random_genome(L, N_c)
        i += 1
        M_c = P_m(G, N=100)[0]
    return G, i


def random_pop(N=1000, L=100, N_c=25):
    '''
    Generate a random population of size N.
    L can be either an int for equal length genomes, or a numpy array of lengths
    N_c has the same restrictions as L    
    '''
    
    pop = []
    if type(L) == int and type(N_c) == int:
        for i in xrange(N):
            pop.append(random_genome(L, N_c))
    elif type(L) in [np.ndarray, list] and type(N_c) in [np.ndarray, list]:
        if len(L) == len(N_c) and len(L) == N:
            for i in xrange(N):
                pop.append(random_genome(L[i], N_c[i]))
        else:
            raise IndexError('L and N_c must be lists of length N')
    else:
        raise TypeError('L and N_c must be ints or lists of length N')
    return pop


def calc_random(L, N_c, N=1000):
    '''
    Convenience function for returning P_m of a randomly generated genome
    with the given parameters.
    '''
    
    G = random_genome(L=L, N_c=N_c)
    return P_m(G, N=N)



def E(L, N_c, N=1000, Ns=1000):
    '''
    Get the expected P_m for a genome L, N_c. 
    Use N genomes, with Ns passed to the P_m function
    '''
   
    #print >>sys.stderr, 'calculating E(P_m) for L={l} Nc={nc}'.format(l=L, nc=N_c) 
    results = np.zeros((N,2))
    for i in xrange(N):
        Rs = calc_random(L=L, N_c=N_c, N=Ns)
        results[i,:] = Rs[:2]
    return results

def calc_E_over_Nc_range(L, Lm, N_c_i, N_c_j, N=1000, Ns=1000):
    results = np.zeros( (Lm,) )
    print >>sys.stderr, 'calcuating E(P_m) for L={l}, Nc={Nci}-{Ncj}'.format(l=L, Nci=N_c_i, Ncj=N_c_j)
    for i in xrange(N_c_i, N_c_j):
        print >>sys.stderr, '...working on Nc={nc}'.format(nc=i)
        e = E(L, i, N=N, Ns=Ns)
        results[i] = np.mean(e[:,0])
    #print >>sys.stderr, results
    fn = 'E_{l}'.format(l=L) 
    np.save(fn, results)
    return fn+'.npy'


def calc_expected_mat(L_i, L_j, N=1000, Ns=1000, threads=2):
    # calc E(P_m) for genomes of length L_i through L_j
    lengths = np.arange(L_i, L_j)
    files = parallel_map(lambda L: calc_E_over_Nc_range(L, L_j, 2, L+1, N=N, Ns=Ns), lengths, threads=threads)
    return files

class LambdaHandler:
    
    def __init__(self, Ng=1000, Ns=1000):
        self.Ng = Ng
        self.Ns = Ns
        self.exp_lambdas = {}

    @classmethod
    def load(cls, fn, Ng=100, Ns=1000):
        newlh = cls(Ng=Ng, Ns=Ns)
        with open(fn, 'rb') as in_fp:
            in_fp.next()
            for line in in_fp:
                vals = line.split(',')
                L = int(vals[0].strip())
                Nc = int(vals[1].strip())
                e = np.float(vals[2].strip())
                print L, Nc, e
                if L not in newlh.exp_lambdas:
                    newlh.exp_lambdas[L] = {}
                newlh.exp_lambdas[L][Nc] = e
        return newlh

    def get_expected(self, L, Nc):
        if L in self.exp_lambdas and Nc in self.exp_lambdas[L]:
            return self.exp_lambdas[L][Nc]
        else:
            result = E(L, Nc, N=self.Ng, Ns=self.Ns)
            exp_l = np.mean(result[:,0])
            print >>sys.stderr, '...calculated expected for', L, Nc, exp_l
            if L not in self.exp_lambdas:
                self.exp_lambdas[L] = {}
            self.exp_lambdas[L][Nc] = exp_l
            return exp_l

    def Lambda(self, G, N=1000, t=1, S=2):
        result = P_m(G, N=N, t=t, S=S)
        mu = result[0]
        Nc = len(np.where(G >= t)[0])
        L = len(G)
        if Nc == 0:
            return float('NaN'), L, Nc
        expected = self.get_expected(L, Nc)
        return -2.0 * np.log(expected/mu), L, Nc

    def save(self, fn):
        print >>sys.stderr, 'saving expected Pm to', fn
        with open(fn, 'wb') as out_fp:
            out_fp.write('L, Nc, E\n')
            for L in self.exp_lambdas:
                for Nc in self.exp_lambdas[L]:
                    out_fp.write('{l}, {nc}, {e}\n'.format(l=L, nc=Nc, e=self.exp_lambdas[L][Nc]))   


def process_lambda(org_id, datadir, lh):
    fn = os.path.join(datadir, 'data/dom_lineage/tasksites.org-{i}.dat'.format(i=org_id))
    _, taskmap = orgmap.parse_taskmap(fn)
    lam, L, Nc = lh.Lambda(taskmap)
    return lam, L, Nc


def process_run(datadir, lh):
    fn = os.path.join(datadir, 'data/dom_lineage_orgs.dat')
    df = orgmap.get_org_mat(fn)
    print df
    df['Lambda'] = float('NaN')
    df['length'] = float('NaN')
    df['Nc'] = float('NaN')
    for i in xrange(1, len(df)):
        if i % 100 == 0:
            print 'processed {} orgs...'.format(i)
        lam, L, Nc = process_lambda(int(df.ix[i,1]), datadir, lh)
        df.ix[i,'Lambda'] = lam
        df.ix[i, 'length'] = L
        df.ix[i, 'Nc'] = Nc
    df = df.ix[1:]
    print df
    return df


def handle_process_runs(args):
    if args.load_exp:
        lh = LambdaHandler.load(args.load_exp, Ng=args.Ng, Ns=args.Ns)
    else:
        lh = LambdaHandler(Ng=args.Ng, Ns=args.Ns)
    for datadir in args.datadirs:
        print >>sys.stderr, 'processing', datadir
        df = process_run(datadir, lh)
        outname = args.prefix + '_' + os.path.basename(datadir) + '.dat'
        outfn = os.path.join(args.outdir, outname)
        print outname
        print >>sys.stderr, 'saving processed results to', outfn
        df.to_csv(outfn, na_rep='NaN', index=False)
        if args.save_exp:
            lh.save(args.save_exp)

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations-per-class', dest='Ng', type=int, default=1000)
    parser.add_argument('--iterations-per-org', dest='Ns', type=int, default=1000)
    parser.add_argument('--load-exp-from', dest='load_exp')
    parser.add_argument('--save-exp-to', dest='save_exp')
    parser.add_argument('--datadirs', nargs='+')
    parser.add_argument('--outdir', default='')
    parser.add_argument('--prefix', default='lambda')
    args = parser.parse_args()
    
    handle_process_runs(args)
        
if __name__ == '__main__':
    main()
