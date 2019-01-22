#!/bin/bash

layout="$1"
alg="$2"
specified=$3

# echo "layout = $layout"
# echo "alg = $alg"
# echo "specified = $specified"

if [[ "$specified" = "" ]]; then
    echo -e "Running layout ${layout}\n"
    echo -e "Now running ${alg}\n"
    if [[ "$alg" = "dfs" ]]; then
        python pacman.py -l ${layout} -p SearchAgent
    elif [[ "$alg" = "bfs" ]]; then
        python pacman.py -l ${layout} -p SearchAgent -a fn=bfs
    elif [[ "$alg" = "ucs" ]]; then
        python pacman.py -l ${layout} -p SearchAgent -a fn=ucs
    elif [[ "$alg" = "astar" ]]; then
        python pacman.py -l ${layout} -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic --frameTime 0
    elif [[ "$alg" = "all" ]]; then
        echo "Running all"
        echo "------------------------------------------------------------------"
        echo -e "Now running dfs\n"
        python pacman.py -l ${layout} -p SearchAgent -z .5 --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running bfs\n"
        python pacman.py -l ${layout} -p SearchAgent -a fn=bfs -z .5 --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running ucs\n"
        python pacman.py -l ${layout} -p SearchAgent -a fn=ucs -z .5 --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running astar\n"
        python pacman.py -l ${layout} -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "Done"
    else
        echo "Rip"
    fi
else
    echo -e "Running ${specified}\n"
    echo "------------------------------------------------------------------"
    if [[ "$specified" = "dfs" ]]; then
        echo -e "Now running tinyMaze\n"
        python pacman.py -l tinyMaze -p SearchAgent
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running mediumMaze\n"
        python pacman.py -l mediumMaze -p SearchAgent --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running bigMaze\n"
        python pacman.py -l bigMaze -z .5 -p SearchAgent --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "Done"
    elif [[ "$specified" = "bfs" ]]; then
        echo -e "Now running mediumMaze\n"
        python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running bigMaze\n"
        python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5 --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "Done"
    elif [[ "$specified" = "ucs" ]]; then
        echo "Now running mediumMaze"
        python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running StayEastSearchAgent\n"
        python pacman.py -l mediumDottedMaze -p StayEastSearchAgent --frameTime 0
        echo -e "------------------------------------------------------------------\n"
        echo "------------------------------------------------------------------"
        echo -e "Now running StayWestSearchAgent\n"
        python pacman.py -l mediumScaryMaze -p StayWestSearchAgent --frameTime 0
    elif [[ "$specified" = "astar" ]]; then
        python pacman.py -l mediumMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic --frameTime 0
    elif [[ "$specified" = "q5" ]]; then
        echo "Running for question 5"
        echo "------------------------------------------------------------------"
        python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
        python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    fi
    echo -e "------------------------------------------------------------------\n"
    echo "Done"
fi
