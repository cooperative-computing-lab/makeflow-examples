
#!/bin/bash

# Command-line input - $1: List_Reference.txt, $2: Pileup File 

f_reflist=$1
f_pileup=$2
num_ref=$3
size_partition=$4

#echo $1, $2, $3, $4

# Create subset pileup files, each containing $size_partition number of reference contig/header
for ((i=$size_partition; i<=$num_ref; i+=$size_partition))
do
	#echo $i
	c=$(($c+1))
	beg=$(($i-$size_partition-1))
	beg_ref="$(sed -n "$beg"p "$f_reflist")"
	end_ref="$(sed -n "$i"p "$f_reflist")"

	# Get line number of the line where the beg_ref starts (head -1)	
	pileup_linenum_beg="$(grep -n "$beg_ref" "$f_pileup" | head -1 | awk -F ':' '{print $1}')"
	# Get line number of the line where end_ref ends (tail -1)
	pileup_linenum_end="$(grep -n "$end_ref" "$f_pileup" | tail -1 | awk -F ':' '{print $1}')"

	# Save each line in putput of sed as an element of the array
	declare -a subset
	f_out='Pileup_Set'$c'.txt'

	#break
	sed -n "$pileup_linenum_beg,${pileup_linenum_end}p" $f_pileup > $f_out

done




