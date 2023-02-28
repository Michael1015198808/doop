#!/usr/bin/env python
import os
import shutil
import sys
import multiprocessing

# This script should be executed from the root directory of Doop.

# ----------------- configuration -------------------------
DOOP = './doop' # './doopOffline'
PRE_ANALYSIS = 'context-insensitive'
DATABASE = 'last-analysis'

APP = 'temp'
SEP = '"\t"'

ZIPPER_CP = ':'.join(['zipper/lib/zipper.jar', 'zipper/lib/guava-23.0.jar'])
ZIPPER_MAIN = 'ptatoolkit.zipper.Main'
ZIPPER_PTA = 'ptatoolkit.zipper.doop.DoopPointsToAnalysis'
ZIPPER_EXPRESS_THRESHOLD = 0.05
ZIPPER_CACHE = 'zipper/cache'
ZIPPER_OUT = 'zipper/out'
THREAD = multiprocessing.cpu_count() # use multithreading to accelerate Zipper
HEAP_SIZE = '96g'
STACK_SIZE = '4m'

# ---------------------------------------------------------

RESET = '\033[0m'
YELLOW = '\033[33m'
BOLD = '\033[1m'

def runPreAnalysis(initArgs):
    args = list(initArgs)
    for opt in ['-a', '--analysis']:
        if opt in args:
            i = args.index(opt)
            del args[i] # delete '-a' or '--analysis'
            del args[i] # delete the analysis argument
    args = [DOOP] + args
    args = args + ['-a', PRE_ANALYSIS]
    args = args + ['--Xzipper-pre']
    cmd = ' '.join(args)
    print (YELLOW + BOLD + 'Running pre-analysis ...' + RESET)
    #print cmd
    os.system(cmd)

def dumpRequiredDoopResults(app, db_dir, dump_dir):
    INPUT = {
        'APP_METHODS': 'Stats_Simple_Application_ReachableMethod',
        'VPT': 'Stats_Simple_InsensVarPointsTo'
    }

    REQUIRED_INPUT = [
        'APP_METHODS', 'ARRAY_LOAD', 'ARRAY_STORE', 'ASSIGN_COMPATIBLE',
        'CALLSITE_IN', 'CALL_EDGE', 'CALL_RETURN_TO', 'DIRECT_SUPER_TYPE',
        'INSTANCE_LOAD', 'INSTANCE_STORE', 'INST_CALL_RECV', 'INST_METHODS',
        'INTERPROCEDURAL_ASSIGN', 'LOCAL_ASSIGN', 'METHOD_MODIFIER',
        'OBJECT_ASSIGN', 'OBJECT_IN', 'OBJ_TYPE', 'PARAMS', 'RET_VARS',
        'SPECIAL_OBJECTS', 'THIS_VAR', 'VAR_IN', 'VAR_TYPE', 'VPT',
    ]

    def dumpDoopResults(db_dir, dump_dir, app, query):
        file_name = INPUT.get(query, query) + '.csv'
        from_path = os.path.join(db_dir, file_name)
        dump_path = os.path.join(dump_dir, '%s.%s' % (app, query))
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        shutil.copyfile(from_path, dump_path)
    
    print ('Dumping doop analysis results %s ...' % app)
    for query in REQUIRED_INPUT:
        dumpDoopResults(db_dir, dump_dir, app, query)

def runZipper(app, cache_dir, out_dir):
    cmd = 'java -Xmx%s -Xss%s ' % (HEAP_SIZE, STACK_SIZE)
    cmd += ' -cp %s ' % ZIPPER_CP
    cmd += ZIPPER_MAIN
    cmd += ' -sep %s ' % SEP
    cmd += ' -pta %s ' % ZIPPER_PTA
    cmd += ' -app %s ' % app
    cmd += ' -cache %s ' % cache_dir
    cmd += ' -out %s ' % out_dir
    cmd += ' -express %s ' % str(ZIPPER_EXPRESS_THRESHOLD)
    cmd += ' -thread %d ' % THREAD
    #print cmd
    os.system(cmd)

    zipper_file = os.path.join(out_dir, \
        '%s-ZipperPrecisionCriticalMethod.facts' % app)
    return zipper_file

def runMainAnalysis(args, zipper_file):
    args = [DOOP] + args
    args = args + ['--Xzipper', zipper_file]
    cmd = ' '.join(args)
    print (YELLOW + BOLD + 'Running main (Zipper-guided) analysis ...' + RESET)
    #print cmd
    os.system(cmd)

def run(args):
    runPreAnalysis(args)
    dumpRequiredDoopResults(APP, DATABASE, ZIPPER_CACHE)
    zipper_file = runZipper(APP, ZIPPER_CACHE, ZIPPER_OUT)
    # runMainAnalysis(args, zipper_file)

if __name__ == '__main__':
    APP = sys.argv[2]
    run(sys.argv[3:])


