<img align=right src=ssaha.png width=256></img>

SSAHA Workflow Example
----------------------

This example workflow demonstrates how to parallelize the
SSAHA2 (Sequence Search and Alignment by Hasing Algorithm)
tool published by the Sanger institute.

If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/ssaha
```

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
Alternatively, the makeflow can be run using the `JX` or `JSON` implementation
```
makeflow --jx ssaha.jx
makeflow --json ssaha.json
```

<table cellpadding=20>
<tr><td>Workflow Size<td>Reference Size(Number x Length)<td>Query Size(Number x Length)<td>Number of seq per split<td> Approx Time with Machine
<tr><td>Small<td>10000x2000 (Fixed 20M)<td>100000x100 (237K)<td>100 <td> ~5 min : 1 machine
<tr><td>Medium<td>10000x2000 (Fixed 1000M)<td>1000000x100 (237M)<td>1000 <td> ~3 : 20 machines
<tr><td>Large<td>100000x2000 (Fixed 4.0G)<td>1000000x500 (386M)<td>1000 <td> ~15 min : 20 machines
</table>


