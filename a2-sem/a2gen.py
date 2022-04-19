import sys
import tpg


DEBUG=False

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

    def convert(self, store):
        return self.name
    
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def eval(self, store): return self.value

    def convert(self, store):
        return str(self.value)

class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']

    def convert(self, store):
        return '"' + self.value + '"'
    
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

    def convert(self, store):
        ret = '{'
        for elem in self.elements:
            ret += elem.convert(store)
            ret += ','
        ret += '}'
        return ret.replace(',}', '}')

class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']

    def convert(self, store):
        return "{indexable}[{index}]".format(indexable = self.indexable.convert(store),\
            index = self.index.convert(store))

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

    def convert(self, store):
        ret = "{left} {op} {right}".format(left = self.left.convert(store), \
            op = self.op, right = self.right.convert(store))

        return ret

class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

    def convert(self, store):
        if self.op == "not":
            return "!({arg})".format(arg = self.arg.convert(store))

# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

    def exec(self, store):
        print(repr(self.exp.eval(store)))

    def convert(self, store):
        return "Console.WriteLine({exp})".format(exp = self.exp.convert(store))

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']

    def convert(self, store):

        rval = self.right.convert(store)
        
        if isinstance(self.left, Var):
            
            if self.left.name in store:
                return "{left} = {right}".format( left=self.left.convert(store),\
                    right=rval)
            
            # declare the variable
            store[self.left.name] = rval
            
            if isinstance(self.right, Int) or isinstance(self.right, Index):
                ret = "{dtype} {left} = {right}".format(dtype = "int", \
                    left=self.left.convert(store), right=rval)
            
            elif isinstance(self.right, Array):
                ret = "{dtype} {left} = {right}".format(dtype = "int []", \
                    left = self.left.convert(store), right=rval)

            return ret
        
        elif isinstance(self.left, Index):
            arr = self.left.indexable

            while isinstance(arr, Index):
                arr = arr.indexable
            
            if arr.name in store:
                return "{left} = {right}".format(left = self.left.convert(store),\
                    right = rval)
            raise EvalError()
        
    
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def convert(self, store):
        ret = ""
        for st in self.stmts:
            if isinstance(st, If) or isinstance(st, While):
                ret = ret + st.convert(store) + "\n";
            else:
                ret = ret + st.convert(store) + ";\n"
        return ret

class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

    def convert(self, store):
        return "if ( {expr} ) \n {{ \n {stmts} \n }}".format(expr = \
            self.exp.convert(store), stmts = self.stmt.convert(store))

class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

    def convert(self, store):
        return "while ( {expr} ) \n {{\n {stmts} \n}}".format(expr = \
            self.exp.convert(store), stmts = self.stmt.convert(store))



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
    program = node.convert(global_store)
    if DEBUG:
        print(global_store)


    template = "using System;\npublic class Program {\n\
    public static void Main() {\n"

    program = template + program + "}\n}"

    with open(sys.argv[2], "w") as output:
        output.write(program)


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
