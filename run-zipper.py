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

ZIPPER_HOME = '../zipper/zipper'
ZIPPER_CP = ':'.join([
    os.path.join(ZIPPER_HOME, 'build', 'zipper.jar'),
    os.path.join(ZIPPER_HOME, 'lib', 'guava-23.0.jar'),
    os.path.join(ZIPPER_HOME, 'lib', 'sootclasses-2.5.0.jar'),
])
ZIPPER_MAIN = 'ptatoolkit.zipper.Main'
ZIPPER_PTA = 'ptatoolkit.zipper.doop.DoopPointsToAnalysis'
ZIPPER_CACHE = 'cache/zipper'
ZIPPER_OUT = 'results'

ZIPPER_THREAD = 4 # multiprocessing.cpu_count() # use multithreading to accelerate Zipper
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

INS_LEVEL = False

def runPreAnalysis(initArgs):
    args = [DOOP, "--Xzipper-pre", "--Xzipper-ins-tracker" if INS_LEVEL else ""] + [a if a not in ANALYSES else PRE_ANALYSIS for a in initArgs]
    cmd = ' '.join(args)
    print(YELLOW + BOLD + 'Running pre-analysis ...' + RESET)
    print("Pre-analysis cmd:")
    print(cmd)
    os.system(cmd)


def runZipper(app, cache_dir, out_dir, express):
    suffix = ''
    if express:
        suffix = '-express'
    zipper_ins_dic = {
        "methods": os.path.join(out_dir, '%s-ZipperPrecisionCriticalMethod%s.facts' % (app, suffix)),
        "heap_allocation": os.path.join(out_dir, '%s-InsAssignHeapAllocation.facts' % app),
        "local_assign": os.path.join(out_dir, '%s-InsAssignLocal.facts' % app),
        "casts": os.path.join(out_dir, '%s-InsAssignCast.facts' % app),
        "instance_load": os.path.join(out_dir, '%s-InsLoadInstanceField.facts' % app),
        "array_load": os.path.join(out_dir, '%s-InsLoadArrayIndex.facts' % app),
    }

    for file in zipper_ins_dic.values():
        if os.path.exists(file):
            os.remove(file) # remove old file

    cmd = 'java -Xmx%s ' % ZIPPER_MEMORY
    cmd += ' -cp %s ' % ZIPPER_CP
    cmd += ZIPPER_MAIN
    cmd += ' -pta %s ' % ZIPPER_PTA
    cmd += ' -app %s ' % app
    cmd += ' -cache %s ' % cache_dir
    cmd += ' -out %s ' % out_dir
    if INS_LEVEL:
        cmd += '-ins-level' # not '--ins-level'
    # cmd += ' -debug'
    if ZIPPER_THREAD > 1:
        cmd += ' -thread %d ' % ZIPPER_THREAD
    if express:
        cmd += ' -express %f ' % express
    print("Zipper analysis cmd:")
    print(cmd)
    os.system(cmd)
    return zipper_ins_dic

def runMainAnalysis(args, zipper_ins_file_dic):
    zipper_ins_args = [
        '--instruction-level',
        '--ins-assignheapallocation', zipper_ins_file_dic['heap_allocation'],
        '--ins-assignlocal', zipper_ins_file_dic['local_assign'],
        '--ins-assigncast', zipper_ins_file_dic['casts'],
        '--ins-loadinstancefield', zipper_ins_file_dic['instance_load'],
        '--ins-loadarrayindex', zipper_ins_file_dic['array_load'],
    ]
    args = [DOOP, '--Xzipper', zipper_ins_file_dic['methods']] \
            + (zipper_ins_args if INS_LEVEL else []) \
            + args # you may add '--cache' between DOOP and '--Xzipper'
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
            elif args[i] == '--ins-level':
                REQUIRED_QURIES.extend(['ASSIGN_CAST', 'INSTANCE_LOAD_CAUSE', 'ARRAY_LOAD_CAUSE'])
                global INS_LEVEL
                INS_LEVEL = True
            elif args[i] == "--souffle-jobs":
                global ZIPPER_THREAD
                ZIPPER_THREAD = int(args[i+1])
                res.append(args[i])
                res.append(args[i+1])
                i += 1
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
    zipper_in_file_dic = runZipper(APP, ZIPPER_CACHE, ZIPPER_OUT, express)
    runMainAnalysis(args, zipper_in_file_dic)

if __name__ == '__main__':
    """
    example (run this command in './', i.e. doop):
    python ./run-zipper.py -a 2-object-sensitive+heap -i benchmarks/dacapo-2006/eclipse.jar --dacapo --platform java_6
    """
    run(sys.argv[1:])
