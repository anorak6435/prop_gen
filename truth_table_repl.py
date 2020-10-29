from lark import Lark, Visitor, Tree, Token
from lark.visitors import Interpreter
import sys
DEBUG = False

# get the grammar
with open("grammar.lark", 'r') as file:
    grammar = file.read()
# make the parser from the grammar
parser = Lark(grammar)

def parse(in_string):
    return parser.parse(in_string)

def list_all_operations(ast):
    get_operations.operations = [] # clear the operations list before starting
    ops = get_operations.visit(ast)
    if DEBUG:
        print("top level operations:")
        print(ops)
    return get_operations.operations
    
# the operations
class OP_NOT:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return repr(self) == repr(other)

    def execute(self, state):
        return not self.value.execute(state)
    
    def __repr__(self):
        return f"(¬{self.value})"

class OP_AND:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return repr(self) == repr(other)

    def execute(self, state):
        return self.left.execute(state) and self.right.execute(state)
    
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class OP_OR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return repr(self) == repr(other)

    def execute(self, state):
        return self.left.execute(state) or self.right.execute(state)
    
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class OP_IMPLY:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return f"({self.left} -> {self.right})"

    def execute(self, state):
        return not self.left.execute(state) or self.right.execute(state)

class OP_PAREN:
    def __init__(self, value):
        self.value = value
    
    def execute(self, state):
        return self.value.execute(state)

    def __repr__(self):
        return f"({self.value})"

# represent the variables I find
class OP_VAR:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return repr(self) == repr(other)
    
    def execute(self, state):
        return state[repr(self)]

    def __repr__(self):
        return self.value

# get the operations from the ast
class get_operations:
    operations = [] # static list of operations
    
    def visit(tree):
        if DEBUG:
            print(f"step--{tree}")
            print(f"type:{type(tree)}")
            print(f"children:{len(tree.children)}")
        if isinstance(tree, Tree):
            # rule matches that propagate the visitor down to the actual rules / operations
            if tree.data == "start":
                return get_operations.visit(tree.children[0])
            if tree.data == "orexpr":
                return get_operations.visit(tree.children[0])
            if tree.data == "andexpr":
                return get_operations.visit(tree.children[0])
            if tree.data == "notexpr":
                return get_operations.visit(tree.children[0])
            if tree.data == "implyexpr":
                return get_operations.visit(tree.children[0])
            # return the value of the variable to the last operation
            if tree.data == "variable":
                opvar = OP_VAR(tree.children[0].value)
                if not opvar in get_operations.operations:
                    get_operations.operations.append(opvar)
                return opvar
            # the operations
            if tree.data == "not":
                opnot = OP_NOT(get_operations.visit(tree.children[0]))
                if not opnot in get_operations.operations:
                    get_operations.operations.append(opnot)
                return opnot
            if tree.data == "and":
                opand = OP_AND(get_operations.visit(tree.children[0]), get_operations.visit(tree.children[1]))
                if not opand in get_operations.operations:
                    get_operations.operations.append(opand)
                return opand
            if tree.data == "or":
                opor = OP_OR(get_operations.visit(tree.children[0]), get_operations.visit(tree.children[1]))
                if not opor in get_operations.operations:
                    get_operations.operations.append(opor)
                return opor
            if tree.data == "imply":
                opimply = OP_IMPLY(get_operations.visit(tree.children[0]), get_operations.visit(tree.children[1]))
                if not opimply in get_operations.operations:
                    get_operations.operations.append(opimply)
                return opimply
            if tree.data == "parentesis":
                paren = OP_PAREN(get_operations.visit(tree.children[0]))
                return paren

def filter_variable_type(op):
    return isinstance(op, OP_VAR)

# class that represents the table
class Table:
    def __init__(self, operations):
        self.header = operations
        self.variables = list(filter(filter_variable_type, operations)) # return the variables from the operations
        if DEBUG:
            print(self.variables)

    def generate_csv(self):
        # the header of the table
        temp_els = ",".join([repr(el) for el in self.header])
        file_contents = temp_els + "\n"

        # the generation of a state
        # make the booleans for the variables
        bin_repr = f"0{len(self.variables)}b"
        for index in range(2 ** len(self.variables)):
            bin_state_string = format(index, bin_repr)
            bool_list = [c == "1" for c in bin_state_string]

            # A state will be a dict that has a boolean value linked to the variables
            state = {}
            for var_index in range(len(self.variables)):
                state[repr(self.variables[var_index])] = bool_list[var_index]
            if DEBUG:
                print(index, state)

            # for every state execute all operations in the table header
            computed_state = ["1" if op.execute(state) else "0" for op in self.header]
            
            # print a csv row
            computed_state = ",".join(computed_state)
            
            file_contents += computed_state + "\n"
        return file_contents
        



# get the input
if len(sys.argv) >= 2:
    proposition = sys.argv[1] # the first argument after the program name should be the proposition
else:
    print("The propositon was not defined!")
    quit()

# make the tree
ast = parse(proposition)
if DEBUG:
    print("AST pretty version (check priority)")
    print(ast.pretty())
    print("AST obj version (if unusual)")
    print(ast)

# operations
operations = list_all_operations(ast)
# filter operations based on length
operations = sorted(operations, key=lambda op: len(repr(op)))
if DEBUG:
    print("operations breakdown:")
    for op in operations:
        print(op)

# create the table
my_table = Table(operations)

csv_contents = my_table.generate_csv()


if len(sys.argv) >= 3:
    file_name = sys.argv[2] # the first argument after the program name should be the proposition
    bestand = open(file_name, "w", encoding="utf-8")
    bestand.write(csv_contents)
    bestand.close()

print(csv_contents, end="")