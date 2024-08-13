#!/usr/bin/env python
import os
import shutil
import sys
import multiprocessing

# This script should be executed from the root directory of Doop.

# ----------------- configuration -------------------------
DOOP = './doop'
PRE_ANALYSIS = 'context-insensitive'
DATABASE = 'last-analysis'
ANALYSES = [
    'context-insensitive',
    '2-object-sensitive+heap',
    '2-call-site-sensitive+heap',
    '2-type-sensitive+heap',          
    'refA-2-object-sensitive+heap',
    'refA-2-type-sensitive+heap',
    'refA-2-call-site-sensitive+heap',
    'refB-2-object-sensitive+heap',
    'refB-2-type-sensitive+heap',
    'refB-2-call-site-sensitive+heap',
]

APP = 'temp'

ZIPPER_HOME = './zipper'
ZIPPER_CP = ':'.join([
    os.path.join(ZIPPER_HOME, 'build', 'zipper.jar'),
    os.path.join(ZIPPER_HOME, 'lib', 'guava-23.0.jar'),
    os.path.join(ZIPPER_HOME, 'lib', 'sootclasses-2.5.0.jar'),
])
ZIPPER_MAIN = 'ptatoolkit.zipper.Main'
ZIPPER_PTA = 'ptatoolkit.zipper.doop.DoopPointsToAnalysis'
ZIPPER_CACHE = 'cache/zipper'
ZIPPER_OUT = 'results'

ZIPPER_THREAD = multiprocessing.cpu_count() # use multithreading to accelerate Zipper
ZIPPER_MEMORY = '48g'

REQUIRED_QURIES = [
    'ARRAY_LOAD', 'ARRAY_STORE',
    'CALL_EDGE', 'CALL_RETURN_TO', 'CALLSITEIN', 'DIRECT_SUPER_TYPE',
    'INST_CALL_RECV', 'INST_METHODS', 'INSTANCE_LOAD', 'INSTANCE_STORE', 
    'INTERPROCEDURAL_ASSIGN', 'LOCAL_ASSIGN', 'METHOD_MODIFIER',
    'OBJ_TYPE', 'OBJECT_ASSIGN', 'OBJECT_IN',
    'PARAMS', 'RET_VARS', 'SPECIAL_OBJECTS',
    'THIS_VAR', 'VAR_IN', 'VPT',
]

# ---------------------------------------------------------

RESET = '\033[0m'
YELLOW = '\033[33m'
BOLD = '\033[1m'

def runPreAnalysis(initArgs):
    args = [DOOP, "--Xzipper-pre"] + [a if a not in ANALYSES else PRE_ANALYSIS for a in initArgs]
    cmd = ' '.join(args)
    print(YELLOW + BOLD + 'Running pre-analysis ...' + RESET)
    print("Pre-analysis cmd:")
    print(cmd)
    os.system(cmd)


def runZipper(app, cache_dir, out_dir, express):
    suffix = ''
    if express:
        suffix = '-express'
    zipper_file = os.path.join(out_dir, \
        '%s-ZipperPrecisionCriticalMethod%s.facts' % (app, suffix))
    if os.path.exists(zipper_file):
        os.remove(zipper_file) # remove old file

    cmd = 'java -Xmx%s ' % ZIPPER_MEMORY
    cmd += ' -cp %s ' % ZIPPER_CP
    cmd += ZIPPER_MAIN
    cmd += ' -pta %s ' % ZIPPER_PTA
    cmd += ' -app %s ' % app
    cmd += ' -cache %s ' % cache_dir
    cmd += ' -out %s ' % out_dir
    # cmd += ' -debug'
    if ZIPPER_THREAD > 1:
        cmd += ' -thread %d ' % ZIPPER_THREAD
    if express:
        cmd += ' -express %f ' % express
    print("Zipper analysis cmd:")
    print(cmd)
    os.system(cmd)
    return zipper_file

def runMainAnalysis(args, zipper_file):
    args = [DOOP, '--Xzipper', zipper_file] + args # you may add '--cache' between DOOP and '--Xzipper'
    cmd = ' '.join(args)
    print(YELLOW + BOLD + 'Running main (Zipper-guided) analysis ...' + RESET)
    print("Main analysis cmd:")
    print(cmd)
    os.system(cmd)

def movePreAnalysisResult():
    output = os.path.join(ZIPPER_CACHE)
    if os.path.exists(output):
        print("Old zipper cache exists, remove:", output)
        shutil.rmtree(output)
    os.mkdir(output)
    for file in os.listdir(DATABASE):
        factName = file.split(".")[0]
        if factName in REQUIRED_QURIES:
            shutil.copyfile(os.path.join(DATABASE, file), os.path.join(output, "%s.%s" % (APP, factName)))
    

def run(args):
    def processArgs(args):
        res = []
        express = None
        i = 0
        while i < len(args):
            if args[i] == '-e':
                if isFloat(args[i+1]):
                    express = float(args[i+1])
                    i += 1
                else:
                    express = 0.05 # default threshold for Zipper-e
            else:
                res.append(args[i])
            i += 1
        return res, express

    def isFloat(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    args, express = processArgs(args)
    # print(args, express)
    runPreAnalysis(args)
    movePreAnalysisResult()
    # dumpRequiredDoopResults(APP, DATABASE, ZIPPER_CACHE)
    zipper_file = runZipper(APP, ZIPPER_CACHE, ZIPPER_OUT, express)
    runMainAnalysis(args, zipper_file)

if __name__ == '__main__':
    """
    example (run this command in './', i.e. doop):
    python ./run-zipper.py -a 2-object-sensitive+heap -i benchmarks/dacapo-2006/eclipse.jar --dacapo --platform java_6
    """
    run(sys.argv[1:])
