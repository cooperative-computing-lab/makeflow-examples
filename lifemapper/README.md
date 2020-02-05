<img align=right src=image.png width=256></img>

# Lifemapper

This version of the Lifemapper Makeflow generator splits a single csv file 
containing multiple taxa into groups such that like taxa are adjacent to each
other into files.  These files are used as inputs to models (if there are
enough points) and projections under different climate scenarios.
The workflow is comprised of a large number of independent taxa (pictured).
The included dataset contains a number of invalid samples,
so the workflow generates a lot of noise.
You should expect to see numerous errors like

    Exception in thread "main" java.util.NoSuchElementException
        at java.util.StringTokenizer.nextToken(StringTokenizer.java:349)
        at density.Project.projectGrid(Project.java:152)
        at density.Project.doProject(Project.java:112)
        at density.Project.main(Project.java:522)

and

    Warning: Sample at 32.2275, -109.781389 in Conanthalictus_conanthi.csv is outside the bounding box of environmental data, skipping
    Warning: Sample at 32.2275, -109.781389 in Conanthalictus_conanthi.csv is outside the bounding box of environmental data, skipping
    Warning: Sample at 32.2275, -109.781389 in Conanthalictus_conanthi.csv is outside the bounding box of environmental data, skipping
    Warning: Sample at 32.2275, -109.781389 in Conanthalictus_conanthi.csv is outside the bounding box of environmental data, skipping
    Warning: Sample at 32.2275, -109.781389 in Conanthalictus_conanthi.csv is outside the bounding box of environmental data, skipping

The workflow will finish successfully after processing as much data as possible.
This example requires Java.
It may be installed or available through your system's package manager.
You can also download Java [here](https://java.com/en/download/manual.jsp).

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
