#!/bin/sh
mkdir -p ./svgs/flames/mixed_poisson/pplus1pow3/trafo_none/case1/
 cd svgs
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/flames/mixed_poisson/pplus1pow3/trafo_none/case1/baseline_params_warm_up_flame.svg>flames/mixed_poisson/pplus1pow3/trafo_none/case1/baseline_params_warm_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/flames/mixed_poisson/pplus1pow3/trafo_none/case1/baseline_params_warmed_up_flame.svg>flames/mixed_poisson/pplus1pow3/trafo_none/case1/baseline_params_warmed_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/flames/mixed_poisson/pplus1pow3/trafo_none/case1/perform_params_warm_up_flame.svg>flames/mixed_poisson/pplus1pow3/trafo_none/case1/perform_params_warm_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/flames/mixed_poisson/pplus1pow3/trafo_none/case1/perform_params_warmed_up_flame.svg>flames/mixed_poisson/pplus1pow3/trafo_none/case1/perform_params_warmed_up_flame.svg

