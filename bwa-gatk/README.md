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

Next, you will need to get GATK.
First, register for an account with the Broad Institute at <a href="https://software.broadinstitute.org/gatk/download/">software.broadinstitute.org</a>.

After registering for an account, you will be able to download the GATK software. 
We use version 3.7, but you may download the latest version if you like. 
Make sure you download it to your working directory. 
Once it is downloaded, it can be extracted like so:

```
tar -jxvf GenomeAnalysisTK-3.7-0.tar.bz2
```

You will also need to download Picard to properly run the software:

```
wget https://github.com/broadinstitute/picard/releases/download/2.9.4/picard.jar
```

You will also need SAMtools:
```
wget https://github.com/samtools/samtools/releases/download/1.4.1/samtools-1.4.1.tar.bz2
tar -jxvf samtools-1.4.1.tar.bz2
cd samtools-1.4.1
make prefix=. install
cp bin/samtools ..
cd ..
```

If you do not have real data to work with, then generate
some simulated data (~10 second workflow):

```
./fastq_generate.pl 10000 1000 > ref.fastq
./fastq_generate.pl 1000 100 ref.fastq > query.fastq
```

In order to run BWA-GATK, you will need real data.
The generator script we use relies on a barcode for real data.
However, the data we use is private.
Please contact the Cooperative Computing Lab if you do not have
your own dataset to test with.

Then, generate a workflow to process the data detailed in the barcode file on 100 splits:

```
./make_bwa_gatk_workflow barcode_file.txt 100 > bwa_gatk.mf
```

Finally, execute the workflow using makeflow locally,
or using a batch system like Condor, SGE, or Work Queue:

```
makeflow bwa_gatk.mf
makeflow -T condor bwa_gatk.mf
makeflow -T sge bwa_gatk.mf
makeflow -T wq bwa_gatk.mf
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
