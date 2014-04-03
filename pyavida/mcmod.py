#import scipy as sp
import numpy as np
import os

def check_region(G, x, y, t=1):
    for i in xrange(x,y):
        if G[i] < t:
            return False
    return True


def P_m(G, N=1000, t=1, S=2):
    results = np.zeros(N)
    coding = np.where(G == t)[0]
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
    def load(cls, fn, Ng=1000, Ns=1000):
        newlh = cls(Ng=Ng, Ns=Ns)
        with open(fn, 'rb') as in_fp:
            in_fp.next()
            for line in in_fp:
                vals = line.split(',')
                L = int(vals[0].strip())
                Nc = int(vals[1].strip())
                e = np.float(vals[2].strip())
                newlh.exp_lambdas[L][Nc] = e
        return newlh

    def get_expected(L, Nc):
        if L in self.exp_lambdas and Nc in self.exp_lambdas[L]:
            return self.exp_lambdas[L][Nc]
        else:
            exp_l = E(L, Nc, N=self.Ng, Ns=self.Ns)
            self.exp_lambdas[L][Nc] = exp_l
            return exp_l

    def Lambda(G, N=1000, t=1, S=2):
        result = P_m(G, N=N, t=t, S=S)
        mu = result[0]
        Nc = len(np.where(G >= t)[0])
        L = len(G)
        expected = self.get_expected(Nc, L)
        return (-2.0 * np.log(expected) + 2.0 * np.log(mu))

    def save(fn):
        print >>sys.stderr, 'saving expected Pm to', fn
        with open(fn, 'wb') as out_fp:
            out_fp.write('L, Nc, E\n')
            for L in self.exp_lambdas:
                for Nc in self.exp_lambdas[L]:
                    out_fp.write('{l}, {nc}, {e}\n'.format(l=L, nc=Nc, e=self.exp_lambdas[L][Nc]))

import orgmap

def process_lambda(X, d, lh):
    org_id = int(X[1])
    fn = os.path.join(d, 'dom_lineage/tasksites.org-{i}.dat'.format(i=org_id))
    _, taskmap = orgmap.parse_taskmap(fn)
    l = lh.Lambda(taskmap)
    return l

def process_run(datadir, lh):
    fn = os.path.join(datadir, 'dom_lineage_orgs.dat')
    df = orgmap.get_org_mat(fn)
    L_d = df[df.u_birth > 0].apply(process_lambda, axis=1, raw=True, args=(datadir,lh))   
    df.insert(6, 'Lambda', L_d)
    return df

def handle_calc_M_exp(args):

    if args.load:
        nums = eval(args.load)
        assert type(nums) == list
        pairs = [(nums[i-1],nums[i]) for i in range(1,len(nums))]
        files = []
        for i,j in pairs:
            files.append('E_{i}_{j}.mat.csv'.format(i=i,j=j))
        files = map(lambda f: os.path.join('E_Pm', f), files)
        files.sort(key=lambda s: s.split('_')[1])
        
        mat = np.zeros( (max(nums),max(nums)) )
        for file,(i,j) in zip(files,pairs):
            mat_ij = np.loadtxt(file, delimiter=',')
            mat[i:j,:j] = mat_ij
        np.savetxt('E_{i}_{j}.mat.csv'.format(i=min(nums),j=max(nums)), mat, delimiter=',')
     
    else:
        files = calc_expected_mat(args.L_i, args.L_j, N=args.N, Ns=args.Ns, threads=args.threads)

        results = []
        for f in files:
            results.append(np.load(f))
        results = np.array(results)
        np.savetxt('E_{s}_{e}.mat.csv'.format(s=args.L_i, e=args.L_j), results, delimiter=',')

def handle_process_runs(args):
    for datadir in args.datadirs:
        pass 

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--threads', dest='threads', type=int, default=2)
    parser.add_argument('--iterations-per-class', dest='N', type=int, default=1000)
    parser.add_argument('--iterations-per-org', dest='Ns', type=int, default=1000)
    parser.add_argument('--load', dest='load')
    parser.add_argument('--load-from', dest='folder')
    parser.add_argument('L_i', type=int)
    parser.add_argument('L_j', type=int)
    args = parser.parse_args()
    

        
if __name__ == '__main__':
    main()
