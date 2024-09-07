import os
from pathlib import Path
from multiprocessing import Pool

tests = {
    # "batik": "./benchmarks/dacapo-bach/batik.jar",
    "sunflow": "./benchmarks/dacapo-bach/sunflow.jar",
    "eclipse": "./benchmarks/dacapo-2006/eclipse.jar",
    "chart": "./benchmarks/dacapo-2006/chart.jar",
    "fop": "./benchmarks/dacapo-2006/fop.jar",
    "xalan": "./benchmarks/dacapo-2006/xalan.jar",
    # "bloat": "./benchmarks/dacapo-2006/bloat.jar",
}

def runTest(resultPath:str, cmd:str):
    Path(resultPath).mkdir(parents=True, exist_ok=True)
    cmdList = [cmd.format(benchName=k, resPath=resultPath, benchPath=v) for (k, v) in tests.items()]
    # with Pool(8) as p:
    #     p.map(os.system, cmdList)
    for cmd in cmdList:
        os.system(cmd)

cmd2obj = "./doop -a 2-object-sensitive+heap -i {benchPath} --dacapo --platform java_6 > {resPath}/{benchName}"

run2obj = lambda: runTest("./sdiff/2-obj", cmd2obj)

cmdZipper = "python ./run-zipper.py -a 2-object-sensitive+heap -i {benchPath} --dacapo --platform java_6 > {resPath}/{benchName}"

runZipper = lambda: runTest("./sdiff/zipper", cmdZipper)

datas = {
    "time": "analysis execution time (sec)",
    "fail-cast": "reachable casts that may fail",
    "poly-call": "polymorphic virtual call sites",
    "reach-mtd": "reachable methods (INS)",
    "call-edge": "call graph edges (INS)"
}

def readData(benchResPath):
    txt = Path(benchResPath).read_text()
    txt = txt[txt.rfind("Runtime metrics") : ]
    lines = txt.split("\n")
    res = {}
    for l in lines:
        for k, v in datas.items():
            if l.startswith(v):
                res[k] = l.split()[-1]
        if len(res) == 5:
            break
    return res

def processData(path, round):
    header = "Benchmark;time;fail-cast;poly-call;reach-mtd;call-edge"
    benchs = tests.keys()
    datas = map(lambda bench: (bench, readData(os.path.join(path, bench))), benchs)
    line = "%s;%s;%s;%s;%s;%s"
    lines = map(lambda p: line % (p[0], p[1]["time"], p[1]["fail-cast"], p[1]["poly-call"], p[1]["reach-mtd"], p[1]["call-edge"]), datas)
    with open(os.path.join(path, "round-%d.csv" % round), "w") as f:
        f.write(header + "\n" + "\n".join(lines))

def readINSData(benchResPath):
    txt = Path(benchResPath).read_text()
    txt = txt[txt.find("Runtime metrics") : ]
    lines = txt.split("\n")
    res = {}
    for l in lines:
        for k, v in datas.items():
            if l.startswith(v):
                res[k] = l.split()[-1]
        if len(res) == 5:
            break
    return res

def processINSData(round):
    resultPath = "./sdiff/insensitive"
    path = "./sdiff/zipper"
    Path(resultPath).mkdir(parents=True, exist_ok=True)
    header = "Benchmark;time;fail-cast;poly-call;reach-mtd;call-edge"
    benchs = tests.keys()
    datas = map(lambda bench: (bench, readINSData(os.path.join(path, bench))), benchs)
    line = "%s;%s;%s;%s;%s;%s"
    lines = map(lambda p: line % (p[0], p[1]["time"], p[1]["fail-cast"], p[1]["poly-call"], p[1]["reach-mtd"], p[1]["call-edge"]), datas)
    with open(os.path.join(resultPath, "round-%d.csv" % round), "w") as f:
        f.write(header + "\n" + "\n".join(lines))

def main():
    for i in range(1):
        run2obj()
        processData("./sdiff/2-obj", i)
        runZipper()
        processData("./sdiff/zipper", i)
        processINSData(i)

if __name__ == "__main__":
    main()