# prop_gen
proposition table generator

# how to use
This program will become a commandline tool

the user will type the commandName (tableprop)
followed by a string as an argument

the program will print out comma separated values for the proposition you gave.

this output can be saved to a file if specified as second argument

C:/>tableprop "p and q" "and_table.csv"

# parse the proposition

I will use the lark parser to parse the proposition given to the program.

# return the variables
The different variables will be taken out of the syntax tree the lark parser gave.

# return InnerPropositions of the proposition
InnerPropositions are given and ordered by length

# return a table of possibilities
The proposition is worked out complete with inner values for inner propositions comma separated.

# testing propositions
### "not p"
output:
p,(¬p)
0,1
1,0

### "p & q"
output:
p,q,(p ∧ q)
0,0,0
0,1,0
1,0,0
1,1,1

### "p | q"
output:
p,q,(p ∨ q)
0,0,0
0,1,1
1,0,1
1,1,1

### "p & q & r"
output:
p,q,r,(p ∧ q),((p ∧ q) ∧ r)
0,0,0,0,0
0,0,1,0,0
0,1,0,0,0
0,1,1,0,0
1,0,0,0,0
1,0,1,0,0
1,1,0,1,0
1,1,1,1,1

### "not p & q & r"
output:
p,q,r,(¬p),((¬p) ∧ q),(((¬p) ∧ q) ∧ r)
0,0,0,1,0,0
0,0,1,1,0,0
0,1,0,1,1,0
0,1,1,1,1,1
1,0,0,0,0,0
1,0,1,0,0,0
1,1,0,0,0,0
1,1,1,0,0,0

## check () higher precedence in the next 2 tests

### "p & q | r"
output:
p,q,r,(p ∧ q),((p ∧ q) ∨ r)
0,0,0,0,0
0,0,1,0,1
0,1,0,0,0
0,1,1,0,1
1,0,0,0,0
1,0,1,0,1
1,1,0,1,1
1,1,1,1,1

### "p & (q | r)"
output:
p,q,r,(q ∨ r),(p ∧ ((q ∨ r)))
0,0,0,0,0
0,0,1,1,0
0,1,0,1,0
0,1,1,1,0
1,0,0,0,0
1,0,1,1,1
1,1,0,1,1
1,1,1,1,1