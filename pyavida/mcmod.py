import scipy as sp
import pandas as pd
import numpy as np

def check_region(G, x, y, t=1):
    for i in xrange(x,y):
        if G[i] < t:
            return False
    return True


def P_m(G, N=1000, t=1, S=2):
    results = np.zeros(N)
    coding = np.where(G >= t)[0]
    #print coding
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
    
    coding = np.random.randint(0, high=L, size=N_c)
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
    
    results = np.zeros((N,2))
    for i in xrange(N):
        Rs = calc_random(L=L, N_c=N_c, N=Ns)
        results[i,:] = Rs[:2]
    return results

def calc_E_over_Nc_range(L, Lm, N_c_i, N_c_j, outfp, N=1000, Ns=1000, q=None):
    results = np.zeros( Lm )
    for i in xrange(N_c_i, N_c_j):
        e = E(L, i, N=N, Ns=Ns)
        results[i] = e[0]
    np.savetxt(outfp, results, delimiter=' ')
    if q:
        q.put(L)
    

import Queue
import threading

def calc_expected_mat(L_i, L_j, N=1000, Ns=1000):
   pass 
