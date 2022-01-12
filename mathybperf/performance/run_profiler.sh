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
FOLDER='results/mixed_poisson/'
FOLDER+='pplus1pow3/'  # penalty set permanently to this
TRAFOTYPE='trafo_'$TRAFO
BASENAME=$FOLDER$TRAFOTYPE$CASE
FLAMEBASENAME='flames/mixed_poisson/pplus1pow3/'$TRAFOTYPE$CASE
LINKS=""
CURLS=""
WEBPAGE="https://raw.githubusercontent.com/sv2518/mathybperf/main/mathybperf/performance/"

alias urlencode='python3 -c "import sys, urllib.parse as ul; print(ul.quote_plus(sys.argv[1]))"'
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
                    CURLS=$CURLS"mkdir -p "$FLAMENAME"\n"
                    LINKS=$LINKS'\n\nLinks for flames of RT$_{p+1}$-DG$_{p}$ with $p='$P'$ and base mesh $'$C'\\times'$C'\\times'$C'$ refined on '$LEVELS' levels\\\\ \n\n'
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
                    LINKS=$LINKS"Baseline warmup run\n"
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --clean --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi
                    # Make new flamegraphs online accessible
                    git add $FLAMENAME*"_flame.svg"
                    git add -f $FLAMENAME*"_flame.txt"
                    git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
                    git push origin $CURRENT_BRANCH
                    # Generate data for links
                    long_url="https://www.speedscope.app/#profileURL="$WEBPAGE$FNAME"_flame.txt"
                    encode_long_url=$(urlencode $long_url)
                    short_url=$(curl -s "http://tinyurl.com/api-create.php?url=${encode_long_url}")
                    LINKS=$LINKS"\url{$short_url}\n\n"
                    CURLS=$CURLS"curl "$WEBPAGE$FNAME"_flame.svg>"$FNAME"_flame.svg\n"

                    NNAME=$NAME$PARAMS
                    FNAME=$FLAMENAME$PARAMS
                    NNAME+='_warmed_up'
                    FNAME+='_warmed_up'
                    LINKS=$LINKS"Baseline warmed up run\n"
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi
                    # Make new flamegraphs online accessible
                    git add $FLAMENAME*"_flame.svg"
                    git add -f $FLAMENAME*"_flame.txt"
                    git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
                    git push origin $CURRENT_BRANCH
                    # Generate data for links
                    long_url="https://www.speedscope.app/#profileURL="$WEBPAGE$FNAME"_flame.txt"
                    encode_long_url=$(urlencode $long_url)
                    short_url=$(curl -s "http://tinyurl.com/api-create.php?url=${encode_long_url}")
                    LINKS=$LINKS"\url{$short_url}\n\n"
                    CURLS=$CURLS"curl "$WEBPAGE$FNAME"_flame.svg>"$FNAME"_flame.svg\n"

                    # run perf case
                    PARAMS=$PERFORMP
                    NNAME=$NAME$PARAMS
                    FNAME=$FLAMENAME$PARAMS
                    firedrake-clean
                    NNAME+='_warm_up'
                    FNAME+='_warm_up'
                    LINKS=$LINKS"Performance warmup run\n"
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --clean --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi
                    # Make new flamegraphs online accessible
                    git add $FLAMENAME*"_flame.svg"
                    git add -f $FLAMENAME*"_flame.txt"
                    git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
                    git push origin $CURRENT_BRANCH
                    # Generate data for links
                    long_url="https://www.speedscope.app/#profileURL="$WEBPAGE$FNAME"_flame.txt"
                    encode_long_url=$(urlencode $long_url)
                    short_url=$(curl -s "http://tinyurl.com/api-create.php?url=${encode_long_url}")
                    LINKS=$LINKS"\url{$short_url}\n\n"
                    CURLS=$CURLS"curl "$WEBPAGE$FNAME"_flame.svg>"$FNAME"_flame.svg\n"

                    NNAME=$NAME$PARAMS
                    FNAME=$FLAMENAME$PARAMS
                    NNAME+='_warmed_up'
                    FNAME+='_warmed_up'
                    LINKS=$LINKS"Performance warmed up run\n"
                    if $FLAME
                    then
                        FLARG='-log_view :'$FNAME'_flame.txt:ascii_flamegraph'
                    fi
                    python3 run_profiler.py $NNAME $PARAMS $P $LEVELS $QUADS $S $D $TRAFO $C $SOLTYPE $FLARG --add_to_quad_degree "${ATQD[@]}" --projectexactsol $PROJECTEXACTSOL > $NNAME"_log.txt"
                    if $FLAME
                    then
                    ../../../FlameGraph/flamegraph.pl $FNAME"_flame.txt" > $FNAME"_flame.svg"  --inverted --title "Firedrake example" --countname us --fontsize 13 --colors "eyefriendly"
                    fi
                    # Make new flamegraphs online accessible
                    git add $FLAMENAME*"_flame.svg"
                    git add -f $FLAMENAME*"_flame.txt"
                    git commit -m "New flamegraphs were generated for parameter sets "$BASEP" and "$PERFORMP"."
                    git push origin $CURRENT_BRANCH
                    # Generate data for links
                    long_url="https://www.speedscope.app/#profileURL="$WEBPAGE$FNAME"_flame.txt"
                    encode_long_url=$(urlencode $long_url)
                    short_url=$(curl -s "http://tinyurl.com/api-create.php?url=${encode_long_url}")
                    LINKS=$LINKS'\url{'$short_url'}\\\\\n'
                    CURLS=$CURLS"curl "$WEBPAGE$FNAME"_flame.svg>"$FNAME"_flame.svg\n"
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
NOTE="\nIf you want the flamegraphs locally as svgs just run\n\ncurl -OL "$WEBPAGE$BASEFLAMENAME"curlthesvgs.sh\n\n and then\n\nsh ./curlthesvgs.sh."
touch $BASEFLAMENAME"linkstosvgs.tex"
echo $LINKS"\n"$NOTE > $BASEFLAMENAME"linkstosvgs.tex"

# Generate and publish script to fetch the svg files
touch $BASEFLAMENAME"curlthesvgs.sh"
echo "#!/bin/sh\nmkdir -p ./svgs/"$BASEFLAMENAME"\ncd svgs\n"$CURLS"\n" > $BASEFLAMENAME"curlthesvgs.sh"
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