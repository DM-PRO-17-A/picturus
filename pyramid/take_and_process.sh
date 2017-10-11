#!/bin/bash

counter=1

while [ $counter -le 10 ]
do
    filepath=$(python /home/embrik/Datamaskinprosjekt/picturus/pyramid/fspyramid.py)
    echo $filepath
    python pyramid.py --image $filepath
    ((counter++))
done
