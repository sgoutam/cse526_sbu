#! /usr/bin/python3

"""

_author_ : Sanket Goutam

"""

import sys
import tpg
from pprint import pprint

DEBUG = False

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
        if DEBUG:
            print("print Node: ", self, "-->", args)

        for f, a in zip(self.fields, args): setattr(self, f, a)

    def varnames(self, vars_defined):
        """Analyze variable names in the AST node, called on all nodes."""
        raise Exception("Not implemented.")

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']
    
    def varnames(self, vars_defined):
        #print(self.name, vars_defined)
        if self.name not in vars_defined: 
            #print(self.name, 'not in ', vars_defined)
            raise AnalError()
        display('Use of variable', self.name)

class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def varnames(self, vars_defined): pass

class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']

    def varnames(self, vars_defined): pass

class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['value']

    def __init__(self, *args):
        super(Array, self).__init__(*args)

    def varnames(self, vars_defined): pass

class ArrayIndex(Node):
    """Class to handle array indexing operations"""
    fields = ['a_name', 'a_index']

    def __init__(self, *args):
        super(ArrayIndex, self).__init__(*args)

    def varnames(self, vars_defined):
        self.a_name.varnames(vars_defined)
        self.a_index.varnames(vars_defined)


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
            #print(vars_defined)
            display('Definition of variable', self.left.name)
        else: # isinstance(self.left, Index) or otherwise # type error ignored
            self.left.varnames(vars_defined)

class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def varnames(self, vars_defined):
        for s in self.stmts: s.varnames(vars_defined)

class CtrlStmt(Node):
    """Statements representing While/If blocks"""
    fields = ['expr','stmts']
    
    def varnames(self, vars_defined):
        self.expr.varnames(vars_defined)
        self.stmts.varnames(vars_defined)

class Comment(Node):
    """Class of nodes representing comments"""
    fields = []

    def varnames(self, vars_defined): 
        if DEBUG: display('Comment block')
        pass

class CreateFunc(Node):
    """Class of nodes representing function definitions."""
    fields = ['params', 'stmt']

    def __init__(self, *args):
        super(CreateFunc, self).__init__(*args)


    def varnames(self, vars_defined):
        func_name, param = self.params[0], self.params[1:]
        #print(func_name, param, self.stmt)
        
        for val in vars_defined:
            if type(val) is tuple:
                if val[0] == "FuncName" and val[1] == func_name:
                    # function already defined before
                    raise AnalError
        
        local_vars = set(param)
        if hasattr(self.stmt, 'stmts'):
            # def func(args) : { stmts ... }
            for statement in self.stmt.stmts:
                #print("Statement: ", statement, param)
                statement.varnames(local_vars)
        else:
            # def func(args) 
            #print("self statement ", self.stmt)
            self.stmt.varnames(local_vars)
            
        # add function to Global scope
        func_ = ("FuncName", func_name, tuple(param), self.stmt)
        vars_defined.add(func_)
        if DEBUG:
            print("vars_defined ", vars_defined)

        display('Definition of proceduce ', func_name)
        display('Locals of procedure ', func_name, ': ', ", ".join(param))


class CallFunc(Node):
    """Class of nodes representing function calls."""
    fields =['params']

    def __init__(self, *args):
        super(CallFunc, self).__init__(*args)

    def varnames(self, vars_defined):
        func_name, param = self.params[0], self.params[1:]

        # check if func_name is defined, AnalError if not defined
        f_defined = False
        func_def = None

        for var in vars_defined:
            if type(var) is tuple:
                if var[0] == "FuncName" and var[1] == func_name:
                    f_defined = True
                    func_def = var
                    break
        if not f_defined:
            raise AnalError
        
        display('Call of procedure ', func_name)

        # shadow variables
        for temp in param:
            if isinstance(temp,Var):
                if temp.name in func_def[2]:
                    display('Shadowing of global variable ', temp.name)

