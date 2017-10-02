# Converting JSON to JX #

## JX ##
JX is a language that simplfies and shortens interaction with the Makeflow program. At the core, JX is an extended JSON form.  It allows for the formatting of strings, for loops to iterate over a rule, list comprehension, and `join` functions to create single strings out of lists.

Additionally, external variables can be defined in an external "context" file, where lists, strings, and values can be defined for use within the JX structure.

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

### Command Reqires String of Inputs of the Same Style ###
This final example makes use of join, for and format.  Often, the different files must be concatenated into one single string for a command.  This could be a command such as the following:
```
"command" : "cat Corrected_ref.fasta.0 Corrected_ref.fasta.1 Corrected_ref.fasta.2 Corrected_ref.fasta.3 Corrected_ref.fasta.4 Corrected_ref.fasta.5 Corrected_ref.fasta.6 Corrected_ref.fasta.7 Corrected_ref.fasta.8 Corrected_ref.fasta.9 > Corrected_ref.fasta"
```
We see that there is a very simialr structure to the inputs. As join accepts a list of objects, we can follow a similar procedure to the inputs and outputs structure mentioned previously.  This list simply needs to be placed inside a join function.
```
"command": format(
	"cat %s > Corrected_ref.fasta",
	join([format("Corrected_ref.fasta.%d", x) for x in r    ange(SPLIT_SIZE)])
)
```
When expanded, this creates an analagous string to be executed.

## JSON to JX ##

