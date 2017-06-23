BWA Workflow Example
--------------------

This workflow gives an example of using Makeflow to parallelize
the Burroughs-Wheeler Alignment and Genome Analysis Toolkit (BWA-GATK) tool.

NOTE: This implementation requires Java version 1.7, please make sure you are using the correct Java version.

If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/bwa-gatk
```

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

In order to run BWA-GATK, you will need real data.
The generator script we use relies on a barcode for real data.
However, the data we use is private.
Please contact the Cooperative Computing Lab if you do not have
your own dataset to test with.

Then, generate a workflow to process.
In this example we use the data detailed in a barcode file on 10 splits:

```
./make_bwa_gatk_workflow barcode_file.txt 10 > bwa_gatk.mf
```

Finally, execute the workflow using makeflow locally,
or using a batch system like Condor, SGE, or Work Queue:

```
makeflow bwa_gatk.mf
makeflow -T condor bwa_gatk.mf
makeflow -T sge bwa_gatk.mf
makeflow -T wq bwa_gatk.mf
```