# This is the parser using TPG for parsing FlatScript code and building an AST.
class Parser(tpg.VerboseParser):
    r"""                                    # python raw string literals
    token int:         '\d+' ;              # 1+ (1 or more) decimal digits 
    token string:      '\"[^\"]*\"' ;       # ", then 0+ non-", then "
    
    # Placing keywords here to prevent usage as identifiers
    
    token controlStmt:      '(if|while)\b';
    token printStmt:        'print\b';
    token negate:           'not\b';
    token And:              'and\b';
    token Or:               'or\b';

    token ident:       '[a-zA-Z_][\w]*' ;   # letr or _,then 0+ alphanum chars
    separator space:   '\s+' ;              # 1+ white space/tab/return chars
    
    START/s -> Stmt/s ;

    Stmt/s ->
      Exp/l '=(?!=)' Exp/r ';'          $ s= Assign(l, r)      # =, then not =
    | '\{'  $ s=[] $  ( Stmt/s2  $ s.append(s2) $  )* '\}'  $s= Block(s)
    | controlStmt '\(' Exp/e '\)' Stmt/s    $ s = CtrlStmt(e,s)
    | printStmt Exp/s ';' 
    | '#.*\s'                           $ s=Comment()
    | ProcDef/s
    | ProcCall/s
    ;


    Exp/e ->  IndexOp/e | ArrayOp/e | Term/e  ;      # order decides precedence
    
    
    # all operations in order of precedence

    Term/e ->  Add/e (MulOp Add/e2      $e=BinOpExp(e,MulOp,e2)$ )* ;   # Multiply
    Add/e -> Rel/e (AddOp Rel/e2        $e=BinOpExp(e,AddOp,e2)$ )* ;   # Add
    Rel/e -> Neg/e (RelOp Neg/e2        $e=BinOpExp(e,RelOp,e2)$ )* ;   # Compare
    Neg/e -> (negate)* Log/e;                                           # Negate
    Log/e -> Atom/e ( LogOp Atom/e2     $e=BinOpExp(e,LogOp,e2)$ )* ;   # Logical
    

    Atom/e -> '\(' Exp/e '\)'
    | int/i                             $ e= Int(int(i))
    | ident                             $ e= Var(ident)
    | string/e                          $ e= String(e)
    ;

    ArrayOp/l -> 
            '\['                        $ l = []
                Exp/e                   $ l.append(e)
                ( ',' Exp/e2            $ l.append(e2)               # nested array
                )* 
            '\]'                        $ l = Array(l)
            ;

    IndexOp/e -> ident/e1 $e=Var(e1) 
                ('\[' Exp/e2 '\]'       $e=ArrayIndex(e,e2) 
                )+ 
            ;

    ProcDef/e -> 'def' ident/e1         $fargs=[e1]                    
                '\(' (ident/e2          $fargs.append(e2) 
                )? (',' ident/e3        $fargs.append(e3) 
                )* '\)' Stmt/s2         $e= CreateFunc(fargs, s2) 
                ; 

    ProcCall/e ->  ident/e1             $fargs=[e1] 
                '\(' (Term/e2           $fargs.append(e2) 
                )? (',' Term/e3         $fargs.append(e3) 
                )* '\)' ';'             $e= CallFunc(fargs) 
                ;

    MulOp/o -> '\*'/o | '/'/o ;
    AddOp/o -> '\+'/o | '\-'/o;
    RelOp/o -> '\>'/o | '\<'/o | '\=\='/o | '\>\='/o | '\<\='/o;
    LogOp/o ->  And/o | Or/o;
    """

    if DEBUG: 
        verbose = 2
    else:
        verbose = 0



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

    if DEBUG: raise

except AnalError as e:
    print('Analysis Error')

    # Uncomment the next line to re-raise the analysis error, 
    # displaying where the error occurs.  Comment it for submission.

    if DEBUG: raise
