#!/usr/bin/env python

import argparse
import datetime
import math
import os
import random
import shutil
import time

import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "--loops", nargs="+", type=int,
    help="""Number of loops to run the coarsen algorithm.
    Given a single number N, results will be named from bench-0 to bench-{N-1}
    Given numbers N and M, results will be named from bench-N to bench-{M-1}""",
)
parser.add_argument(
    "benchmark", type=str,
    help="The name of benchmark to carry out the coarsen algorithm. (For example, 2006-xalan or bach-pmd.)"
)
parser.add_argument(
    "--frac", type=float,
    help="Fraction of the termination condition of Active Coarsening."
)
parser.add_argument(
    "--fast", action="store_true",
    help="Whether to add the speed restriction."
)
parser.add_argument(
    "--keep", choices=["necessary", "small"], required=True,
    help="""Types of files to keep.
    necessary: keeps only necessary metrics and runtime files.
    small: remove large files like points-to facts."""
)
parser.add_argument(
    "--metrics-lines", nargs="+", type=int, default=[18, 21, 26, 36],
    help="""Line numbers of metrics that should be kept during coarsening. Default values correspond to:
    call graph edges (INS) &
    reachable methods(INS) &
    polymorphic virtual call sites &
    reachable casts that may fail."""
)
parser.add_argument(
    "--souffle-jobs", type=int, default=16,
    help="The number of jobs for souffle to launch.",
)
parser.add_argument(
    "--jre", type=int, default=6, choices=range(6, 9),
    help="The version of JRE",
)
parser.add_argument(
    "--last", type=int, default=None,
    help="(Used if the algorithm terminated abnormally) Continue from the given iteration",
)
parser.add_argument(
    "--MCMC", action="store_true",
    help="Whether to run MCMC."
)
parser.add_argument(
    "--mcmc-k", type=float,
    help="A hyperparameter k of MCMC"
)
parser.add_argument(
    "--mcmc-a", type=float, default=10,
    help="A hyperparameter a of MCMC"
)


class ScanCoarsen:
    def __init__(self, COARSEN_DIR, reachable):
        self.COARSEN_DIR = COARSEN_DIR
        self.reachable = reachable
        self.flags = [True] * len(reachable)
        self.it = tqdm.trange(len(reachable)).__iter__()
    def generate_abs(self, i):
        self.flags[i] = False
        abs_path = os.path.join(self.COARSEN_DIR, str(i), f"database/ZipperPrecisionCriticalMethod.facts")
        with open(abs_path, "w") as f:
            for flag, method in zip(self.flags, self.reachable):
                if flag:
                    print(method, file=f, end="")
        return abs_path, sum(self.flags)
    def update(self, accept, i):
        self.flags[i] = not accept
        return sum(self.flags)
    def working(self):
        try:
            self.it.__next__()
            return True
        except StopIteration:
            return False

class ActiveCoarsen:
    lr = 0.1

    def __init__(self, COARSEN_DIR, reachable):
        self.COARSEN_DIR = COARSEN_DIR
        self.reachable = reachable

        self.s_estimate = round(len(reachable) * frac)
        print(f"s_estimate = {frac} * |reachable|")
        self.theta = -math.log(math.exp(1 / self.s_estimate) - 1)
        alpha = 1 / (1 + math.exp(-self.theta))
        self.stuck_count = 0
        print(f"{self.theta = :.5f}")
        print(f"{alpha = :.5f}")
        print(len(reachable), "parameters")
    def generate_abs(self, i):
        abs_path = os.path.join(self.COARSEN_DIR, str(i), f"database/ZipperPrecisionCriticalMethod.facts")
        alpha = 1 / (1 + math.exp(-self.theta))
        self.new_param = [
            method
            for method in self.reachable
            if random.random() < alpha
        ]
        with open(abs_path, "w") as f:
            print("".join(self.new_param), end="", file=f)
        return abs_path, len(self.new_param)
    def update(self, accept, i):
        if accept:
            self.stuck_count = 0
            self.reachable = self.new_param
        self.theta -= ActiveCoarsen.lr * (flag - 1 / math.e)
        alpha = 1 / (1 + math.exp(-self.theta))
        print(f"{i:4}-th iteration. {self.theta = :.5f} {alpha = :.5f}")
        return len(self.reachable)
    def working(self):
        return len(self.reachable) > self.s_estimate

