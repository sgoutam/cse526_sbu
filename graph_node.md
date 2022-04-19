# Assignment 1: Successors of a graph node


## Question

Given (a) a graph with directed edges e, among a set of nodes numbered 1 to n, 
and (b) a particular node k, we want to find the successor nodes s of k in e.
(Node i is a successor of k iff there is an edge from k to i.)

The exercise is to write a program in each of (1) imperative, (2) database, 
(3) functional, and (4) logic programming paradigms.
(Write as many as you can.  I will help by giving more specifics below.)

(1) e is represented using an array, where e[i,j]=1 iff i has successor j. 
s is an array holding successor nodes of k in increasing node number.
Write using for-loops.

(2) e is a set.  s is a set too.  Write using set comprehensions.

(3) e is as in (1).  s is a list.  Write using recursive functions.

(4) e is a predicate.  s is a predicate too.  Write using logic rules.

Each program should be just a few lines (or even just one short line).

You should at least be able to write (1) and (3) in Python.
In fact, functional programming people like to use lists more,
so for (3), another version is to represent e using a list of lists.

## Solution
### typeset in markdown
1. 

```
# e[i,j] = 1, iff j is a successor of i  <input>
# s , array holding all successor nodes of k <output>
# k , node for which we need to find successors <input>


def find_successors(e, k):
    s = []                              # empty result list
    for i in range(0, len(e[0]) ):
        if( e[k][i] == 1):               # if node is a successor
            s.append(i)                 # append node to list

    return s

```

2. 

```
# e, set where each index points to a list of its successor nodes
# s, set for the result which will return a set of successor nodes for given k
# k, node for which we want to find successors


# Here e is essentially a hash table where each index is a node and it maps
# to a list of its successor nodes
# 1 -> [2,3]
# 2 -> [3]
# 3 -> [4]

def find_successors(e, k):
    if k in e:                  # if node exists in the set
        return e[k]             # return the successor node list
```

3. 

```
# e[i,j] = 1,
# s = list
# recursively look for successors

s = []

def find_successor(e, k, s, index):
    if index > len(e[k]):
        return s
    else:
        if e[k][index] == 1:
            s.append(index)
        else:
            find_successor(e, k, s, index+1)

find_successor(e, k, s, 0)

```

4.

```
# for defining predicate logics, we can say
# if there is an edge between k and i, then i is
# a successor of k

successor(i, k) :- edge(k, i, e)

# here if i is a successor of k, then i should be added to 
# successor list of k, so we append i to list s

add_successor(k, i) :- successor(i, k) -> append_to_list(s, i)

# we need to iterate over all nodes, so
# assuming N is the total number of all nodes in the graph

add_successors(k, N) :- N>0, add_successor(k, N)


```