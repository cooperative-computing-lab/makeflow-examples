Makeflow Examples Repository
----------------------------

This is an repository of sample workflows for use with the <a href=http://ccl.cse.nd.edu/software/makeflow>Makeflow</a> workflow system.
You can use as examples of how to use Makeflow, or to benchmark the performance of your system.
If you have an interesting workflow, we would be happy to add it here; please make a pull request.

We recommend the following citation for this data:

> Nick Hazekamp and Douglas Thain, *Makeflow Examples Repository*,
> http://github.com/cooperative-computing-lab/makeflow-examples, 2017.

Some of these examples are more complete than others, as described in the README.md
files in each directory:

- BLAST, SSAHA, and BWA contain complete instructions for downloading software,
generating sample data, and creating and running complete workflows from scratch.
The other examples are static snapshots of workflows for display
or analysis, but do not contain the actual applications necessary to run them.

- It should be noted that the sample data that is generated in these is complelely
random and has no value other than for showing these workflows in action. As a result
some generated behavior may appear to cause issues when programs expect some format 
or quality guarantee.

<table cellpadding=20>
<tr><td><img width=128 src=blast/blast.png><td>BLAST workflow adapted from the Biocompute web portal.  (Shown at a scale of 10 splits.)
<tr><td><img width=128 src=ssaha/ssaha.png><td>SSAHA genomics analysis workflow, courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.  (Shown at scale of 25 splits.)
<tr><td><img width=128 src=bwa/bwa.png><td>BWA genomics analysis workflow, courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.  (Shown at scale of 20 splits.)
<tr><td><img width=128 src=lifemapper/lifemapper.png><td>Lifemapper Species Distribution Modeling (SDM) workflow, courtesy of C.J. Grady.  (Shown at scale of 10 species and 5 random trials.)
<tr><td><img width=128 src=snpexp/snpexp.png><td>SNPEXP Genomics analysis workflow courtesy of Scott Emrich and Notre Dame Bioinformatics Laboratory.
<tr><td><img width=128 src=bwa-gatk/bwa-gatk.png><td>BWA-GATK genomics workflow by Nick Hazekamp and Olivia Choudhury.
</table>
