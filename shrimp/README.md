Shrimp Workflow Examples
------------------------

This directory contains the materials needed to construct a working
Shrimp workflow, with some example data.

If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/shrimp
```

First, obtain a `rmapper-cs` binary suitable for your architecture
from `compbio.cs.toronto.edu/shrimp`.  (At the time of writing,
this website was offline, so a `rmapper-cs` binary for Linux-x86
is currently included in the repository.)

If you need some example data to work with, download this to
obtain `genome.fasta` and `query.csfasta`:
```
wget http://ccl.cse.nd.edu/workflows/shrimp-example-data.tar.gz
tar xvzf shrimp-example-data.tar.gz
```

Test the rmapper-cs executable to make sure that it works locally:
```
./rmapper-cs -M fast -M 50bp query.csfasta genome.fasta
```

If that works, you can construct a workflow to parallelize it:

```
./make_shrimp_workflow query.csfasta genome.fasta output.txt 10000 > shrimp.mf
```

Then, you can use `makeflow` to run the whole thing as desired.
For example, to run it all locally:

```
makeflow shrimp.mf
```

Or to run it using HTCondor or Work Queue or SGE:
```
makeflow -T condor shrimp.mf
makeflow -T wq shrimp.mf
makeflow -T sge shrimp.mf
```

Alternatively, it can be run using the `JX` or `JSON` format
```
makeflow --jx shrimp.jx --jx-context="context.jx"
makeflow --json shrimp.json
```
To visualize the workflow that was generated:
```
makeflow_viz shrimp.mf --dot-no-labels > shrimp.dot
dot -Tpng shrimp.dot > shrimp.png
display shrimp.png
```

