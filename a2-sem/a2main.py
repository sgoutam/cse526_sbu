#! /usr/bin/python3

"""

_author_ : Sanket Goutam

"""

import sys
import tpg
import copy

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

    def eval(self, store):
        # return the value stored for each variable
        if store["mode"] == "pre-pass":
            return
        
        if DEBUG:
            print(self.__class__.__name__, store, self.name)

        if self.name in store:
            return store[self.name]

        raise EvalError()

class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    
    def eval(self, store): 
        if store["mode"] == "pre-pass":
            return
        
        return self.value

class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']

    def eval(self, store): 
        if store["mode"] == "pre-pass":
            return
        
        return self.value
    
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']

    def eval(self, store):
        """ Create an array with elements """
        if store["mode"] == "pre-pass":
            return
        
        arr = []
        if DEBUG:
            print(self.__class__.__name__, store)

        for elem in self.elements:
            obj = elem.eval(store)
            arr.append(obj)
        return arr


class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']


    """ 
    Indexing: The index b must be an integer, and the indexable a must be 
    a string or an array. 
    The index starts at 0 for the first element, and must not be out of 
    bound. If a is a string, the b-th character of the string is returned 
    as a string. If a is an array, the b-th element 
    of the array is returned.
    """
    def eval(self, store):
        if store["mode"] == "pre-pass":
            return
        
        b = self.index.eval(store)
        if isinstance(self.indexable, Var):
            a = self.indexable.name
            if a in store and b < len(store[a]):
                return store[a][b]
            else:
                raise EvalError()    
        elif isinstance(self.indexable, Index):
            # for arr[][], indexable will itself be an Index node
            arr = self.indexable.indexable
            while isinstance(arr, Index):
                arr = arr.indexable     # get the deepest nested node
            
            if arr.name in store:
                result = []
                for a in store[arr.name]:
                    if b < len(a):
                        result.append(a[b])
                    else:
                        raise EvalError()

                store_cp = copy.deepcopy(store)
                store_cp[arr.name] = result
                return self.indexable.eval(store_cp)
            else:
                raise EvalError() 

class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    
    def eval(self, store):
        if store["mode"] == "pre-pass":
            return
        
        v1 = self.left.eval(store)
        v2 = self.right.eval(store)
            
        if self.op == '+': 
            if isinstance(v1,int) and isinstance(v2,int): return v1 + v2
            if isinstance(v1,str) and isinstance(v2,str): return v1 + v2
            raise EvalError()
        
        if isinstance(v1,int) and isinstance(v2,int):

            # Subtraction, multiplication, and division: 
            # Both arguments must be integers. 
            if self.op == '-':
                return v1 - v2

            elif self.op == '*':
                return v1 * v2

            # For division, b must not be 0. 
            # The result of a division is rounded down to the nearest integer
            elif self.op == '/':
                if v2 != 0:
                    return int(round(v1/v2))
                else:
                    raise EvalError()

            # Comparison: Both arguments must be integers. 
            # The two integers are compared, and the result is 1 if the 
            # comparison is true, and 0 otherwise.
            elif self.op == '<':
                return (1 if v1 < v2 else 0)
            
            elif self.op == '>':
                return (1 if v1 > v2 else 0)

            elif self.op == '==':
                return (1 if v1 == v2 else 0)

            # Conjunction, disjunction, and negation: The arguments must be integers. 
            # 0 is considered false. All other integers are true. 
            elif self.op == 'and':
                return int(v1 and v2)
            
            elif self.op == 'or':
                return int(v1 or v2)
            
        else:
            # operation not supported
            raise EvalError()

class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']

    def eval(self, store):
        # The Boolean operation is performed. The result is 1 if the 
        # Boolean operation is true, and 0 otherwise.
        if store["mode"] == "pre-pass":
            return
        
        if self.op == 'not':
            result = self.arg.eval(store)
            return int(not(result))
        
        raise EvalError()

# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']

    def exec(self, store):
        if store["mode"] == "pre-pass":
            return
        if DEBUG:
            print(self.__class__.__name__, store)

        print(repr(self.exp.eval(store)))

class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']

    def exec(self, store):
        """ 
        When an assignment statement executes, the left expression is evaluated to a location, 
        the right expression is evaluated to a value, and a reference to the 
        value is placed into the location.
        """
        if store["mode"] == "pre-pass":
            return
        
        rval = self.right.eval(store)
        if isinstance(self.left, Var):
            store[self.left.name] = rval
        elif isinstance(self.left, Index):
            # Array location: This is the index into an indexable, where the 
            # indexable and index are evaluated, the value of the indexable 
            # must be an array, the value of the index must be an integer, 
            # and the value of the index must not be out of bound.
            arr = self.left.indexable.name
            id = self.left.index.eval(store)
            if arr in store and id < len(store[arr]):
                # array must be defined in store
                store[arr][id] = rval
            else:
                raise EvalError()
        else:
            pass


    
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']

    def exec(self, store):
        # When a block statement executes, each of the statements of 
        # the block is executed in order.
        for st in self.stmts: st.exec(store)


