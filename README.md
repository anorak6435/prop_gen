# prop_gen
proposition table generator

# how to use
This program will become a commandline tool

the user will type the commandName (tableprop)
followed by a string as an argument

the program will print out comma separated values for the proposition you gave.

this output can be piped in the command line into a .csv file.

C:/>tableprop "p and q" > and_table.csv

# parse the proposition

I will use the lark parser to parse the proposition given to the program.

# return the variables
The different variables will be taken out of the syntax tree the lark parser gave.

# return InnerPropositions of the proposition
InnerPropositions are given and ordered by length

# return a table of possibilities
variables InnerPropositions and the full propositions are together inside a list.
A list of options for the variables is generated.

# print options to the screen
foreach of the options in the options list the structures are computed. the returnvalues are comma separated and printed to the screen. 

# first proposition

"not p"

create a structure for the not operation.