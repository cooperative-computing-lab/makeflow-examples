<img align=right src=blast.png width=256>

BLAST Workflow Example
----------------------

This directory contains the materials needed to construct a blast workflow.
However, you will first need to install the blast software and a suitable
database before you can run the makeflow.

If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/blast
```

First, obtain a blast binary suitable for your architecture. (about 30MB)
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
tar xvzf blast-2.2.26-x64-linux.tar.gz
```

Next, copy the main executable into the working directory.
```
cp blast-2.2.26/bin/blastall .
```

Obtain a nucleotide database suitable for searching. (about 400MB)
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/nt.44.tar.gz
mkdir nt
tar -C nt -xvzf nt.44.tar.gz
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

Or to run it using HTCondor or Work Queue or SGE:
```
makeflow -T condor blast.mf
makeflow -T wq blast.mf
makeflow -T sge blast.mf
```

To visualize the workflow that was generated:
```
makeflow_viz blast.mf --dot-no-labels > blast.dot
dot -Tpng blast.dot > blast.png
display blast.png
```

Additionally, you can generate random data to adjust the total runtime:
```
./fasta_generator 200 1000 > test.fasta
./makeflow_blast -d nt -i test.fasta -p blastn --num_seq 5 --makeflow blast_test.mf
makeflow blast_test.mf
```

Alternatively, the makeflow can be run using `JX` or `JSON` formats using one of the following commands:
```
makeflow --jx blast.jx
makeflow --json blast.json
```

The number and length of sequences can be adjusted for your needs, with the first number 
adjusting the number of contigs and the second adjusting the length of these contigs.
`fasta_generator` produces contigs containing random AGCT sequences.

The provided values produces a workflow that runs in ~5 minutes on a local single core machine.

<table cellpadding=20>
<tr><td>Workflow Size<td>Reference Size<td>Query Size(Number x Length)<td>Number of seq per split<td> Approx Time with Machine
<tr><td>Small<td>NT (Fixed 565MB)<td>200x1000 (198K)<td>5 <td> ~5 min : 1 machine
<tr><td>Medium<td>NT (Fixed 565MB)<td>30000x2000 (58M)<td>100 <td> ~20 min : 20 machines
<tr><td>Large<td>NT (Fixed 565MB)<td>100000x2000 (193M)<td>1000 <td> ~30 min : 75 machines
</table>