### JSON Format ###
```
{
    "rules": [
        {
            "command": "./bwa index ref.fasta 2> index.err",
            "inputs": [
                "./bwa",
                "ref.fasta"
            ],
            "outputs": [
                "index.err",
                "ref.fasta.amb",
                "ref.fasta.ann",
                "ref.fasta.bwt",
                "ref.fasta.pac",
                "ref.fasta.sa"
            ],
            "local_job": true
        },
        {
            "command": "./fastq_reduce query.fastq 100",
            "inputs": [
                "./fastq_reduce",
                "query.fastq"
            ],
            "outputs": [
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
            ],
            "local_job": true
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.0 > Out.0.sam 2> mem.0.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.0"
            ],
            "outputs": [
                "Out.0.sam",
                "mem.0.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.1 > Out.1.sam 2> mem.1.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.1"
            ],
            "outputs": [
                "Out.1.sam",
                "mem.1.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.2 > Out.2.sam 2> mem.2.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.2"
            ],
            "outputs": [
                "Out.2.sam",
                "mem.2.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.3 > Out.3.sam 2> mem.3.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.3"
            ],
            "outputs": [
                "Out.3.sam",
                "mem.3.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.4 > Out.4.sam 2> mem.4.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.4"
            ],
            "outputs": [
                "Out.4.sam",
                "mem.4.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.5 > Out.5.sam 2> mem.5.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.5"
            ],
            "outputs": [
                "Out.5.sam",
                "mem.5.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.6 > Out.6.sam 2> mem.6.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.6"
            ],
            "outputs": [
                "Out.6.sam",
                "mem.6.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.7 > Out.7.sam 2> mem.7.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.7"
            ],
            "outputs": [
                "Out.7.sam",
                "mem.7.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.8 > Out.8.sam 2> mem.8.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.8"
            ],
            "outputs": [
                "Out.8.sam",
                "mem.8.err"
            ]
        },
        {
            "command": "./bwa mem ref.fasta query.fastq.9 > Out.9.sam 2> mem.9.err",
            "inputs": [
                "./bwa",
                [
                    "ref.fasta.amb",
                    "ref.fasta.ann",
                    "ref.fasta.bwt",
                    "ref.fasta.pac",
                    "ref.fasta.sa"
                ],
                "query.fastq.9"
            ],
            "outputs": [
                "Out.9.sam",
                "mem.9.err"
            ]
        },
        {
            "command": "./sam_cat.sh Out.0.sam Out.1.sam Out.2.sam Out.3.sam Out.4.sam Out.5.sam Out.6.sam Out.7.sam Out.8.sam Out.9.sam > Out.sam",
            "inputs": [
                "./sam_cat.sh",
                "Out.0.sam",
                "Out.1.sam",
                "Out.2.sam",
                "Out.3.sam",
                "Out.4.sam",
                "Out.5.sam",
                "Out.6.sam",
                "Out.7.sam",
                "Out.8.sam",
                "Out.9.sam"
            ],
            "outputs": [
                "Out.sam"
            ],
            "local_job": true
        },
        {
            "command": "cat mem.*.err > mem.err",
            "inputs": [
                "mem.0.err",
                "mem.1.err",
                "mem.2.err",
                "mem.3.err",
                "mem.4.err",
                "mem.5.err",
                "mem.6.err",
                "mem.7.err",
                "mem.8.err",
                "mem.9.err"
            ],
            "outputs": [
                "mem.err"
            ],
            "local_job": true
        },
        {
            "command": "./samtools view -bS Out.sam | ./samtools sort - Out 2> sort.err",
            "inputs": [
                "./samtools",
                "Out.sam"
            ],
            "outputs": [
                "Out.bam",
                "sort.err"
            ]
        },
        {
            "command": "./samtools mpileup -s -f ref.fasta Out.bam > pileup.txt 2> pileup.err",
            "inputs": [
                "./samtools",
                "ref.fasta",
                "Out.bam"
            ],
            "outputs": [
                "pileup.txt",
                "ref.fasta.fai",
                "pileup.err"
            ]
        },
        {
            "command": "./Split_Pileup.sh pileup.txt 2 2> Split_Pileup.err",
            "inputs": [
                "./Split_Pileup.sh",
                "Create_SubsetPileup.sh",
                "pileup.txt"
            ],
            "outputs": [
                "Pileup_Set1.txt",
                "Pileup_Set2.txt",
                "List_RefHeader.txt"
            ],
            "local_job": true
        },
        {
            "command": "python Correction.py Pileup_Set0.txt ref.fasta lc.0.out Out.sam 100 > corr.0.out 2> corr.0.err ; echo \"\" >> lc.0.out ; echo \"\" >> corr.0.out",
            "inputs": [
                "Correction.py",
                "Pileup_Set1.txt",
                "ref.fasta",
                "Out.sam"
            ],
            "outputs": [
                "corr.0.out",
                "lc.0.out",
                "corr.0.err"
            ],
            "local_job": true
        },
        {
            "command": "python Correction.py Pileup_Set1.txt ref.fasta lc.1.out Out.sam 100 > corr.1.out 2> corr.1.err ; echo \"\" >> lc.1.out ; echo \"\" >> corr.1.out",
            "inputs": [
                "Correction.py",
                "Pileup_Set2.txt",
                "ref.fasta",
                "Out.sam"
            ],
            "outputs": [
                "corr.1.out",
                "lc.1.out",
                "corr.1.err"
            ],
            "local_job": true
        },
        {
            "command": "cat corr.0.out corr.1.out > corr.out",
            "inputs": [
                "corr.0.out",
                "corr.1.out"
            ],
            "outputs": [
                "corr.out"
            ],
            "local_job": true
        },
        {
            "command": "cat corr.0.err corr.1.err > corr.err",
            "inputs": [
                "corr.0.err",
                "corr.1.err"
            ],
            "outputs": [
                "corr.err"
            ],
            "local_job": true
        },
        {
            "command": "cat lc.0.out lc.1.out > LowConf.txt",
            "inputs": [
                "lc.0.out",
                "lc.1.out"
            ],
            "outputs": [
                "LowConf.txt"
            ],
            "local_job": true
        },
        {
            "command": "./fasta_reduce ref.fasta 1000",
            "inputs": [
                "./fasta_reduce",
                "ref.fasta"
            ],
            "outputs": [
                "ref.fasta.0",
                "ref.fasta.1",
                "ref.fasta.2",
                "ref.fasta.3",
                "ref.fasta.4",
                "ref.fasta.5",
                "ref.fasta.6",
                "ref.fasta.7",
                "ref.fasta.8",
                "ref.fasta.9"
            ],
            "local_job": true
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.0 corr.out 2> create.err.0",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.0"
            ],
            "outputs": [
                "Corrected_ref.fasta.0"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.1 corr.out 2> create.err.1",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.1"
            ],
            "outputs": [
                "Corrected_ref.fasta.1"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.2 corr.out 2> create.err.2",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.2"
            ],
            "outputs": [
                "Corrected_ref.fasta.2"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.3 corr.out 2> create.err.3",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.3"
            ],
            "outputs": [
                "Corrected_ref.fasta.3"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.4 corr.out 2> create.err.4",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.4"
            ],
            "outputs": [
                "Corrected_ref.fasta.4"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.5 corr.out 2> create.err.5",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.5"
            ],
            "outputs": [
                "Corrected_ref.fasta.5"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.6 corr.out 2> create.err.6",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.6"
            ],
            "outputs": [
                "Corrected_ref.fasta.6"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.7 corr.out 2> create.err.7",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.7"
            ],
            "outputs": [
                "Corrected_ref.fasta.7"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.8 corr.out 2> create.err.8",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.8"
            ],
            "outputs": [
                "Corrected_ref.fasta.8"
            ]
        },
        {
            "command": "python Create_Corrected_AllLRReads.py ref.fasta.9 corr.out 2> create.err.9",
            "inputs": [
                "Create_Corrected_AllLRReads.py",
                "corr.out",
                "ref.fasta.9"
            ],
            "outputs": [
                "Corrected_ref.fasta.9"
            ]
        },
        {
            "command": "cat Corrected_ref.fasta.0 Corrected_ref.fasta.1 Corrected_ref.fasta.2 Corrected_ref.fasta.3 Corrected_ref.fasta.4 Corrected_ref.fasta.5 Corrected_ref.fasta.6 Corrected_ref.fasta.7 Corrected_ref.fasta.8 Corrected_ref.fasta.9 > Corrected_ref.fasta",
            "inputs": [
                "Corrected_ref.fasta.0",
                "Corrected_ref.fasta.1",
                "Corrected_ref.fasta.2",
                "Corrected_ref.fasta.3",
                "Corrected_ref.fasta.4",
                "Corrected_ref.fasta.5",
                "Corrected_ref.fasta.6",
                "Corrected_ref.fasta.7",
                "Corrected_ref.fasta.8",
                "Corrected_ref.fasta.9"
            ],
            "outputs": [
                "Corrected_ref.fasta"
            ],
            "local_job": true
        }
    ]
}
```

