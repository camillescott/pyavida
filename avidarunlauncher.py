import jinja2
import argparse
from config import *

def build_scripts(folders, args, jenv):
    t = jenv.get_template('submit.pbs')
    
    scripts = [t.render(folder=os.path.abspath(folder), buy=args.buyin,
                        resources=args.resources, 
                        jobname=args.job_prefix+folder,
                        seed=random.randint(0,9999999999999999999)) \
                for folder in folders]
    return scripts

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
    args = parser.parse_args()

    folders = args.folderlist.read().split('\t')
    
    jenv = Environment(loader=PackageLoader('pyavida', 'templates'))

    scripts = build_scripts(folders, args, jenv)
    
