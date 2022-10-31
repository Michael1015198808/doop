#!/usr/bin/env python
import os
import sys

ALLAPP = ['bloat', 'xalan', 'hsqldb', 'eclipse', 'jython',
         'findbugs', 'soot', 'gruntspud', 'columba', 'jedit', 'freecol', 'briss']
ANALYSIS = ['context-insensitive', '2-object-sensitive+heap', '2-type-sensitive+heap', 'zipper-e', 'cut-shortcut', 'collection-3obj']

APPINPUT = {
    'findbugs' : 'benchmarks/findbugs/3.0/lib/findbugs.jar benchmarks/findbugs/3.0/plugin/coreplugin.jar',
    'soot' : 'benchmarks/soot/2.3.0/sootclasses-2.3.0.jar',
    'gruntspud' : 'benchmarks/gruntspud/0.4.6/GruntspudSA.jar',
    'columba' : 'benchmarks/columba/1.4/columba.jar',
    'jedit' : 'benchmarks/jedit/3.0/jedit.jar',
    'freecol' : 'benchmarks/freecol/0.10.3/FreeCol.jar',
    'briss' : 'benchmarks/briss/0.9/briss-0.9.jar',
    'hsqldb' : 'benchmarks/dacapo-2006/hsqldb.jar',
    'eclipse' : 'benchmarks/dacapo-2006/eclipse.jar',
    'xalan' : 'benchmarks/dacapo-2006/xalan.jar',
    'bloat' : 'benchmarks/dacapo-2006/bloat.jar',
    'jython' : 'benchmarks/dacapo-2006/jython.jar'

}

APPLIB = {
    'findbugs' : 'benchmarks/findbugs/3.0/lib',
    'soot' : 'benchmarks/soot/2.3.0',
    'columba' : 'benchmarks/columba/1.4/lib benchmarks/columba/1.4/native/linux',
    'jedit' : 'benchmarks/jedit/3.0/lib',
    'freecol' : 'benchmarks/freecol/0.10.3/jars',
    'briss' : 'benchmarks/briss/0.9',
    'hsqldb' : 'benchmarks/dacapo-2006/hsqldb-deps.jar',
    'eclipse' : 'benchmarks/dacapo-2006/eclipse-deps.jar',
    'xalan' : 'benchmarks/dacapo-2006/xalan-deps.jar',
    'bloat' : 'benchmarks/dacapo-2006/bloat-deps.jar',
    'jython' : 'benchmarks/dacapo-2006/jython-deps.jar'
}

APPTAMIFLEX = {
    'findbugs' : 'benchmarks/findbugs/3.0/refl.log',
    'soot' : 'benchmarks/soot/2.3.0/refl.log',
    'gruntspud' : 'benchmarks/gruntspud/0.4.6/refl.log',
    'columba' : 'benchmarks/columba/1.4/refl.log',
    'jedit' : 'benchmarks/jedit/3.0/refl.log',
    'freecol' : 'benchmarks/freecol/0.10.3/refl.log',
    'briss' : 'benchmarks/briss/0.9/refl.log',
    'hsqldb' : 'benchmarks/dacapo-2006/hsqldb-refl.log',
    'eclipse' : 'benchmarks/dacapo-2006/eclipse-refl.log',
    'xalan' : 'benchmarks/dacapo-2006/xalan-refl.log',
    'bloat' : 'benchmarks/dacapo-2006/bloat-refl.log',
    'jython' : 'benchmarks/dacapo-2006/jython-refl.log'
}

APPMAIN = {
    'findbugs' : 'edu.umd.cs.findbugs.FindBugs2',
    'soot' : 'soot.Main',
    'gruntspud' : 'gruntspud.standalone.JDK13GruntspudHost',
    'columba' : 'org.columba.core.main.Main',
    'jedit' : 'org.gjt.sp.jedit.jEdit',
    'freecol' : 'net.sf.freecol.FreeCol',
    'briss' : 'at.laborg.briss.Briss',
    'hsqldb' : 'Harness',
    'eclipse' : 'Harness',
    'xalan' : 'Harness',
    'bloat' : 'Harness',
    'jython' : 'Harness'
}

DOOPHOME = os.path.dirname(os.path.realpath(__file__))


# This script should be executed from the root directory of Doop.
# ---------------------------------------------------------

RESET = '\033[0m'
YELLOW = '\033[33m'
BOLD = '\033[1m'

def runDoop(app, analyse):
    os.environ['DOOP_PLATFORMS_LIB'] = os.path.join(DOOPHOME, 'benchmarks')
    cmd = ''
    if analyse  == 'zipper-e':
        cmd = cmd + 'python bin/zippere.py -a 2-object-sensitive+heap'
    else :    
        cmd = cmd +"./doop -a "+analyse
    cmd = cmd + ' -i '+APPINPUT[app]
    if APPLIB.has_key(app):
        cmd = cmd + ' -l '+APPLIB[app]
    cmd = cmd + ' --platform java_6'
    cmd = cmd + ' --tamiflex '+APPTAMIFLEX[app]
    cmd = cmd + ' --main '+APPMAIN[app]
    cmd = cmd + ' --cs-library'
    cmd = cmd + ' --no-merge-library-objects'
    cmd = cmd + ' --Xno-ssa'
    print YELLOW + BOLD + 'Running ' + analyse+ ' for '+app+"...."+RESET
    print cmd
    os.system(cmd)
    clearcmd = 'rm -rf out'
    os.system(clearcmd)
    print clearcmd
    if analyse  == 'zipper-e':
        clearcmd = 'rm -rf zipper/cache'
        os.system(clearcmd)
        print clearcmd
        clearcmd = 'rm -rf zipper/out'
        os.system(clearcmd)
        print clearcmd

def run(args):
    apps = []
    analyses = []
    for arg in args:
        if arg in ALLAPP:
            apps.append(arg)
        elif arg in ANALYSIS:
            analyses.append(arg)
        else:
            print 'wrong input'
            sys.exit()
    for app in apps:
        for analyse in analyses:
            runDoop(app, analyse)

if __name__ == '__main__':
    run(sys.argv[1:])

