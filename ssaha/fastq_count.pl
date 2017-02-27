#!/usr/bin/perl

# Count the number of sequences in a FASTQ file.

if($#ARGV!=0) {
	print "Count the number of sequences in a FASTQ file.\n";
	print "Use: $0 <filename>\n";
	exit(0);
}

$filename = $ARGV[0];
$count = 0;

open FILE, $filename or die "$0: couldn't open $ARGV[0]\n";
while(<FILE>) {
	if(/^@.*/ ) {
		$count++;
	}
}
close FILE;

print "$count\n";


