# CSE526: Assignment 1

> Sanket Goutam (sanket.goutam@stonybrook.edu)
> Student ID: 111463594
> Due date: Feb 14, 2022 11:59PM


## Design of the parser

### Files attached

1. Readme.md:           Implementation details
2. a1main.py:           main program
3. tpg.py:              tpg module
4. a1inputtest.txt:     Sample test cases used


### Precedence of operations:
  
To get the precedence of operations, we need to make sure that our rules
decompose in the order of precedence ensuring that highest order operations
are always evaluated first.

To achieve this I used nested operations (reference to the example discussed 
during lecture).

        Stmt -> Exp
        Exp -> Term
        Term -> Add (MulOp Add)*        # Multiply/Divide
        Add -> Rel (AddOp Rel)*         # Add/Subtract
        Rel -> Neg (RelOp Rel)*         # Relational (>, <, ==, >=, <=)
        Neg -> (negate)* Log            # Negation  (not)
        Log -> Atom (LogOp Atom)*       # Logical   (and, or)

        Atom -> '\(' Exp '\)' | int | ident | string

If we draw the parse tree for the above set of productions, we will notice
that higher precedence operations will always get 
evaluated first.

Note: The above parser supports nesting of one of more instances of all
expressions. 

Test samples (refer a1input0.txt)
    - not ( not ( a and b))
    - a and ( b or c or d)
    - a + b * c + d and e or f and not g

### Arrays and Indexing

We can represent arrays in tpg using the follwing syntax.

    Array -> '[' Exp (',' Exp )* ];         # Nested arrays

Array indexing grammar can be written as

    IndexOp -> ident ('\[' Exp '\]' )+ ;    # indexing needs 1 or more [Exp]


### Helper classes used as Python actions in tpg

I have created different Helper classes for different kinds of statements.

+ CtrlStmt() class is used for While/If blocks
+ Comment() class for Comments
+ Array() class for handling Array definitions
+ ArrayIndex() class for indexing related operations

The syntax and definition for these classes are largely copied from the 
templates already provided with the assignment.

### Test cases:

Run the following test cases

```
python3 a1main.py a1input0.txt
python3 a1main.py a1input1.txt
python3 a1main.py a1input2.txt
```

Credits claimed for all the test cases covered in these 3 examples provided with
the assignmnet.

Some additional test cases are included in the a1inputtest.txt file.


## Extra Credit — Procedures

### Parser syntax

I have added two production rules for procedure definition and procedure call.

    ProcDef -> 'def' ident '\(' (ident)? (',' ident)* '\)' Stmt ;

    ProcCall -> ident '\(' (Term)? (',' ident)* '\)' Stmt ;

Since a function can have any number of arguments, we ensure that our parser
allows 1 or more identifiers as the parameters to the function.

Above syntax also allows for nested procedure defintions, as we recursively
decompose to `Stmt` production rule and the `ProcDef` and `ProcCall` are also
stemmed at `Stmt`.

### Procedure helper class

Similar as before, I created two helper classes for dealing with procedure 
definition and calls, `CreateFunc` and `CallFunc`.

To solve the problem of global variable scope and local variable scope, I 
redefined the `varnames` function locally in each class. Initially I was trying
to add all variables passed as arguments into the function to the global
`vars_defined`, following the similar logic from `Assign` class.

But that was clearly wrong because there was no way to distinguish between 
global and local scopes. To achieve this I insert a tuple for each 
function into `vars_defined`, with the follwing syntax

    ('FuncName', func_name, *params, *stmts)

        func_name: name of the function
        *params: list of all the parameters passed locally to the function
        *stmts: Block object representing all the statements defined inside
                the function definition

Having this syntax helps me to identify the local variables defined within
each functions scope, since I can directly look at *params list for each 
function. It also helps identify shadow variables as all global variables
will be declared in `vars_defined`, whereas any redefinition of a global 
variable has to be also present inside the functions *params list.


```
y = 1;                      # vars_defined.add('y')
def g(x,y): {               
    x= 1;
    print x+y;
}                           # vars_defined.add(('FuncName', 'g', ('x','y'),
                            #                   Block.object ))

```

### Extra credits claimed

+ I was able to get most of the test cases covered in a1input3.txt
+ Nested procedure definitions is implemented
+ Procedures and Variables are defined in different namespaces, since I use 
    different validations for procedure names and var names.
+ Shadowing of a global variable is implemented.


### Not implemented
+ I haven't been able to figure out how to do procedure definition lookahead.
    The following test case in a1input3.txt is not working for me.

        # test a procedure call to a procedure defined later
        g(1,2);
+ Not fully tested on a1input4.txt. 