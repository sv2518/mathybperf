import pytest
import subprocess
import glob


def setup_names():
    setup_list = glob.glob("./mathybperf/performance/setups/*.sh")
    setup_names = [s[s.rfind("/")+1:s.rfind(".")] for s in setup_list]
    return setup_names

base_path = './mathybperf/performance/verification/results/mixed_poisson/pplus1pow3/'
setups = setup_names()

def run_profiler(name):
    proc = subprocess.run(["cd ./mathybperf/performance ; sh ./run_profiler.sh "+name+" --verification"], shell=True)
    if proc.returncode!=0:
        error_file = base_path+name+'/verification.err'
        error_message = open(error_file, "r").read()
    else:
        error_message="empty"
    assert proc.returncode==0, "Case "+name+" failed. Error message in file "+str(error_file)+": \n"+error_message


@pytest.mark.parametrize("name", setups)
def test_setups_mixed_poisson(name):
    run_profiler(name)
