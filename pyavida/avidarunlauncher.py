from jinja2 import Environment, PackageLoader
import argparse
import subprocess
import sys
import random

from config import *

def build_scripts(folders, args, jenv):
    t = jenv.get_template('submit.pbs')
    analyze = not args.analyze
    scripts = [t.render(folder=os.path.abspath(folder), buyin=args.buyin,
                        resources=args.resources, analyze=analyze,
                        jobname=args.job_prefix+os.path.basename(folder),
                        seed=random.randint(0,9999999999999999999)) \
                for folder in folders]
    return scripts

def write_scripts(folders, scripts):
    script_files = []
    for folder, script in zip(folders, scripts):
        fn = os.path.join(folder, 'run_avida.pbs')
        with open(fn, 'w') as outfp:
            outfp.write(script)
            script_files.append(fn)
    return script_files

def qsub_script(script_file):
    cmd = ['qsub', script_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    jid = ''.join(p.stdout)
    return jid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--folderlist', dest='folderlist', 
        type=argparse.FileType('w'), default=sys.stdin)
    parser.add_argument('--resources', dest='resources',
        default=RESOURCES)
    parser.add_argument('--buyin', dest='buyin',
        default=BUYIN)
    parser.add_argument('--job-prefix', dest='job_prefix',
        default=JOB_PREFIX)
    parser.add_argument('--submit', dest='submit', action='store_true')
    parser.add_argument('--no-analyze', dest='analyze', action='store_true')
    args = parser.parse_args()

    folders = args.folderlist.readline().strip().split('\t')
    jenv = Environment(loader=PackageLoader('avidarunlauncher', '../templates'))

    print >>sys.stderr, 'building job scripts from templates...'
    scripts = build_scripts(folders, args, jenv)
    print >>sys.stderr, 'writing scripts to files...'
    script_files = write_scripts(folders, scripts)
    
    if args.submit:
        print >>sys.stderr, 'submitting jobs to torque...'
        for fn in script_files:
            jid = qsub_script(fn)
            print jid

if __name__ == '__main__':
    main()
