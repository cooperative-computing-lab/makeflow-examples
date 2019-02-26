Makeflow Examples Repository
----------------------------

<img src=banner.png>

This is an repository of sample workflows for use with the <a href=http://ccl.cse.nd.edu/software/makeflow>Makeflow</a> workflow system.
You can use as examples of how to use Makeflow, or to benchmark the performance of your system.
If you have an interesting workflow, we would be happy to add it here; please make a pull request.

We recommend the following citation for this data:

> Nick Hazekamp and Douglas Thain, *Makeflow Examples Repository*,
> http://github.com/cooperative-computing-lab/makeflow-examples, 2017.

Some of these examples are more complete than others, as described in the README.md
files in each directory:

- BLAST, SSAHA, BWA, HECIL, BWA-GATK, SHRIMP, and Shakespeare contain complete instructions for downloading software,
generating sample data, and creating and running complete workflows from scratch.
Each workflow is demonstrated in two ways: once using the classic make language (.mf file)
and again using the JX language (.jx file).

- LIFEMAPPER and SNPEXP are static snapshots of just the workflow structure,
but do not contain the applications and data necessary to execute them.
You may find them instructive as further examples of how to write workflows.

- It should be noted that the sample data that is generated in these is complelely
random and has no value other than for showing workflow performance.
Some analysis programs may emit errors indicating low quality data.

<table cellpadding=20>
<tr><td><a href=blast><img width=128 src=blast/image.png></a><td>BLAST workflow adapted from the Biocompute web portal.  (Shown at a scale of 10 splits.)
<tr><td><a href=ssaha><img width=128 src=ssaha/image.png></a><td>SSAHA genomics analysis workflow, courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.  (Shown at scale of 25 splits.)
<tr><td><a href=bwa><img width=128 src=bwa/image.png></a><td>BWA genomics analysis workflow, courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.  (Shown at scale of 20 splits.)
<tr><td><a href=shrimp><img width=128 src=shrimp/image.png></a><td>SHRIMP genomics analysis workflow adapted from the Biocompute web portal.  (Shown at a scale of 100 splits.)
<tr><td><a href=hecil><img width=128 src=hecil/image.png></a><td>HECIL genomics analysis workflow, courtesy of Olivia Choudhury and Connor Howington.
<tr><td><a href=lifemapper><img width=128 src=lifemapper/image.png></a><td>Lifemapper Species Distribution Modeling (SDM) workflow, courtesy of C.J. Grady.  (Shown at scale of 10 species and 5 random trials.)
<tr><td><a href=snpexp><img width=128 src=snpexp/image.png></a><td>SNPEXP Genomics analysis workflow courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.
<tr><td><a href=bwa-gatk><img width=128 src=bwa-gatk/image.png></a><td>BWA-GATK genomics workflow by Nick Hazekamp and Olivia Choudhury.
<tr><td><a href=shakespeare><img width=128 src=shakespeare/image.png></a><td>Example text analysis workflow by Nate Kremer-Herman.
</table>
