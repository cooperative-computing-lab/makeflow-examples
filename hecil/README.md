<img align=left src=hecil.png width=256></img>
HECIL Workflow Example
----------------------

This workflow gives an example of using Makeflow to parallelize
the Hybrid Error Correction with Iterative Learning (HECIL) tool.

Citation:
"HECIL: A Hybrid Error Correction Algorithm for Long Reads with Iterative Learning",
Olivia Choudhury, Ankush Chakrabarty, and Scott Emrich
bioRxiv preprint, 2017.
https://doi.org/10.1101/162917

The conversion of HECIL into a workflow was accomplished
by Connor Howington as part of a summer REU project at Notre Dame.

Installation and Use
--------------------

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
./fastq_generate.pl 100000 1000 > ref.fastq
./fastq_generate.pl 10000 100 ref.fastq > query.fastq
```

The long read file needs to be in fasta format, so you'll need to convert it:

```
./convert_fastq.py ref.fastq > ref.fasta
```

Then, generate a workflow to process the data:

```
./make_hecil_workflow -l ref.fasta -s query.fastq -len 100 -p 100 -ps 2 -rs 1000
```

Finally, execute the workflow using makeflow locally
or using a batch system like Condor, SGE, or Work Queue:

```
makeflow hecil.mf
makeflow -T condor hecil.mf
makeflow -T sge hecil.mf
makeflow -T wq hecil.mf
```

corr.out (default) contains only the corrected long reads.  Corrected_ref.fasta contains all reads, with the corrected reads replacing the old reads (order is not conserved from input fasta file).

