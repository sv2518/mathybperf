#!/bin/sh

# turn off threading
export OMP_NUM_THREADS=1
source /Users/sv2518/firedrakeinstalls/firedrake/bin/activate
cd /Users/sv2518/firedrakeexamples/mathybperf/mathybperf/performance

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
ORDERS=(0 1 2)
LEVELS=2
SCALING=(1)
DEFORM=(0)
TRAFO='none' # 'affine'
ATQD=(0 0)
CELLSPD=(3)
QUADS=true
FLAME=true
PERFORMP='perform_params'
BASEP='jacks_baseline_params'
SOLTYPE='quadratic'
PROJECTEXACTSOL=false

# setup output folder name
# first choose a case name
CASE='/case1/'
FOLDER='results/mixed_poisson/'
FOLDER+='pplus1pow3/'  # penalty set permanently to this
TRAFOTYPE='trafo_'$TRAFO
BASENAME=$FOLDER$TRAFOTYPE$CASE
FLAMEBASENAME='flames/mixed_poisson/pplus1pow3/'$TRAFOTYPE$CASE

if $DORES
then
    # file name is parameter set name
    for D in "${DEFORM[@]}"
    do
        for S in "${SCALING[@]}"
        do
            for P in "${ORDERS[@]}"
            do
                for C in "${CELLSPD[@]}"
                do
                    FLAMENAME=$FLAMEBASENAME"order_"$P"/cells_"$C"/"
                    NAME=$BASENAME"order_"$P"/cells_"$C"/"
                    mkdir -p $FLAMENAME
                    mkdir -p $NAME
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
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --clean --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi

                    NNAME=$NAME$PARAMS
                    FNAME=$FLAMENAME$PARAMS
                    NNAME+='_warmed_up'
                    FNAME+='_warmed_up'
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
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
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --clean --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi

                    NNAME=$NAME$PARAMS
                    FNAME=$FLAMENAME$PARAMS
                    NNAME+='_warmed_up'
                    FNAME+='_warmed_up'
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi
                done
            done
        done
    done
    # Make new flamegraphs online accessible
    git add $FLAMENAME*"_flame.svg"
    git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
    CURRENT_BRANCH=$(git branch --show-current)
    git push origin $CURRENT_BRANCH
fi

mkdir -p "../report/"$FLAMENAME
WEBPAGE="https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/"$FLAMENAME
WEBPAGE1=$WEBPAGE$BASEP"_warm_up_flame.svg"
WEBPAGE2=$WEBPAGE$BASEP"_warmed_up_flame.svg"
WEBPAGE3=$WEBPAGE$PERFORMP"warm_up_flame.svg"
WEBPAGE4=$WEBPAGE$PERFORMP"warmed_up_flame.svg"
NOTE="\nEasier way is to run curl -OL "$WEBPAGE"curlthesvgs.sh\n and sh ./curlthesvgs.sh."
touch "../report/"$FLAMENAME"linkstosvgs.txt"
echo $WEBPAGE1"\n"$WEBPAGE2"\n"$WEBPAGE3"\n"$WEBPAGE4"\n"$NOTE > "../report/"$FLAMENAME"linkstosvgs.txt"

CWEBPAGE1="curl "$WEBPAGE$BASEP"_warm_up_flame.svg>"$FLAMENAME$BASEP"_warm_up_flame.svg"
CWEBPAGE2="curl "$WEBPAGE$BASEP"_warmed_up_flame.svg>"$FLAMENAME$BASEP"_warmed_up_flame.svg"
CWEBPAGE3="curl "$WEBPAGE$PERFORMP"_warm_up_flame.svg>"$FLAMENAME$PERFORMP"_warm_up_flame.svg"
CWEBPAGE4="curl "$WEBPAGE$PERFORMP"_warmed_up_flame.svg>"$FLAMENAME$PERFORMP"_warmed_up_flame.svg"
touch $FLAMENAME"curlthesvgs.sh"
echo "#!/bin/sh\nmkdir -p ./svgs/"$FLAMENAME"\ncd svgs\n"$CWEBPAGE1"\n"$CWEBPAGE2"\n"$CWEBPAGE3"\n"$CWEBPAGE4"\n" > $FLAMENAME"curlthesvgs.sh"
git add $FLAMENAME"curlthesvgs.sh"
git commit -m "New script to fetch flamegraphs was generated."
CURRENT_BRANCH=$(git branch --show-current)
git push origin $CURRENT_BRANCH

# Move results over into report directory and push online
PATH_TO_REPORT='../../../mathybperf_report/61dc091dbf10034613ed0daa/'
find ./results -type f | grep -i setup.txt$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./results -type f | grep -i log.txt$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./flames -type f | grep -i linkstosvgs.txt$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./results -type f | grep -i setup.txt$ | xargs -I{} git -C $PATH_TO_REPORT add {} 
find ./results -type f | grep -i log.txt$ | xargs -I{} git -C $PATH_TO_REPORT add {} 
find ./flames -type f | grep -i linkstosvgs.txt$ | xargs -I{} git -C $PATH_TO_REPORT add {}
git -C $PATH_TO_REPORT commit -m "New results"
git -C $PATH_TO_REPORT pull origin master
git -C $PATH_TO_REPORT push origin master