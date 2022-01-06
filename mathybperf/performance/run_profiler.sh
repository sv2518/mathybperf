#!/bin/sh

# turn off threading
export OMP_NUM_THREADS=1
ORDERS=(0)
LEVELS=2
SCALING=(1)
DEFORM=(0)
TRAFO='none' # 'affine'
ATQD=(0 0)
CELLSPD=(3)
QUADS=true
FLAME=true
PERFORMP='perform_params'
BASEP='baseline_params'

echo $ORDERS

# setup output folder name
# first choose a case name
CASE='/case1/'
FOLDER='results/mixed_poisson/'
FOLDER+='pplus1pow3/'  # penalty set permanently to this
TRAFOTYPE='trafo_'$TRAFO
NAME=$FOLDER$TRAFOTYPE$CASE
mkdir -p $NAME

# file name is parameter set name
for D in $DEFORM
do
    for S in $SCALING
    do
        for P in $ORDERS
        do
            for C in $CELLSPD
            do
                if not $FLAME
                then 
                    FLARG=''
                fi

                # run base case
                PARAMS=$BASEP
                NNAME=$NAME$PARAMS
                firedrake-clean
                NNAME+='_warm_up'
                if $FLAME
                then
                    FLARG='-log_view :flame_'$NNAME'.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" --clean
                
                NNAME+='_warmed_up'
                if $FLAME
                then
                    FLARG='-log_view :flame_'$NNAME'.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" 


                # run perf case
                PARAMS=$PERFORMP
                NNAME=$NAME$PARAMS
                firedrake-clean
                NNAME+='_warm_up'
                if $FLAME
                then
                    FLARG='-log_view :flame_'$NNAME'.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" --clean
                
                NNAME+='_warmed_up'
                if $FLAME
                then
                    FLARG='-log_view :flame_'$NNAME'.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" 
            done
        done
    done
done