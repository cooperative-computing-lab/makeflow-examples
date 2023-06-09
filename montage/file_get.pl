#!/usr/bin/perl
#
#Copyright (C) 2016- The University of Notre Dame
#This software is distributed under the GNU General Public License.
#See the file COPYING for details.
#

use strict; 
use Scalar::Util qw(looks_like_number);
use Math::Complex;
use POSIX;

my $num_args = $#ARGV + 1;
if($num_args ne 1) {
	print "Must specify input data file.\n";
	exit 1;
}

my $in = $ARGV[0];
my $result = 0;
my $i = 1;
open(INPUT, $in);

	while (my $line = <INPUT>) {
		chomp $line;
		my @parts = split(" ",$line);
		my $final = $parts[0];
		my $intermediate = $parts[0] . ".gz";
		my $url = $parts[1];
		$result = system("curl $url -o $intermediate");
		if($result ne 0) { print "Error in curl #$i\n"; exit 1; }
		$result = system("gunzip -c $intermediate > $final; rm $intermediate");
		if($result ne 0) { print "Error in gunzip and rm #$i\n"; exit 1; }
		$i++;
		sleep(1);
	}

close(INPUT);
exit 0;
