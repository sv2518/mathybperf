#!/bin/sh

# turn off threading
export OMP_NUM_THREADS=1
source /Users/sv2518/firedrakeinstalls/firedrake/bin/activate
cd /Users/sv2518/firedrakeexamples/mathybperf/mathybperf/performance

# mode of the script, options are:
# do we want to generate a tex from this?
# do we want to generate new results?
ARG0="$1"
ARG1="$2"
ARG2="$3"
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

# setup (MAKE YOUR CHANGES HERE
current_case="$ARG0"
my_dir="$(dirname "$0")"
echo $my_dir
pwd
. $my_dir/setups/$current_case.sh
echo $CASE

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

# Save the links to the svgs in a file for easy access from the report
# but a note that explain how to fetch this automatically to a local repo
# FIXME links don't work because I changed the repo structure
WEBPAGE="https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/"$BASEFLAMENAME
WEBPAGE1="\url{"$WEBPAGE$BASEP"_warm_up_flame.svg}"
WEBPAGE2="\url{"$WEBPAGE$BASEP"_warmed_up_flame.svg}"
WEBPAGE3="\url{"$WEBPAGE$PERFORMP"warm_up_flame.svg}"
WEBPAGE4="\url{"$WEBPAGE$PERFORMP"warmed_up_flame.svg}"
NOTE="\nEasier way is to run curl -OL "$WEBPAGE"curlthesvgs.sh\n and sh ./curlthesvgs.sh."
touch $BASEFLAMENAME"linkstosvgs.tex"
echo $WEBPAGE1"\n"$WEBPAGE2"\n"$WEBPAGE3"\n"$WEBPAGE4"\n"$NOTE > $BASEFLAMENAME"linkstosvgs.tex"

# Generate and publish script to fetch the svg files
CWEBPAGE1="curl "$WEBPAGE$BASEP"_warm_up_flame.svg>"$BASEFLAMENAME$BASEP"_warm_up_flame.svg"
CWEBPAGE2="curl "$WEBPAGE$BASEP"_warmed_up_flame.svg>"$BASEFLAMENAME$BASEP"_warmed_up_flame.svg"
CWEBPAGE3="curl "$WEBPAGE$PERFORMP"_warm_up_flame.svg>"$BASEFLAMENAME$PERFORMP"_warm_up_flame.svg"
CWEBPAGE4="curl "$WEBPAGE$PERFORMP"_warmed_up_flame.svg>"$BASEFLAMENAME$PERFORMP"_warmed_up_flame.svg"
touch $BASEFLAMENAME"curlthesvgs.sh"
echo "#!/bin/sh\nmkdir -p ./svgs/"$BASEFLAMENAME"\ncd svgs\n"$CWEBPAGE1"\n"$CWEBPAGE2"\n"$CWEBPAGE3"\n"$CWEBPAGE4"\n" > $BASEFLAMENAME"curlthesvgs.sh"
git add $BASEFLAMENAME"curlthesvgs.sh"
git commit -m "New script to fetch flamegraphs was generated."
CURRENT_BRANCH=$(git branch --show-current)
git push origin $CURRENT_BRANCH

# Keep track of the sh file
SCRIPT="run_profiler.sh"
cp $SCRIPT "$BASENAME"$SCRIPT

# Move results over into report directory and push online
PATH_TO_REPORT='../../../mathybperf_report/61dc091dbf10034613ed0daa/'
find ./results -type f | grep -i setup.txt$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./results -type f | grep -i log.txt$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./flames -type f | grep -i linkstosvgs.tex$ | xargs -I{} ditto {} $PATH_TO_REPORT/{}
find ./results -type f | grep -i setup.txt$ | xargs -I{} git -C $PATH_TO_REPORT add {} 
find ./results -type f | grep -i log.txt$ | xargs -I{} git -C $PATH_TO_REPORT add {} 
find ./flames -type f | grep -i linkstosvgs.tex$ | xargs -I{} git -C $PATH_TO_REPORT add {}
git -C $PATH_TO_REPORT commit -m "New results"
git -C $PATH_TO_REPORT pull origin master
git -C $PATH_TO_REPORT push origin master