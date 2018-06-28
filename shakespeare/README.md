<img align=right src=shakespeare.png width=256></img>

Shakespeare Workflow Example
--------------------

This workflow gives an example of using Makeflow to parallelize
a text search through a collection of William Shakespeare's plays.
Makeflow will run download the plays, package up the version of
Perl at the location Makeflow is running, and run a text analysis
Perl script in parallel to figure out which character had the most
dialogue out of the plays selected.


If you have not done so already, please clone this example repository like so:
```
git clone https://github.com/cooperative-computing-lab/makeflow-examples.git
cd ./makeflow-examples/shakespeare
```

Finally, execute the workflow using makeflow locally,
or using a batch system like Condor, SGE, or Work Queue:

```
makeflow shakespeare.mf
makeflow -T condor shakespeare.mf
makeflow -T sge shakespeare.mf
makeflow -T wq shakespeare.mf
```
Alternatively, the makeflow can be run using the `JX` or `JSON` format:
```
makeflow --jx shakespeare.jx --jx-args="args.jx"
makeflow --json shakespeare.json"
```
