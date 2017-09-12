# Makeflow Benchmarking Tool
The Makeflow Benchmarking Tool is a tool designed to help developers and researchers test the viability of different platforms to run workflows. The tool enables control over 5 factors: execution time of worker, having the worker produce output, the size of the common input file, the size of the unique input files, and the number of jobs in the DAG.

The DAG itself is extremely flat, with no jobs dependant on one another.


###### the\_job
This is the worker which performs the operations. To create this file, call:

```
make
```

and the program will compile.

###### make\_benchmark
This is the python script which will generate the makeflow file. Please ensure that you have Python 2.7+ installed to run it.


## Using the Software
First, ensure that `the_job` has been compiled by calling:
```
make
```

Next, call `make_benchmark` with the proper flags to generate your makeflow. The following is an example call:

```
./make_benchmark --run-time=10 --unique-size=10MB --common-size=10GB --pass-unique --null-output --number=1000
```

This call will create a workflow with 1000 jobs, along with 1000 unique input files each 10MB large, and a single 10GB large common file. While the job will recieve the 10MB file, it will not read it, and instead write out 4MB of data to /dev/null. The job will also spend 10 seconds doing busy work.

Let's break that down.

`--run-time=10` specifies that each job should do 10 seconds of pure CPU busy work.
`--unique-size=10MB` specifies that each job should have associated with it a unique input file filled with 10MB of random data.
`--common-size=10GB` specifies that a single 10GB file will be created and filled with random data, and passed to each job as an input file.
`--pass-unique` specifies that while the unique file should be sent to the worker which takes the job, the `the_job` program will not read it. Rather, 4MB of random data will be written out to output.
`--null-output` specifies that the output of `the_job` should go to /dev/null.
`--number=1000` specifies that 1000 jobs should be created.


Here is a copy of the running `make_benchmark --help` specifying all of the different parameters and what they do:

```
-s,--unique-size    The size for each unique file
-c,--common-size    The size for the common file
-t,--run-time       The processing time for the program
-n,--number         How many jobs to make
-P,--pass-common    Require the common input file to be an input file, but do not have the program read it
-P,--pass-unique    Require the unique input file to be an input file, but do not have the program read it
-O,--no-output      Tells the program to make empty output file
-z,--null-output    Tells the program to send all output to /dev/null
-h,--help           Prints this out
```