class MCMCCoarsen:
    def __init__(self, COARSEN_DIR, reachable, pts_k, param_a):
        self.COARSEN_DIR = COARSEN_DIR
        self.reachable = reachable
        self.old_param = reachable
        self.i = 0
        self.old_pts_cnt = 1e8
        self.pts_k = pts_k
        self.param_a = param_a
        # self.s_estimate = round(sum(map(len, parameters)) * frac)
        # print(f"s_estimate = {frac} * |reachable|")
        # self.theta = -math.log(math.exp(1 / self.s_estimate) - 1)
        # alpha = 1 / (1 + math.exp(-self.theta))
        print(len(reachable), "parameters")

    def generate_abs(self, i):
        abs_path = os.path.join(self.COARSEN_DIR, str(i), f"database/ZipperPrecisionCriticalMethod.facts")
        alpha = 2e-4
        if i == 0:
            print(f"{alpha = :.0e} {self.pts_k = :.0e} {self.param_a = :g}")
        self.new_param = [
            method
            for method in self.reachable
            if (
                (random.random() < (1 - alpha))
                if method in self.old_param else
                (random.random() < alpha / self.param_a)
            )
        ]
        with open(abs_path, "w") as f:
            print("".join(self.new_param), end="", file=f)
        return abs_path, len(self.new_param)
    def update(self, accept, new_pts_cnt, i):
        self.i = i
        if self.old_pts_cnt <= new_pts_cnt:
            print(
                math.log(i + 1) * (self.old_pts_cnt - new_pts_cnt) * self.pts_k,
                math.exp(math.log(i + 1) * (self.old_pts_cnt - new_pts_cnt) * self.pts_k),
            )
        if accept and (
            (self.old_pts_cnt > new_pts_cnt) or
            random.random() < math.exp(math.log(i + 1) * (self.old_pts_cnt - new_pts_cnt) * self.pts_k)
        ):
            self.old_param = self.new_param
            self.old_pts_cnt = new_pts_cnt
        return len(self.old_param)
    def working(self):
        return self.i < 1e5

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    benchmark_full = args.benchmark
    metrics_lines = args.metrics_lines
    loops = args.loops
    assert len(loops) <= 2, "--loops only accept 1 or 2 arguments!"
    assert not (args.fast and args.MCMC)
    keep = args.keep
    jobs = args.souffle_jobs
    fast = args.fast

    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64/"
    os.chdir("/home/zyyan/repos/doop-mirror")
    BASE_DATABASE = f"/data/zyyan/doop_out_{args.jre}/"
    if args.fast or args.MCMC:
        frac = 0.25
        COARSEN_OUT = "/data/zyyan/ins_level/theoretical/fast-active-coarsen"
    else:
        frac = 0.15
        COARSEN_OUT = "/data/zyyan/ins_level/theoretical/active-coarsen"
    if args.jre != 6:
        COARSEN_OUT = COARSEN_OUT.replace("theoretical", f"theoretical-{args.jre}")
    reachable_data = "Reachable.csv"
    metrics_data = "Stats_Metrics.csv"

    necessary = set([
        "Stats_Metrics.csv",
        "Stats_Runtime.csv",
        "ZipperPrecisionCriticalMethod.facts",
    ])
    print(f"Running speed-oriented active coarsen on {benchmark_full} for {loops} loops")
    prefix, benchmark = benchmark_full.split("-")
    FULLY_SEN_DB = os.path.join(BASE_DATABASE + f"2-object-sensitive+heap-{benchmark_full}", "database")
    for idx in range(*loops):
        print(f"Executing active coarsen on benchmark {benchmark_full}")
        with open(os.path.join(FULLY_SEN_DB, reachable_data)) as f:
            reachable = f.readlines()
        with open(os.path.join(FULLY_SEN_DB, metrics_data)) as f:
            baseline_stat = f.read().splitlines()

        sen_pts_to_cnt = 1e11
        for Algorithm, DOOP_OUT in (phases := [
            (MCMCCoarsen, f"{COARSEN_OUT}/{benchmark_full}-{idx}/MCMC"),
        ] if args.MCMC else [
            (ActiveCoarsen, f"{COARSEN_OUT}/{benchmark_full}-{idx}/active"),
            (ScanCoarsen,   f"{COARSEN_OUT}/{benchmark_full}-{idx}/scan"),
        ]):
            if args.MCMC:
                algorithm = Algorithm(DOOP_OUT, reachable, args.mcmc_k, args.mcmc_a)
            else:
                algorithm = Algorithm(DOOP_OUT, reachable)
            if args.last != None:
                with open(f"{COARSEN_OUT}/{benchmark_full}-{idx}/active/{args.last}/database/ZipperPrecisionCriticalMethod.facts") as f:
                    reachable = f.readlines()
                algorithm.reachable = reachable
                i = args.last
                args.last = None
            else:
                i = -1
            os.makedirs(DOOP_OUT, exist_ok=True)
            while algorithm.working():
                i += 1
                os.makedirs(f"{DOOP_OUT}/{i}/database", exist_ok=True)
                abs_path, abs_cnt = algorithm.generate_abs(i)
                trial_id = str(i)
                shutil.copy(
                    abs_path,
                    f"{DOOP_OUT}/run/database/ZipperPrecisionCriticalMethod.facts",
                )
                cmdline = " ".join([
                    f"{DOOP_OUT}/run/analysis-binary",
                    f"-F {DOOP_OUT}/run/database/",
                    f"-D {DOOP_OUT}/{i}/database",
                    f"2> {DOOP_OUT}/{i}.log",
                ])
                # cmdline = " ".join([
                #     f"{DOOP_OUT=} ./doop -a 2-object-sensitive+heap -i ../doop-benchmarks/dacapo-{suffix}/{benchmark}.jar",
                #     "--cs-library --no-merge-library-objects --Xno-ssa",
                #     "--cache",
                #     "--no-standard-exports",
                #     f" --Xzipper {abs_path}",
                #     f" -id {trial_id} --souffle-jobs {jobs} --platform java_6",
                #     "--dacapo" if suffix != "bach" else "--dacapo-bach",
                #     f"> {DOOP_OUT}/{i}.log",
                # ])
                print(f"Trying with {abs_cnt} parameters...")
                t1 = time.time()
                os.system(cmdline)
                t2 = time.time()
                ANALYSIS_DB = os.path.join(DOOP_OUT, trial_id, "database")
                while not os.path.exists(os.path.join(ANALYSIS_DB, metrics_data)):
                    print(f"{i:4}-th iteration failed, rerunning...")
                    t1 = time.time()
                    os.system(cmdline.replace(">", ">>"))
                    t2 = time.time()
                with open(f"{DOOP_OUT}/{i}/database/Stats_Runtime.csv", "w") as f:
                    print(f"""
fact generation time (sec)\tN/A
analysis compilation time (sec)\tN/A
analysis execution time (sec)\t{t2 - t1}
disk footprint (KB)\tN/A""".strip(), file=f)
                if keep == "necessary":
                    # Remove all unnecessary outputs
                    for file in os.listdir(os.path.join(ANALYSIS_DB)):
                        if file not in necessary:
                            os.remove(os.path.join(ANALYSIS_DB, file))
                    # os.remove(abs_path)
                else:
                    # Remove large outputs only
                    for large in [
                        "Var-DeclaringMethod.facts",
                        "Stats_Simple_JavaUtilVarPointsTo.csv",
                    ]:
                        large_full_path = os.path.join(ANALYSIS_DB, large)
                        if os.path.exists(large_full_path):
                            os.remove(large_full_path)
                        else:
                            print(f"[IMPORTANT] {large} not found after the analyzation.")
                with open(os.path.join(ANALYSIS_DB, metrics_data)) as f:
                    coarse_stat = f.read().splitlines()
                    flag = True
                    for lineno in metrics_lines:
                        line1 = coarse_stat[lineno]
                        line2 = baseline_stat[lineno]
                        if line1 != line2:
                            print(line1 == line2)
                            print(line1, line2)
                            flag = False
                    if fast:
                        if flag:
                            pts_to = int(coarse_stat[1].strip().split("\t")[-1])
                            if pts_to > sen_pts_to_cnt:
                                tqdm.tqdm.write(f"{sen_pts_to_cnt:^12} => {pts_to:^12}")
                                flag = False
                            else:
                                sen_pts_to_cnt = pts_to
                        print(f"Number of sensitive points-to facts {sen_pts_to_cnt}")
                    if args.MCMC:
                        pts_to = int(coarse_stat[1].strip().split("\t")[-1])
                        if flag:
                            tqdm.tqdm.write(f"{algorithm.old_pts_cnt:^12} => {pts_to:^12}")
                        print(algorithm.update(flag, pts_to, i), "parameters kept.")
                    else:
                        print(algorithm.update(flag, i), "parameters kept.")
                    if flag:
                        last_precise = i
            reachable = algorithm.reachable
            print(f"{type(algorithm)} Finished. {len(reachable)} parameters left.")
        os.system(" ".join([
            "cp -r",
            f"{COARSEN_OUT}/{benchmark_full}-{idx}/scan/{last_precise}",
            f"{COARSEN_OUT}/{benchmark_full}-{idx}/result"
        ]))
