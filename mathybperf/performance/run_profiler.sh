#!/bin/sh

# turn off threading
export OMP_NUM_THREADS=1

# mode of the script, options are:
# do we want to generate a tex from this?
# do we want to generate new results?
ARG1="$1"
ARG2="$2"
if [[ "$ARG1" == "--nores" || "$ARG2" == "--nores" ]]
then
    DORES=false
else
    DORES=true
fi
if [[ "$ARG1" == "--tex" || "$ARG2" == "--tex" ]]
then
    DOTEX=true
else
    DOTEX=false
fi

# setup
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

# setup output folder name
# first choose a case name
CASE='/case1/'
FOLDER='results/mixed_poisson/'
FOLDER+='pplus1pow3/'  # penalty set permanently to this
TRAFOTYPE='trafo_'$TRAFO
NAME=$FOLDER$TRAFOTYPE$CASE
FLAMENAME='flames/mixed_poisson/pplus1pow3/'$TRAFOTYPE$CASE
mkdir -p $NAME
mkdir -p $FLAMENAME

# file name is parameter set name
for D in $DEFORM
do
    for S in $SCALING
    do
        for P in $ORDERS
        do
            for C in $CELLSPD
            do
                if ! $FLAME
                then 
                    FLARG=''
                fi

                # run base case
                PARAMS=$BASEP
                NNAME=$NAME$PARAMS
                FNAME=$FLAMENAME$PARAMS
                firedrake-clean
                NNAME+='_warm_up'
                FNAME+='_warm_up'
                if $FLAME
                then
                    FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" --clean
                if $FLAME
                then
                ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.html"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                fi

                NNAME=$NAME$PARAMS
                FNAME=$FLAMENAME$PARAMS
                NNAME+='_warmed_up'
                FNAME+='_warmed_up'
                if $FLAME
                then
                    FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}"
                if $FLAME
                then
                ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.html"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                fi

                # run perf case
                PARAMS=$PERFORMP
                NNAME=$NAME$PARAMS
                FNAME=$FLAMENAME$PARAMS
                firedrake-clean
                NNAME+='_warm_up'
                FNAME+='_warm_up'
                if $FLAME
                then
                    FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}" --clean
                if $FLAME
                then
                ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.html"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                fi

                NNAME=$NAME$PARAMS
                FNAME=$FLAMENAME$PARAMS
                NNAME+='_warmed_up'
                FNAME+='_warmed_up'
                if $FLAME
                then
                    FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                fi
                python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $FLARG --add_to_quad_degree "${ATQD[@]}"
                if $FLAME
                then
                ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.html"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                fi
            done
        done
    done
done

# Make new flamegraphs online accessible
git add $FLAMENAME*"_flame.html"
git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
CURRENT_BRANCH=$(git branch --show-current)
git push origin $CURRENT_BRANCH