class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']

    """
    When an if statement executes, the expression of the if is evaluated; 
    if the result of the evaluation is not 0, the body statement is executed
    """
    def exec(self, store):
        if store["mode"] == "pre-pass":
            return
        
        expr = self.exp.eval(store)
        if expr != 0:
            self.stmt.exec(store)       # exec all stmts
        pass


class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']

    """
    When an while statement executes, the expression of the while is evaluated; 
    if the result of the evaluation is 0, the while statement terminates; 
    otherwise, the body statement is executed, and the execution of the while 
    repeats.
    """
    def exec(self, store):
        if store["mode"] == "pre-pass":
            return
        
        expr = self.exp.eval(store)
        if expr != 0:
            self.stmt.exec(store)       # execute all stmts
            self.exec(store)            # repeat while loop execution
        pass

class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']

    """
    When a procedure definition statement executes, the name of the procedure 
    must not have been defined earlier in the program; the name of the procedure
    becomes defined by associating the parameters and body of the procedure with
    the name, if this is not already done. In particular, procedure definitions 
    could be executed in a pre-pass before program execution, in which case
    there would be no work here during the program execution.
    """
    def exec(self, store):
        if store["mode"] == "pre-pass":
            store["Function"][self.name] = {
                'params': self.params,
                'body': self.body
            }
            if DEBUG:
                print(self.__class__.__name__, store)
        else:
            pass

class Call(Node):
    """Class of nodes representing precedure calls."""
    fields = ['name', 'args']

    """
    When a procedure call statement executes, the name of the procedure must be
    defined somewhere in the program, and the number of arguments of the call 
    must equal the number of the parameters; each of the arguments of the call 
    is evaluated in order, and the body of the procedure is executed with its 
    local variables being the parameters of the procedure bound to the 
    corresponding values of the arguments. In particular, finding the names of 
    procedures defined later in the program requires executing procedure 
    definitions that appear later in the programs, if procedure definitions 
    are not executed in a pre-pass.
    """
    def exec(self, store):
        if store["mode"] == "pre-pass":
            return
        
        # store_cp = store.copy()       # doesn't work 
        # need deepcopy because of nested dicts
        store_cp = copy.deepcopy(store)
        func_ = store_cp["Function"]
        if self.name in func_:
            if len(self.args) != len(func_[self.name]["params"]):
                # check length of args
                raise EvalError()

            # evaluate all args in order and store it in a map
            """
            Variable location: This is where the variable is held in the global 
            scope or local scope---global scope if the assignment statement is 
            in the global scope, and local scope otherwise.
            """
            local_vars = {}
            for index, arg in enumerate(self.args):
                local_vars[func_[self.name]['params'][index]] = arg.eval(store)
            
            # add local vars-value mapping to local copy of global_store
            for key,val in local_vars.items():
                store_cp[key] = val

            if DEBUG:
                print(self.__class__.__name__, store_cp, global_store)
            
            # evaluate body of procedure with local variables 
            func_[self.name]['body'].exec(store_cp)
        else:
            raise EvalError()



# This is the parser using TPG for parsing FlatScript code and building an AST.
class Parser(tpg.VerboseParser):
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
    | ProcDef/s
    | ProcCall/s
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

    ProcDef/e -> 'def' ident/e1         $params=[]                    
                '\(' (ident/e2          $params.append(e2) 
                )? (',' ident/e3        $params.append(e3) 
                )* '\)' Stmt/s2         $e= Def(e1, params, s2) 
                ; 

    ProcCall/e ->  ident/e1             $fargs=[] 
                '\(' (Exp/e2            $fargs.append(e2) 
                )? (',' Exp/e3          $fargs.append(e3) 
                )* '\)' ';'             $e= Call(e1, fargs) 
                ;


    CmpOp/o -> '=='/o | '<'/o | '>'/o ;
    AddOp/o -> '\+'/o | '-'/o ;
    MulOp/o -> '\*'/o | '/'/o ;
    """
    if DEBUG:
        verbose=1
    else:
        verbose=0

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
    
    # create nested dict for function names
    global_store = dict({"mode":"pre-pass", "Function": dict()})
    node.exec(global_store)
    
    # pre-pass will store all function defs, final-pass will execute the code
    global_store["mode"] = "final-pass"
    node.exec(global_store)
    if DEBUG: 
        print(global_store)

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    if DEBUG: raise

except EvalError:
    print('Evaluation Error')

    # Uncomment the next line to re-raise the evaluation error, 
    # displaying where the error occurs.  Comment it for submission.

    if DEBUG: raise
