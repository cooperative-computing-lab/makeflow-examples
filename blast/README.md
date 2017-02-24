This directory contains the materials needed to construct a blast workflow.
However, you will first need to install the blast software and a suitable
database before you can run the makeflow.

First, obtain a blast binary suitable for your architecture. (about 30MB)
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy/2.2.26/blast-2.2.26-x64-linux.tar.gz
tar xvzf blast-2.2.26-x64-linux.tar.gz
```

Next, copy the main executable into the working directory.
```
cp blast-2.2.6/bin/blastall .
```

Obtain a nucleotide database suitable for searching. (about 400MB)
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/nt.44.tar.gz
mkdir nt
tar -C nt xvzf nt..44.tar.gz
```

Now, test to make sure that blast works locally:
```
./blastall -p blastn -d nt/nt -i small.fasta

```

If everything is working correctly, you should see output that starts like this:

```
BLASTN 2.2.26 [Sep-21-2011]

Reference: Altschul, Stephen F., Thomas L. Madden, Alejandro A. Schaffer, 
Jinghui Zhang, Zheng Zhang, Webb Miller, and David J. Lipman (1997), 
"Gapped BLAST and PSI-BLAST: a new generation of protein database search
programs",  Nucleic Acids Res. 25:3389-3402.

```

And then goes on for quite a while.

Now you are ready to generate workflow that will do the job in parallel.
Use the `makeflow_blast` script to create a workflow `blast.mf` that
will split up the input into several pieces, run blast on each one,
and then join the results together:

```
./makeflow_blast -d nt -i small.fasta -o output.fasta -p blastn --num_seq 10 --makeflow blast.mf
```

Then, you can use `makeflow` to run the whole thing as desired.
For example, to run it all locally:

```
makeflow blast.mf
```

To run it using HTCondor:

```
makeflow -T condor blast.mf
```

To run it using SGE:

```
makeflow -T sge blast.mf
```

