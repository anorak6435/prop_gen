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

# first proposition

"not p"

create a structure for the not operation.