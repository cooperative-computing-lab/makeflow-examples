Hello, World! Workflow Example
----------------------

This directory contains the materials needed to run a "Hello, World!" workflow.
The idea behind this is to simply show off how makeflow represents a workflow,
generating files and running commands.

The command is as follows:

```
hello.out:
	echo "hello, world!" > hello.out
```

This demonstrates how Workflows are constructed: specifying an output, and any inputs,
(none in this case), and the command which generates the outputs.

To run this call:

```
makeflow hello_world.mf
```
