BWA Workflow Example
--------------------

This workflow gives an example of using Makeflow to parallelize
the Burroughs-Wheeler Alignment (BWA) tool.

If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/bwa
```

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

<table cellpadding=20>
<tr><td>Workflow Size<td>Reference Size(Number x Length)<td>Query Size(Number x Length)<td>Number of seq per split<td> Approx Time with Machine
<tr><td>Small<td>10000x1000 (Fixed 20M)<td>1000x100 (237K)<td>100 <td> ~10 sec : 1 machine
<tr><td>Medium<td>100000x1000 (Fixed 196M)<td>10000x1000 (20M)<td>1000 <td> ~2 min : 20 machines
<tr><td>Medium<td>100000x1000 (Fixed 196M)<td>1000000x100 (237M)<td>1000 <td> ~6 min : 20 machines
<tr><td>Large<td>1000000x1000 (Fixed 2.0G)<td>1000000x100 (237M)<td>1000 <td> ~30 min : 20 machines
</table>


Note: when using generated data we did not use the paired-end functionality of BWA
as we do not guarantee both query and rquery are matched as a pair would be in real data.
