# contains the different tree nodes for the operations neccesary in the files
class Operation:
    def __eq__(self, other):
        return repr(self) == repr(other)

class OP_NOT(Operation):
    def __init__(self, value):
        self.value = value

    def execute(self, state):
        return not self.value.execute(state)
    
    def __repr__(self):
        return f"(¬{self.value})"

class OP_AND(Operation):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self, state):
        return self.left.execute(state) and self.right.execute(state)
    
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class OP_OR(Operation):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self, state):
        return self.left.execute(state) or self.right.execute(state)
    
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class OP_IMPLY(Operation):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} -> {self.right})"

    def execute(self, state):
        return not self.left.execute(state) or self.right.execute(state)

class OP_BICOND(Operation):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} <=> {self.right})"
    
    def execute(self, state):
        a = self.left.execute(state)
        b = self.right.execute(state)
        return a and b or not a and not b

class OP_PAREN:
    def __init__(self, value):
        self.value = value
    
    def execute(self, state):
        return self.value.execute(state)

    def __repr__(self):
        return f"({self.value})"

# represent variables
class OP_VAR(Operation):
    def __init__(self, value):
        self.value = value
    
    def execute(self, state):
        return state[repr(self)]

    def __repr__(self):
        return self.value