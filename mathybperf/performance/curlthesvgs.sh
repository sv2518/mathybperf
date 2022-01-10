#!/bin/sh
mkdir -p ./svgs/
cd svgs
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/jacks_baseline_params_warm_up_flame.svg>jacks_baseline_params_warm_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/jacks_baseline_params_warmed_up_flame.svg>jacks_baseline_params_warmed_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/perform_params_warm_up_flame.svg>perform_params_warm_up_flame.svg
curl https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/perform_params_warmed_up_flame.svg>perform_params_warmed_up_flame.svg

