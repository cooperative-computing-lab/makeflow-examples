
#!/bin/bash

#USAGE: ./Split_Pileup.sh Pileup.txt 20
# Command line arguments: $1: Pileup File, $2: Number of partitions


# Create List_RefHeader.txt that contains list of unique reference contig/header
echo -e 'Calculating number of reference contigs\n'
awk '{print $1}' $1 | uniq > List_RefHeader.txt

num_ref="$(wc -l List_RefHeader.txt | awk '{print $1}')"
# Based on number of partitions (input argument), find number of reference header
# to keep in each Pileup subset file
size_partition="$(expr $num_ref / $2)"

if [ $size_partition -eq 0 ]
then
	
	size_partition=1
fi

echo -e "Splitting Pileup file into "$2" subsets\n"

./Create_SubsetPileup.sh List_RefHeader.txt $1 $num_ref $size_partition


echo -e "Finished splitting pileup\n"

