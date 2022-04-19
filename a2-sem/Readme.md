# CSE526: Assignment 2

> Sanket Goutam (sanket.goutam@stonybrook.edu)
> Student ID: 111463594
> Due date: Feb 28, 2022 11:59PM


## Flatscript - Program Execution

In this section, I explain my implementation of program execution for Flatscript

Note: I have added snippets from assignment description in my code as comments, 
to help write the logic of the code. Most of the implementation is a straightforward
translation of the assignment description.

### Logical and Relational operations

I have clubbed together all operations in BinOpExp with the operands being
`int` since except `add` operation all other operations require `int` operands.

I use generator comprehensions in python for all the relational operations,
where I return `1` if the comparison evaluates to `True` and `0` otherwise.

### Array Indexing

This was a little tricky to figure out.

    Arr[<id>] -> Indexable[Index]

The tpg parser is basically trying to create the AST nodes as above. So for a 
1-D array we need to resolve `Arr -> Indexable` and `<id> -> Index`. Here `Arr` 
should be a Var node and needs to be present in our global_store.

```
        # Assign.eval()
        if isinstance(self.left, Var):
            store[self.left.name] = rval

        # Index.eval()
        b = self.index.eval(store)
        if isinstance(self.indexable, Var):
            a = self.indexable.name
            if a in store and b < len(store[a]):
                return store[a][b]
```

However, it gets tricky when we need to handle multi-dimensional arrays. 

    Arr[<id1>][<id2>] -> Indexable[Index]

Here tpg will still resolve `Arr[<id1>] -> Indexable` and `<id2> -> Index`. So
when indexing a multi-dimensional array we need to recursively evaluate
the Indexable until there are no `Index` nodes inside it and we resolve it 
into a Var AST node.

```
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

```

By recursively calling `self.indexable.eval()` we are essentially doing a 
bottom-up evaluation. `Arr[][][]` will get evaluated as `Arr[id1]` `[id2][id3]` 
then `Arr[id1][id2]` `[id3]`.


> Example of global_store for 2D arrays for a1input2.txt

    {
        'mode': 'final-pass', 
        'Function': {}, 
        'data': [[100, 42], [100, 50], [123, 456], [300, 9000]], 
        'result': [2, 50, 3, 300], 
        'i': 4, 
        'a': 300, 
        'b': 0
    }

### If and While statements

For `If` and `While` statements I pretty much translated the description provided
in the assignment description. 

The only difference between `If` and `While` is pretty much the recursive 
execution in case of `While` until the `exp` evaluates to `False`.

### Running the program

> Input examples

a2input0.txt a1input1.txt a1input2.txt.

> Testing

    python a2main.py a2input0.txt
    python a2main.py a1input1.txt
    python a2main.py a1input2.txt

> Output

Output will be generated to stdout. You can compare against a2output0.txt, 
a2output1.txt, and a2output2.txt respectively.

> Supported Python versions

Supported on Python 3.8.10+ versions

> References:

[tpg module](https://github.com/CDSoft/tpg)


## Extra Credit I : RecScript evaluation

### Modifications to Parser

I modified to the Parser provided in the assignment by including my rules for
Procedure definition and Procedure call that I submitted for extra credit 
in the previous assignment.

```
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
```

### Lookahead parsing

The hint for lookahead parsing was provided in the assignment description.
We need to pre-parse the input file first to identify all the function 
definitions and store them in our `global_store` and finally do a final
parse when the functions actually get executed.

I modified the `global_store` to include a nested dict using

```    
    # create nested dict for function names
    global_store = dict({"mode":"pre-pass", "Function": dict()})
```

I use the "pre-pass" and "final-pass" modes to distinguish between the 
versions of the global_store for AST node creation. During "pre-pass" mode only 
the Def() AST node gets executed.

### Handling local variables for functions

To handle local variable declarations, along with shadowing of global variables,
I create a deepcopy of the global_store and create mappings between 
`Varname : Value` for the local variables.

> Example of function call global_store for a2input3.txt

    {
        'mode': 'final-pass', 
        'Function': {
            'p': {
                'params': ['x1', 'x2', 'x3', 'x4'], 
                'body': <__main__.Print object at 0x7fac41db9dc0>
            }, 
            'g': {
                'params': ['x', 'y'], 
                'body': <__main__.Print object at 0x7fac41dcc280>
            }, 
            'g0': {
                'params': ['x'], 
                'body': <__main__.Block object at 0x7fac41dcc7f0>
            }
        }, 
        'x1': 1, 
        'x2': 2, 
        'x3': 3, 
        'x4': 4
    }

## Extra Credit II : FlatScript to C#


### Running the program

`a2gen.py` is the script which converts a FlatScript input file into C# code.

I chose C# as my target language as I plan on doing the same for my project.

> Running the program

    python a2gen.py test.txt test.cs

test.txt is the input file with FlatScript code, test.cs is the name of the 
output file being generated

> Evaluating C# code

I used the online C# editor linked below to evaluate the generated code.
[C# Online compiler](https://dotnetfiddle.net/)

Copy the contents from the generated `test.cs` file and run it on this website.


### Implementation

I have based my implementation on top of the base code provided with the assignment.
Eval and Exec functions are not required for this, so I have only introduced
a new function call `convert()` for each AST node.

`convert()` basically returns the subsequent C# equivalent code for each AST node
identified by tpg in the FlatScript program.

Since C# is a **strongly typed language** there are quite a lot of complications
for target code completion. My program has several limitations which I discuss
in the section below. 

But the basic idea for handling strongly typed languages has been implemented in 
`Assign`. Essentially during every operation we need to check the right side
of the statement and declare our left variables according to the data type
of the right side.

```
    data = [1,2,3,4]

    when converted to C#, will need to be written as

    int [] data = {1,2,3,4};


    Similarly,

    i = 0
    i = i + 1

    in C# will become

    int i = 0;
    i = i + 1;

```

So there is a strong dependency on the data type as well as variable scoping and
variable declaration before definition.


In my implementation, I have been able to cover some of the basic parts:

1. Int variable declaration and usage
2. 1-D array declaration and usage
3. If/While loop and variable scoping
4. Logical and Comparison operations


Note: The target code generated doesn't have proper indentation. But that shouldn't
matter because C# uses scoping using blocks {}, and treats all indentation as
blank space.


### Limitations

There were a few complications that came up which I was not able to resolve in
time before submission.

1. 2-D arrays

```    
    data = [[1,3], [2,4]]

    in C# is represented as

    int [,] data = {{1,3}, {2,4}};

    data[1][0] becomes data[1,0]
```

To achieve the above result, I will need to implement information about nesting
in Index and Array nodes. Basically the Index, Array, and Assign AST nodes will 
need to be updated to handle information about the dimensions of array during
definition so that the target code gets created accordingly.

2. Because of the strongly typed nature, `print Var` is not a straightforward
   implementation for target code. If Var is an array then we need to use loops
   to print the elements. If Var is Int/String it will work.

3. I have not implemented RecScript target code conversion. 