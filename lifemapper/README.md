# Lifemapper

This version of the Lifemapper Makeflow generator splits a single csv file 
containing multiple taxa into groups such that like taxa are adjacent to each
other into files.  These files are used as inputs to models (if there are
enough points) and projections under different climate scenarios.

## Small Example

This example processes a small dataset and only one model/projection scenario with 183 rules in the workflow.

    python split.py data/points/small.csv

To run it, make sure Makeflow is in your `$PATH` and type

    makeflow --jx lifemapper.jx

## Larger Example

This example runs on a larger dataset with a model scenario
and three projection scenarios each.

    python split.py data/points/large.csv

This example consists of 3145 rules and runs all three projection scenarios.

    makeflow --jx-define 'PROJECTIONS=["data/layers/" + x for x in listdir("data/layers")]' --jx lifemapper.jx
