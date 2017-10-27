# Converting JSON to JX #

## JX ##
JX is a language that simplfies and shortens interaction with the Makeflow program. At the core, JX is an extended JSON form.  It allows for the formatting of strings, for loops to iterate over a rule, list comprehension, and `join` functions to create single strings out of lists.

Additionally, external variables can be defined in an external `context` file, where lists, strings, and values can be defined for use within the JX structure.

## General Structure ##
The JX structure is a JSON object with a single "rules" key, which contains a list of separate rules.  Each rule entry is another object containing, at the least, and "outputs", "inputs", and "command" key.  "inputs" and "outputs" contains a list of input and output files respecgively, and the "commmand" key contains a single string.

A content file is a single JSON that contains a list of key-value pairs. The values could possibly contain a list using list comprehension as well to create the values.

## Using Functions ##

### Format ###
Format operates in much the same way that it does in C.  Format requires a string in the first object.  Within each string, values are defined to be placed inside of the string using `%_` where `_` indicates a character from the set `d i e E f F g G s`.  In these cases, `d` and `i` represent integers, `s` represents a string and the rest represent doubles.

Format is mostly used in cases where an integer is needed, or a value from the context file is needed.  If a context file value is defined within the string literal, it will be interpreted as the characters.  So it will be necessary to define the location with the necessary tag.

An example of this is the following command:
```format("%s %s %s %s.%d > Out.%d.sam 2> mem.%d.err", BWA, ARGS, REF, INPUT_PRE, i, i, i)```
This allows for the use of variables.  Of particular interest is `i`.  This is a digit and allows this section to be iterated over.  As a result, 100 rules could be significantly reduced.

### Range ###
This function is not normally used by itself.  It is usually in conjunction with a For Loop.  A range can be defined with a single value, in which case a list from 0 to n-1 is generated where n is the value given to range.  Similarly, with two value `range(x,y)` a list from x to y, not including y is produced.  For `range(x, y, z)` a list from x to y, not including y, stepping up, or down by z.

Range is usually used in the following case:
```for i in range(SPLIT_SIZE)```

### For and List Comprehension ###
For loops in JX operate are performed over iterables.  They can be used to iterate over a particular list or over a range of values.

List:
```x for x in ["amb", "ann", "bwt", "pac", "sa"]```
Range:
```for i in range(SPLIT_SIZE)```

When a for loop is placed at the end of a structures, it will iterate over the structure the given number of times, changing the variable, allowing for the more efficient creation of rules.  A more in-depth eample of this will be given below.

For loops can also be used within the scope of a list comprehension:
```["ref.fasta." + x for x in ["amb", "ann", "bwt", "pac", "sa"]]```

### Join ###
Join concatenates a list of strings to create a single string with an optional delimeter.  If none is provided, then a space is used as a delimeter.  Usually, a join function is used in conjunction with some sort of list comprehension to create a longer length string of multiple similar elements.

```join([format("Out.%d.sam", x) for x in range(SPLIT_SIZE)])```

## Usage Example ##
There are several different ways that these functions can shorten a json list of rules, and create a more comprehendable input file for the reader.

### Many Inputs and Outputs of the same Style ###
In the case where there are several different strings in the input or the output of the same style (i.e. `query.fastq.{0-9}`) then we can use a for loop and list comprehension.  For example if we have the following output key-value pair:
```
"outputs" : [
       "query.fastq.0",
       "query.fastq.1", 
       "query.fastq.2",
       "query.fastq.3",
       "query.fastq.4",
       "query.fastq.5",
       "query.fastq.6",
       "query.fastq.7",
       "query.fastq.8",
       "query.fastq.9"
]
```
This can be greatly reduced with a forloop and list comprehension with the following.
```
"outputs":[
       format("%s.%d", INPUT_PRE, x) for x in range(SPLIT_SIZE),
]
```
The format command is iterated over several time, where `INPUT_PRE` is `query.fastq.` and `SPLIT_SIZE` is `10` as defined in the context file.

### Many Rules of the Same Style ###
If we have mutiple rules of the same style, for example:
```
{
	 "outputs" : [
        "Out.0.sam",
        "mem.0.err"
     ],
     "inputs" : [
        "./bwa",
        "ref.fasta.amb",
        "ref.fasta.ann",
        "ref.fasta.bwt",
        "ref.fasta.pac",
        "ref.fasta.sa",
        "query.fastq.0"
     ],
     "command" : "./bwa mem ref.fasta query.fastq.0 > Out.0.sam 2> mem.0.err"
}
```
where the only items changing through the rule is the integer 0 counting upwards to 9.  the obvious answer is to iterate over this rule nine times and to change x variable representing the changing digit through each iteration.  This can be done in this way:
```
{   
   "command": format(
        "%s %s %s %s.%d > Out.%d.sam 2> mem.%d.err",
        BWA,
        ARGS,
        REF,
        INPUT_PRE, i, i, i,
   ),  
   "inputs": [
        BWA,
        x for x in REF_INDEX,
        format("%s.%d", INPUT_PRE, i), 
   ],  
   "outputs": [
        format("Out.%d.sam", i), 
        format("mem.%d.err", i), 
   ]   
} for i in range(SPLIT_SIZE)
```
All the capital variables are simply values defined in the context file. However, the for loop after the closing brace indicated that we will be iterating over this rule several times.  The defined value `i` is placed throughout the rule, and it is replaced in those locations as is necessary.  The ending result is a `SPLIT_SIZE` number of analgous rules where only the digit in question has been changed.

### Command Requires String of Inputs of the Same Style ###
This final example makes use of join, for and format.  Often, the different files must be concatenated into one single string for a command.  This could be a command such as the following:
```
"command" : "cat Corrected_ref.fasta.0 Corrected_ref.fasta.1 Corrected_ref.fasta.2 Corrected_ref.fasta.3 Corrected_ref.fasta.4 Corrected_ref.fasta.5 Corrected_ref.fasta.6 Corrected_ref.fasta.7 Corrected_ref.fasta.8 Corrected_ref.fasta.9 > Corrected_ref.fasta"
```
We see that there is a very similar structure to the inputs. As join accepts a list of objects, we can follow a similar procedure to the inputs and outputs structure mentioned previously.  This list simply needs to be placed inside a join function.
```
"command": format(
	"cat %s > Corrected_ref.fasta",
	join([format("Corrected_ref.fasta.%d", x) for x in range(SPLIT_SIZE)])
)
```
When expanded, this creates an analagous string to be executed.

## JSON to JX ##

### JSON Format ###
This can be found in the file `bwa/bwa.json`

### JX Conversion ###
This can be found in the file `bwa/bwa.jx`
