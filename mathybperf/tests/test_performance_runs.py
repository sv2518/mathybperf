import pytest
import subprocess
import glob
import os
import gc
import resource
import re


def setup_names():
    setup_list = glob.glob("./mathybperf/performance/setups/*.sh")
    setup_names = [s[s.rfind("/")+1:s.rfind(".")] for s in setup_list]
    return setup_names


def setup_degrees(setups):
    test_setup = []
    for s in setups:
        with open("./mathybperf/performance/setups/"+s+".sh", 'r') as myfile:
            content = myfile.read()
            match = re.search("ORDERS=(.*)",content).group(0)
            degrees = list(int(d) for d in filter(str.isdigit, match))
            for d in degrees:
                test_setup += [(s, d)]
    return test_setup


base_path = './mathybperf/performance/verification/results/mixed_poisson/pplus1pow3/'
setups = setup_names()
setups = setup_degrees(setups)

MAX_AS = 4000 * 1024 * 1024  # 4 GB
def set_limits():
    # The maximum area (in bytes) of address space which may be taken by the process.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_AS, resource.RLIM_INFINITY))
    # resource.setrlimit(resource.RLIMIT_SWAP, (MAX_AS, resource.RLIM_INFINITY))
    resource.setrlimit(resource.RLIMIT_DATA, (MAX_AS, resource.RLIM_INFINITY))

def run_profiler(name, degree):
    gc.collect()
    gc.collect()
    gc.collect()
    proc = subprocess.run(["cd ./mathybperf/performance ; /bin/bash ./run_profiler.sh "+name+" "+str(degree)+" --verification"],
                           shell=True,
                           close_fds=True)
    if proc.returncode!=0:
        # error_file = base_path+name+'/verification.err'
        # print("Current directory is: ", os.system('pwd'))
        # with open(error_file, 'r') as myfile:
        #     error_message = myfile.read()
        log_files = glob.glob(base_path+name+'/*/*/*/*log.txt')
        log_file_curr = sorted(log_files, key=os.path.getmtime)[-1]
        log_file_old = sorted(log_files, key=os.path.getmtime)[-2]
        print("\n\nThe current log file contains:\n")
        with open(log_file_curr, 'r') as myfile:
            print(myfile.read())
        print("\n\nThe previous log file contains:\n")
        with open(log_file_old, 'r') as myfile:
            print(myfile.read())
    else:
        error_message="empty"
    assert proc.returncode==0, "Case "+name+" failed. Error message in file "+str(error_file)+": \n"+error_message


@pytest.mark.parametrize("name, degree", setups)
def test_setups_mixed_poisson(name, degree):
    run_profiler(name, degree)
