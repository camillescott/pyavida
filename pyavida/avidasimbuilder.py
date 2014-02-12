#!/usr/bin/env python

from config import *

from shutil import rmtree
import sys
import argparse
import random
from jinja2 import Environment, PackageLoader

class PyAvidaError(Exception):
    pass

class FileMissingError(PyAvidaError):
    def __init__(self, fn):
        self.fn = fn

def sep():
    sep = '*' * 40
    print >>sys.stderr, sep + '\n'

# Check that the given dir contains proper avida files
def chkconfig(d):
    for fn in CONFIG_FILES.values():
        if not os.path.isfile(fn):
            raise FileMissingError(fn)

def mk_folders(out_dir, prefix, x, force):
    folders = []
    for i in xrange(x):
        p = os.path.join(os.path.abspath(out_dir), '{p}_{i}'.format(p=prefix, i=i)) 
        try:
            os.makedirs(p)
        except OSError as e:
            print >>sys.stderr, e, 'folder already exists', p
        finally:
            if force:
                print >>sys.stderr, '-f is on, replacing dir...'
                rmtree(p)
                os.makedirs(p)
        folders.append(p)
    return folders

def ln_configs(folders, args):
    for folder in folders:
        for cfile in CONFIG_FILES.values():
            try:
                link = os.path.join(folder, os.path.basename(cfile)) 
                os.symlink(cfile, link)
            except OSError as e:
                print >>sys.stderr, e, 'link already exists', link

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument('--prefix', help='run directory prefix', dest='prefix', default='data')
    parser.add_argument('--outdir', help='output directory for all runs', dest='out_dir', default='.')
    parser.add_argument('--avidacfg', dest='avidacfg', 
                        default=CONFIG_FILES['avidacfg'])
    parser.add_argument('--org', dest='org', 
                        default=CONFIG_FILES['org'])
    parser.add_argument('--events', dest='events',
                        default=CONFIG_FILES['events'])
    parser.add_argument('--analyze', dest='analyze',
                        default=CONFIG_FILES['analyze'])
    parser.add_argument('--env', dest='env',
                        default=CONFIG_FILES['env'])
    parser.add_argument('--instset', dest='instset',
                        default=CONFIG_FILES['instset'])
    parser.add_argument('--exe', dest='exe',
                        default=CONFIG_FILES['exe'])
    parser.add_argument('-f', dest='force', action='store_true')
    parser.add_argument('-x', '--replicates', dest='replicates', default=DEF_REPLICATES, type=int)
    parser.add_argument('-o', type=argparse.FileType('w'),
                        dest='outfp', default=sys.stdout)
    args = parser.parse_args()
    
    if args.org:
        CONFIG_FILES['org'] = os.path.abspath(args.org)
    if args.events:
        CONFIG_FILES['events'] = os.path.abspath(args.events)
    if args.analyze:
        CONFIG_FILES['analyze'] = os.path.abspath(args.analyze)
    if args.env:
        CONFIG_FILES['env'] = os.path.abspath(args.env)
    if args.instset:
        CONFIG_FILES['instset'] = os.path.abspath(args.instset)
    if args.exe:
        CONFIG_FILES['exe'] = os.path.abspath(args.exe)
    if args.avidacfg:
        CONFIG_FILES['avidacfg'] = os.path.abspath(args.avidacfg)

    sep()
    print >>sys.stderr, 'Checking configuration files...'
    try:    
        chkconfig(CONFIG_FILES)
    except FileMissingError as e:
        print >>sys.stderr, '**ERR: missing config file {e}'.format(e=e.fn)
        print >>sys.stderr, 'Exiting...'
        sys.exit()
    print >>sys.stderr, 'Config file check passed!'
    sep()

    print >>sys.stderr, 'Creating folders...'
    folders = mk_folders(args.out_dir, args.prefix, args.replicates, args.force)
    print >>sys.stderr, '...linking config files...'
    ln_configs(folders, args)
    print >>sys.stderr, '...done creating workspaces!'
    sep()

    print >>sys.stderr, 'Created the following workspaces:\n'
    args.outfp.write('\t'.join(folders) + '\n')

if __name__ == '__main__':
    main()