### JX Conversion ###
```
{"rules": [
	{
		"command": format(
			"%s index %s 2> index.err",
			BWA,
			REF,
		),
		"inputs": [
			BWA,
			REF,
		],
		"outputs": [
			"index.err",
			x for x in REF_INDEX,
		],
		"local_job": true,
	},
	{
		"command": format(
			"%s %s %d",
			SPLIT,
			INPUT_PRE,
			SPLITS,
		),
		"inputs": [
			SPLIT,
			INPUT_PRE,
		],
		"outputs":[
			format("%s.%d", INPUT_PRE, x) for x in range(SPLIT_SIZE),
		],
		"local_job": true,
	},
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
			[x for x in REF_INDEX],
			format("%s.%d", INPUT_PRE, i),
		],
		"outputs": [
			format("Out.%d.sam", i),
			format("mem.%d.err", i),
		]
	} for i in range(SPLIT_SIZE),
	{
		"command": format(
			"%s %s > Out.sam",
			CONCAT,
			join([format("Out.%d.sam", x) for x in range(SPLIT_SIZE)])
		),
		"inputs": [
			CONCAT,
			format("Out.%d.sam", x) for x in range(SPLIT_SIZE),
		],
		"outputs": [
			"Out.sam"
		],
		"local_job": true,
	},
	{
		"command": format(
			"cat mem.*.err > mem.err"
		),
		"inputs": [
			format("mem.%d.err", x) for x in range(SPLIT_SIZE),
		],
		"outputs": [
			"mem.err",
		],
		"local_job": true,
	},
	{
		"command": format(
			"%s view -bS Out.sam | %s sort - Out 2> sort.err",
			TOOLS,
			TOOLS,
		),
		"inputs": [
			TOOLS,
			"Out.sam",
		],
		"outputs": [
			"Out.bam",
			"sort.err",
		]
	},
	{
		"command": format(
			"%s mpileup -s -f %s Out.bam > pileup.txt 2> pileup.err",
			TOOLS,
			REF,
		),
		"inputs": [
			TOOLS,
			REF,
			"Out.bam",
		],
		"outputs": [
			"pileup.txt",
			"ref.fasta.fai",
			"pileup.err"
		],
	},
	{
		"command": format(
			"%s pileup.txt 2 2> Split_Pileup.err",
			PILEUP,
		),
		"inputs": [
			PILEUP,
			CREATE_PILEUP,
			"pileup.txt",
		],
		"outputs": [
			format("Pileup_Set%d.txt", x) for x in range(1,3),
			"List_RefHeader.txt",
		],
		"local_job": true,
	},
	{
		"command": format(
			"%s %s Pileup_Set%d.txt %s lc.%d.out Out.sam %d > corr.%d.out 2> corr.%d.err ; echo \"\" >> lc.%d.out ; echo \"\" >> corr.%d.out",
			PYTHON,
			CORRECTION,
			x,
			REF,
			x,
			SPLITS,
			x,
			x,
			x,
			x,
		),
		"inputs": [
			CORRECTION,
			format("Pileup_Set%d.txt", x+1),
			REF,
			"Out.sam",
		],
		"outputs": [
			format("corr.%d.out", x),
			format("lc.%d.out", x),
			format("corr.%d.err", x),
		],
		"local_job": true,
	} for x in range(2),
	{
		"command": format(
			"cat %s > corr.out",
			join([format("corr.%d.out", x) for x in range(2)])
		),
		"inputs": [
			format("corr.%d.out", x) for x in range(2),
		],
		"outputs": [
			"corr.out",
		],
		"local_job": true,
	},
	{
		"command": format(
			"cat %s > corr.err",
			join([format("corr.%d.err", x) for x in range(2)])
		),
		"inputs": [
			format("corr.%d.err", x) for x in range(2),
		],
		"outputs": [
			"corr.err",
		],
		"local_job": true,
	},
	{
		"command": format(
			"cat %s > LowConf.txt",
			join([format("lc.%d.out", x) for x in range(2)])
		),
		"inputs": [
			format("lc.%d.out", x) for x in range(2),
		],
		"outputs": [
			"LowConf.txt",
		],
		"local_job": true,
	},
	{
		"command": format(
			"%s %s 1000",
			SPLITA,
			REF,
		),
		"inputs": [
			SPLITA,
			REF,
		],
		"outputs": [
			format("%s.%d", REF, x) for x in range(SPLIT_SIZE),
		],
		"local_job": true,
	},
	{
		"command": format(
			"%s %s %s.%d corr.out 2> create.err.%d",
			PYTHON,
			CORRECT_ALLLR,
			REF,
			x,
			x,
		),
		"inputs": [
			CORRECT_ALLLR,
			"corr.out",
			format("%s.%d", REF, x),
		],
		"outputs": [
			format("Corrected_ref.fasta.%d", x),
		],
	} for x in range(SPLIT_SIZE),
	{
		"command": format(
			"cat %s > Corrected_ref.fasta",
			join([format("Corrected_ref.fasta.%d", x) for x in range(SPLIT_SIZE)])
		),
		"inputs": [
			format("Corrected_ref.fasta.%d", x) for x in range(SPLIT_SIZE),
		],
		"outputs": [
			"Corrected_ref.fasta",
		],
		"local_job": true,
	},
],
}
```
