#!/usr/bin/python

import sys
import os
import getopt


def printhelp():
	print("Creation tool for \"hello, world!\" container makeflow maker.")
	print("Usage: python make.py [ARGS]")
	print("-h,--help          Print this Help")
	print("-d,--docker        Specify Docker Image")
	print("-s,--singularity   Specify Singularity Image")

if __name__ =='__main__':
	shortargs = "d:s:h"
	longargs = ["docker=","singularity=","help"]
	docker = None
	singularity = None
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
	except getopt.GetoptError as err:
		printhelp()
		print(str(err))
		sys.exit(2)
	for o,a in opts:
		if o in ("-h","--help"):
			printhelp()
			sys.exit()
		elif o in ("-d","--docker"):
			docker = a
		elif o in ("-s","--singularity"):
			singularity = a
	
	mffile = open("Makeflow","w+")
	if not docker == None:
		mffile.write("hello-docker.out: \n\tdocker run %s sh -c 'echo \"hello, world!\" > hello-docker.out'\n\n"%docker)
	if not singularity == None:
		imffile.write("hello-sing.out: %s \n\tsingularity exec %s sh -c 'echo \"hello, world!\" > hello-docker.out'\n\n"%(singularity,singularity))
	
	if docker == None and singularity == None:
		print("Making empty Makefile!!")
		printhelp()
	mffile.close()
	sys.exit()
