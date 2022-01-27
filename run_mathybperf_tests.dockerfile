FROM firedrakeproject/firedrake-vanilla:latest
CMD . ./firedrake/bin/activate \
&& ls firedrake\
&& firedrake-status \
&& firedrake-update \
&& cat ./firedrake/firedrake-update.log \
&& git -C ./firedrake/src/firedrake/ checkout sv/local-matfree-pr \
&& git -C ./firedrake/src/tsfc/ checkout sv/local-matfree-pr \
&& git -C ./firedrake/src/PyOP2/ checkout sv/local-matfree-pr \
&& python -m pip install pandas \
&& python -m pip install flake8 pylint \
&& git clone https://github.com/sv2518/mathybperf.git \
&& cd mathybperf \
&& python -m pip install -e . \
&& python $(which firedrake-clean) \
&& python -m pytest -n auto -v mathybperf/tests
# && sudo apt-get update \
# && sudo apt-get install valgrind -y\
# && valgrind -m pytest -v mathybperf/tests
