import sys
import tpg

class AnalError(Exception):
    """Class of exceptions raised when an error occurs during analysis."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes."""

    # For each class of nodes, store names of the fields for children nodes.
    fields = []

    def __init__(self, *args):
        """Populate fields named in "fields" with values in *args."""
        assert(len(self.fields) == len(args))
        for f, a in zip(self.fields, args): setattr(self, f, a)

    def varnames(self, vars_defined):
        """Analyze variable names in the AST ndoe, called on all nodes."""
        raise Exception("Not implemented.")

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']
    
    def varnames(self, vars_defined):
        # print(self.name, vars_defined)
        if self.name not in vars_defined: raise AnalError()
        display('Use of variable', self.name)

class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def varnames(self, vars_defined): pass

class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    
    def varnames(self, vars_defined): 
        self.left.varnames(vars_defined)
        self.right.varnames(vars_defined)

# subclasses of Node for statements

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']
    
    def varnames(self, vars_defined): 
        self.right.varnames(vars_defined)
        if isinstance(self.left, Var):
            vars_defined.add(self.left.name)
            display('Definition of variable', self.left.name)
        else: # isinstance(self.left, Index) or otherwise # type error ignored
            self.left.varnames(vars_defined)

class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def varnames(self, vars_defined):
        for s in self.stmts: s.varnames(vars_defined)


# This is the parser using TPG for parsing FlatScript code and building an AST.
class Parser(tpg.Parser):
    r"""                                    # python raw string literals
    token int:         '\d+' ;              # 1+ (1 or more) decimal digits 
    token string:      '\"[^\"]*\"' ;       # ", then 0+ non-", then "
    token ident:       '[a-zA-Z_][\w]*' ;   # letr or _,then 0+ alphanum chars
    separator space:   '\s+' ;              # 1+ white space/tab/return chars

    START/s -> Stmt/s ;

    Stmt/s ->
      Exp/l '=(?!=)' Exp/r ';'        $ s= Assign(l, r)      # =, then not =
    | '\{'  $ s=[] $  ( Stmt/s2  $ s.append(s2) $  )* '\}'  $s= Block(s)
    ;

    Exp/e -> Mul/e;
    Mul/e -> Atom/e ( MulOp Atom/e2   $e=BinOpExp(e,MulOp,e2)$  )* ;
    Atom/e -> '\(' Exp/e '\)'
    | int/i                           $ e= Int(int(i))
    | ident                           $ e= Var(ident)
    ;

    MulOp/o -> '\*'/o | '/'/o ;
    """

def parse(code):
    # This makes a parser object, which acts as a parsing function.
    parser = Parser()
    return parser(code)


def display(*s): print(' '.join(s))


# Below is the driver code, which parses a given FlatScript program
# and analyzes the definitions and uses of variables

# Open the input file, and read in the input program.
prog = open(sys.argv[1]).read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to analyze the program.
    print('Analyzing...')
    vars_defined = set()
    node.varnames(vars_defined)

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    # raise

except AnalError as e:
    print('Analysis Error')

    # Uncomment the next line to re-raise the analysis error, 
    # displaying where the error occurs.  Comment it for submission.

    # raise
