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
data for testing purposes in FASTQ format:

```
./fastq_generate 1000 100 > query.fastq
./fastq_generate 100000 1000 > db.fastq
```

Make sure that the sequential ssaha executable works.
This may run a long time, so cancel it once you are
satisfied it is working.

```
./ssaha2 db.fastq query.fastq
```

Then, generate a workflow to parallelize the job into
sub-jobs of 100 sequences each:

```
./make_ssaha_workflow ssaha.mf 100
```

Finally, run the workflow using makeflow locally, or using
a batch system:

```
makeflow ssaha.mf
makeflow -T condor ssaha.mf
makeflow -T sge ssaha.mf
makeflow -T wq.ssaha.mf
```
