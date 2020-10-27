from lark import Lark


class PropTextGenerator:
    def __init__(self):
        # defining the grammar and the tree structure
        grammar = """
        start: cmds+

        cmds: not
            | VARIABLE

        not: "not" cmds

        // one letter variable
        VARIABLE: /[a-z]/

        %import common.WS
        %ignore WS
        """
        # the variables inside the proposition
        self.variables = []
        # the tree generated from the proposition
        self.tree = None

        self.parser = Lark(grammar)
    
    def reset_values(self):
        self.variables = []
        self.tree = None

    def get_variables(self): # endpoint for testing
        return self.variables

    def parse(self, proposition):
        self.reset_values()
        self.tree = self.parser.parse(proposition)

        