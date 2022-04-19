import sys
import tpg

class EvalError(Exception):
    """Class of exceptions raised when an error occurs during evaluation."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes."""

    # For each class of nodes, store names of the fields for children nodes.
    fields = []

    def __init__(self, *args):
        """Populate fields named in "fields" with values in *args."""
        assert(len(self.fields) == len(args))
        for f, a in zip(self.fields, args): setattr(self, f, a)

    def eval(self, store):
        """Evaluate the AST node, called on nodes of expression subclasses."""
        raise Exception("Not implemented.")

    def exec(self, store):
        """Evaluate the AST node, called on nodes of statement subclasses.
        """
        raise Exception("Not implemented.")

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']
    
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def eval(self, store): return self.value

class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']
    
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']

class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    
    def eval(self, store):
        v1 = self.left.eval(store)
        v2 = self.right.eval(store)

        if self.op == '+': 
            if isinstance(v1,int) and isinstance(v2,int): return v1 + v2
            if isinstance(v1,str) and isinstance(v2,str): return v1 + v2
            raise EvalError()

class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

    def exec(self, store):
        print(repr(self.exp.eval(store)))

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']
    
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']

class Call(Node):
    """Class of nodes representing precedure calls."""
    fields = ['name', 'args']


# This is the parser using TPG for parsing FlatScript code and building an AST.
class Parser(tpg.Parser):
    r"""
    token int:         '\d+' ;
    token string:      '\"[^\"]*\"' ;
    token ident:       '[a-zA-Z_][\w]*' ;
    separator space:   '\s+' ;
    separator comment: '#.*' ;

    START/s -> Stmt/s ;

    Stmt/s ->
    ( 'print' Exp/e ';'               $s = Print(e)$
    | Exp/l '=(?!=)' Exp/r ';'        $ s = Assign(l, r) $
    | '\{'  $ s=[] $  ( Stmt/s2  $ s.append(s2) $  )* '\}'  $s = Block(s)$
    | 'if' '\(' Exp/e '\)' Stmt/s     $ s = If(e, s) $
    | 'while' '\(' Exp/e '\)' Stmt/s  $ s = While(e, s) $
    ) ;

    Exp/e -> Or/e ;
    Or/e  -> And/e ( 'or'  And/e2  $e=BinOpExp(e,'or', e2)$  )* ;
    And/e -> Not/e ( 'and' Not/e2  $e=BinOpExp(e,'and',e2)$  )* ;
    Not/e -> 'not' Not/e  $e=UniOpExp('not', e)$  | Cmp/e ;
    Cmp/e -> Add/e ( CmpOp Add/e2  $e=BinOpExp(e,CmpOp,e2)$  )* ;
    Add/e -> Mul/e ( AddOp Mul/e2  $e=BinOpExp(e,AddOp,e2)$  )* ; 
    Mul/e -> Index/e ( MulOp Index/e2  $e=BinOpExp(e,MulOp,e2)$  )* ;
    Index/e -> Atom/e ( '\[' Exp/e2 '\]'  $e=Index(e,e2)$  )* ;
    Atom/e -> '\(' Exp/e '\)'
    | int/i     $e=Int(int(i))$
    | string/s  $e=String(s[1:-1])$
    | '\['  $e=[]$  ( Exp  $e.append(Exp)$  ( ',' Exp  $e.append(Exp)$  )*)?
      '\]'  $e=Array(e)$
    | ident     $e=Var(ident)$
    ;
    CmpOp/o -> '=='/o | '<'/o | '>'/o ;
    AddOp/o -> '\+'/o | '-'/o ;
    MulOp/o -> '\*'/o | '/'/o ;
    """

def parse(code):
    # This makes a parser object, which acts as a parsing function.
    parser = Parser()
    return parser(code)


# Below is the driver code, which parses a given FlatScript program,
# and executes the program.

# Open the input file, and read in the input program.
prog = open(sys.argv[1]).read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to execute the program.
    print('Executing...')
    # global_store: map from global variable names to their values
    global_store = dict()
    node.exec(global_store)

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    # raise

except EvalError:
    print('Evaluation Error')

    # Uncomment the next line to re-raise the evaluation error, 
    # displaying where the error occurs.  Comment it for submission.

    # raise
