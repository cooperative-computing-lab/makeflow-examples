# Lifemapper

This version of the Lifemapper Makeflow generator splits a single csv file 
containing multiple taxa but grouped so that like taxa are adjacent to each
other into files.  These files are used as inputs to models if there are
enough points and the projections.

## Small Example

This example processes a small dataset and only one model/projection scenario.

    python split.py data/points/small.csv small/ 

To run it, make sure Makeflow is in your `$PATH` and type

    makeflow --jx-define 'POINTS_DIR="small"' --jx-define 'PROJECTIONS=["data/layers/worldclim"]' --jx template.jx

## Larger Example

This example runs on a larger dataset with a model scenario
and three projection scenarios each.

    python split.py data/points/large.csv large

This example runs all three projection scenarios.

    makeflow --jx-define 'POINTS_DIR="large"' --jx template.jx
