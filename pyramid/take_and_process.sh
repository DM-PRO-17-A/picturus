#!/bin/bash

counter=1

while [ $counter -le 1 ]
do
    filepath=$(python fspyramid.py)
    echo $filepath
    python pyramid.py --image $filepath
    ((counter++))
done
