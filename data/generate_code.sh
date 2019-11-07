#!/bin/bash

for line in $(cat course_list1)
do
    for n1 in {0..9}
    do    
        for n2 in {000..999}
        do 
            echo $line$n1$n2
        done
    done
done