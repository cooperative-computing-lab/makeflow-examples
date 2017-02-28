This example workflow demonstrates how to parallelize the
SSAHA2 (Sequence Search and Alignment by Hasing Algorithm)
tool published by the Sanger institute.

First, download and install a suitable binary for SSAHA2:

```
export SSAHA_BINARY=ssaha2_v2.5.5_x86_64
wget ftp://ftp.sanger.ac.uk/pub/resources/software/ssaha2/${SSAHA_BINARY}.tgz
tar xvzf ${SSAHA_BINARY}.tgz
cp ${SSAHA_BINARY}/ssaha2 .
```

If you do not have any data of your own, you can generate some random
data for testing purposes in FASTQ format.  The first argument to
fastq generate is the number of sequences, and the second is the
length of sequences.

```
./fastq_generate.pl 10000 2000 > db.fastq
./fastq_generate.pl 100000 100 db.fastq > query.fastq
```

Make sure that the sequential ssaha executable works.
This should run in ~5 minutes, so cancel it once you are
satisfied it is working.

```
./ssaha2 db.fastq query.fastq
```

Then, generate a workflow to parallelize the job into
sub-jobs of 1000 sequences each:

```
./make_ssaha_workflow db.fastq query.fastq output.fastq 1000 > ssaha.mf
```

Finally, run the workflow using makeflow locally, or using
a batch system:

```
makeflow ssaha.mf
makeflow -T condor ssaha.mf
makeflow -T sge ssaha.mf
makeflow -T wq.ssaha.mf
```

This should create a workload that runs in ~50 minutes on a single core machine or ~3 minutes on 20 workers
```
./fastq_generate.pl 10000 2000 > db.fastq
./fastq_generate.pl 1000000 100 db.fastq > query.fastq
./make_ssaha_workflow db.fastq query.fastq output.fastq 1000 > ssaha.mf
```

This should create a workload that runs in ~5 hours on a single core machine or ~15 minutes on 20 workers
```
./fastq_generate.pl 100000 2000  > db.fastq
./fastq_generate.pl 1000000 500 db.fastq > query.fastq
./make_ssaha_workflow db.fastq query.fastq output.fastq 1000 > ssaha.mf
```

