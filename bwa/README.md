BWA Workflow Example
--------------------

This workflow gives an example of using Makeflow to parallelize
the Burroughs-Wheeler Alignment (BWA) tool.

First, build the bwa binary for your architecture:

```
git clone https://github.com/lh3/bwa bwa-src
cd bwa-src
make
cp bwa ..
cd ..
```

If you do not have real data to work with, then generate
some simulated data (~10 second workflow):

```
./fastq_generate.pl 10000 1000 > ref.fastq
./fastq_generate.pl 1000 100 ref.fastq > query.fastq
```

Then, generate a workflow to process the data:

```
./make_bwa_workflow --ref ref.fastq --query query.fastq --num_seq 100 > bwa.mf
```

Finally, execute the workflow using makeflow locally,
or using a batch system like Condor, SGE, or Work Queue:

```
makeflow bwa.mf
makeflow -T condor bwa.mf
makeflow -T sge bwa.mf
makeflow -T wq bwa.mf
```

Workflow ~2 mins on 20 workers:

```
./fastq_generate.pl 100000 1000 > ref.fastq
./fastq_generate.pl 10000 1000 ref.fastq > query.fastq
./make_bwa_workflow --ref ref.fastq --query query.fastq --num_seq 1000 > bwa.mf
```

Workflow ~6 mins on 20 workers:

```
./fastq_generate.pl 100000 1000 > ref.fastq
./fastq_generate.pl 1000000 100 ref.fastq > query.fastq
./make_bwa_workflow --ref ref.fastq --query query.fastq --num_seq 1000 --algo backtrack > bwa.mf
```

