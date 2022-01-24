import pytest
import subprocess
import glob
import os
import gc


def setup_names():
    setup_list = glob.glob("./mathybperf/performance/setups/*.sh")
    setup_names = [s[s.rfind("/")+1:s.rfind(".")] for s in setup_list]
    return setup_names

base_path = './mathybperf/performance/verification/results/mixed_poisson/pplus1pow3/'
setups = setup_names()

def run_profiler(name):
    gc.collect()
    gc.collect()
    gc.collect()
    proc = subprocess.run(["cd ./mathybperf/performance ; /bin/bash ./run_profiler.sh "+name+" --verification"],
                          shell=True,
                          close_fds=True,
                          check=True)
    if proc.returncode!=0:
        error_file = base_path+name+'/verification.err'
        print("Current directory is: ", os.system('pwd'))
        with open(error_file, 'w') as file:
            error_message = file.read()
    else:
        error_message="empty"
    assert proc.returncode==0, "Case "+name+" failed. Error message in file "+str(error_file)+": \n"+error_message


@pytest.mark.parametrize("name", setups)
def test_setups_mixed_poisson(name):
    run_profiler(name)
