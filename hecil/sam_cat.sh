#!/bin/bash

grep -v "^@PG" $1

for ((i=1; i<$#; i++))
do
	cat Out.$i.sam | grep -v "^@"
done

