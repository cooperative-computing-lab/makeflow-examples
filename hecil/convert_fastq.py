#! /usr/bin/env python3

############################################
#
# convert_fastq.py
#
# Converts a FASTQ file to FASTA format
#
# Author: Connor Howington
# Date: 7/19/17
#
# Python 3
#
############################################

import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Converts a FASTQ file to FASTA format.  Sends to stdout.')
	parser.add_argument('fastq')

	return parser.parse_args()

def convert_fastq(fastq_path):
	with open(fastq_path) as fastq:
		line = fastq.readline().rstrip()

		while line != '':
			print('>' + line[1:])
			line = fastq.readline().rstrip()

			# Split sequence into 80-char segments (recommended length of a fasta file line)
			split_line = [line[i:i+80] for i in range(0, len(line), 80)]
			print('\n'.join(split_line))

			for i in range(2): fastq.readline()   # Skip the next two lines
			line = fastq.readline().rstrip()

# Main flow
args = parse_args()
convert_fastq(args.fastq)

