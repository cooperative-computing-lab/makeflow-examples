#!/usr/bin/perl

use strict; 

my $numargs = $#ARGV + 1;
if ($numargs != 2) {
	print STDERR "Usage: fastq_split.pl <input file> <number of reads per file>\n";
	exit 1;
}
my $file = $ARGV[0];
my $num_reads = $ARGV[1];
my $num_outputs = 0;

open(INPUT, $file);
my $read_count = 0;
open (OUTPUT,">$file.$num_outputs");
while (my $line = <INPUT>) {
	chomp $line;
	if ($line =~ /^[@]/){
		if ($read_count == $num_reads){
			$num_outputs++;
			close(OUTPUT);
			open(OUTPUT, ">$file.$num_outputs");
			$read_count = 0;
		}else{
			$read_count++;
		}
	}
	print OUTPUT $line;
	print OUTPUT "\n";
}
close OUTPUT;

print "$num_outputs\n";
