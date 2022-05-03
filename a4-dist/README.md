# CSE526: Assignment 3

> Sanket Goutam (sanket.goutam@stonybrook.edu)
> Student ID: 111463594
> Due date: May 2, 2022 11:59PM

## Prerequisites

Install dist-algo using

` pip3 install -pre pyDistAlgo`

## A. Best Modular Design

This game (with the distributed processing) has two components:

- N Player instances that are placing their moves on a board once per turn.
- The board gets replicated among all the players so that the moves of each
    player is replicated on all the board instances.

We can redesign this problem in the following ways:

**Without distributed design**

- Instead of creating multiple instances of the board, we can simply have
just one instance that is shared between all the players. 

- Each player can make a move during their turn and all the updates are made 
to the same board instance.

We can achieve this in the current design by making minor modifications to the
code provided.

+ Instead of creating multiple Player() instances that communicate with each other
via distributed networking, we simply use the run() method inside BoardAI
class to repeatedly play moves per each player.

```python
    def run():
        for player in range(max_players):
            if self.finished(player) == False:
                self.move(player.id)
```

The above logic will use the same board instance and place moves by each player
in a sequential order. 


Pros:

+ No need for any networking, message passing, synchonization of moves, etc.
+ Avoid unnecessary duplication of the board, which may be a problem for boards
of higher dimensions (data size increases)

Cons:

+ Since there is only one instance of the board, all the players effectively 
need to play on the same machine.
+ If the number of players increases exponentially, it creates a version of the
dining philosophers problem where each player is waiting for the others to finish
before they can start playing.

**Without using Objects**

If we don't have support for objects, we can represent the entire board as a 
matrix (2D arrays). Each position (i,j) in the matrix denotes a tile on the board,
and the value at (i,j) location denotes the player id who made a move there.

It can easily be implemented in C, however most of the modular design provided
in the current template will need to be stripped away.

Pros:

+ Fairly simple design, easy to implement, probably highly scalable as memory
footprint of 2D arrays (can use uint8 values) would be quite low.

+ Highly efficient (memory and time complexity) code can be implemented using
languages like C, Rust, etc.


Cons:

+ Might not be able to write modular programs, as most of the implementation
(like using uint8 values) creates a limitation on the scalability of number of 
players (although it would be quite high).

+ Will need to implement networking and distibuted resource sharing services, which
would get really complicated.


---------

## B, C: Objects and Distributed processes


> Refer to a4main.da for implementation

I have filled in all of the TODO sections provided in the template code
and tested by running the program several times over.

Note that the number of players, size of board, etc. have been hard coded in 
the program (as per the template). Submitted code works for board size 3*3
with 2 players playing the game.

Run using:
```bash
python -m da a4main.da
```

Output:

```bash

(venv) pascal➜  a4-dist$ (master) python -m da a4main.da                                                                                                                                          ✭ ✱
/home/sgoutam/Documents/SBU/sem_2/CSE526/assignments/a4-dist/./a4main.da compiled with 0 errors and 0 warnings.
[51] da.api<MainProcess>:INFO: <Node_:67001> initialized at 127.0.0.1:(UdpTransport=32420, TcpTransport=25980).
[52] da.api<MainProcess>:INFO: Starting program <module 'a4main' from '/home/sgoutam/Documents/SBU/sem_2/CSE526/assignments/a4-dist/./a4main.da'>...
[52] da.api<MainProcess>:INFO: Running iteration 1 ...
[52] da.api<MainProcess>:INFO: Waiting for remaining child processes to terminate...(Press "Ctrl-C" to force kill)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (2, 1): False, (2, 2): False, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): False}
_ _ _
_ _ _
_ _ _
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (2, 1): False, (2, 2): False, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): False}
_ _ _
_ _ _
_ _ _
---- move by player 1  :  (1, 2)
board of  2 : {(1, 1): False, (1, 2): 1, (1, 3): False, (2, 1): False, (2, 2): False, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): False}
_ o _
_ _ _
_ _ _
---- move by player 2  :  (2, 2)
[82] da.api<MainProcess>:INFO: Main process terminated.
board of  1 : {(1, 1): False, (1, 2): 1, (1, 3): False, (2, 1): False, (2, 2): 2, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): False}
_ o _
_ x _
_ _ _
---- move by player 1  :  (2, 1)
board of  2 : {(1, 1): False, (1, 2): 1, (1, 3): False, (2, 1): 1, (2, 2): 2, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): False}
_ o _
o x _
_ _ _
---- move by player 2  :  (3, 3)
board of  1 : {(1, 1): False, (1, 2): 1, (1, 3): False, (2, 1): 1, (2, 2): 2, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): 2}
_ o _
o x _
_ _ x
---- move by player 1  :  (1, 3)
board of  2 : {(1, 1): False, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 2, (2, 3): False, (3, 1): False, (3, 2): False, (3, 3): 2}
_ o o
o x _
_ _ x
---- move by player 2  :  (2, 3)
board of  1 : {(1, 1): False, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 2, (2, 3): 2, (3, 1): False, (3, 2): False, (3, 3): 2}
_ o o
o x x
_ _ x
---- move by player 1  :  (1, 1)
board of  2 : {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 2, (2, 3): 2, (3, 1): False, (3, 2): False, (3, 3): 2}
o o o
o x x
_ _ x
---- move by player 2  :  (3, 2)
board of  1 : {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 2, (2, 3): 2, (3, 1): False, (3, 2): 2, (3, 3): 2}
o o o
o x x
_ x x
---- move by player 1  :  (3, 1)
board of  2 : {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 2, (2, 3): 2, (3, 1): 1, (3, 2): 2, (3, 3): 2}
o o o
o x x
o x x
==== player 1 won: row 1
player 2 : Congratulations to 1
(venv) pascal➜  a4-dist$ (master)  

```

-----------


## Extra Credit II : Generalized game


> Refer to a4-generalized.da

I mostly modified my `a4main.da` file itself to support parameterized 
board size and number of players.

The parameters that you can modify are (refer to *def main()* ):

    m, n            # used to define board of size m*n
    k               # checks of k-consecutive tiles to win
    num_players     # use to define players in the game ( between 3 - 8 )


Submitted code has m = 5, n = 6, k = 4, num_players = 3

Run using:

```bash
python -m da a4-generalized.da
```

Output:

```bash

(venv) pascal➜  a4-dist$ (master) python -m da a4-generalized.da                                                                                                                                  ✭ ✱
/home/sgoutam/Documents/SBU/sem_2/CSE526/assignments/a4-dist/./a4-generalized.da compiled with 0 errors and 0 warnings.
[52] da.api<MainProcess>:INFO: <Node_:c3001> initialized at 127.0.0.1:(UdpTransport=10755, TcpTransport=12553).
[52] da.api<MainProcess>:INFO: Starting program <module 'a4-generalized' from '/home/sgoutam/Documents/SBU/sem_2/CSE526/assignments/a4-dist/./a4-generalized.da'>...
[52] da.api<MainProcess>:INFO: Running iteration 1 ...
[52] da.api<MainProcess>:INFO: Waiting for remaining child processes to terminate...(Press "Ctrl-C" to force kill)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): False, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): False, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): False, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): False, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): False, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): False, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): False, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): False, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): False, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
---- move by player 1  :  (4, 3)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): False, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): False, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
_ _ ! _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
---- move by player 2  :  (2, 4)
[98] da.api<MainProcess>:INFO: Main process terminated.
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): False, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ @ _ _
_ _ _ _ _ _
_ _ ! _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
---- move by player 3  :  (6, 1)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): False, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
_ _ _ @ _ _
_ _ _ _ _ _
_ _ ! _ _ _
_ _ _ _ _ _
# _ _ _ _ _
---- move by player 1  :  (2, 1)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): False, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ _ _
_ _ ! _ _ _
_ _ _ _ _ _
# _ _ _ _ _
---- move by player 2  :  (3, 5)
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): False, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ @ _
_ _ ! _ _ _
_ _ _ _ _ _
# _ _ _ _ _
---- move by player 3  :  (5, 4)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): False, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ @ _
_ _ ! _ _ _
_ _ _ # _ _
# _ _ _ _ _
---- move by player 1  :  (4, 5)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): False, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ @ _
_ _ ! _ ! _
_ _ _ # _ _
# _ _ _ _ _
---- move by player 2  :  (4, 1)
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): False, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ @ _
@ _ ! _ ! _
_ _ _ # _ _
# _ _ _ _ _
---- move by player 3  :  (5, 6)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): False, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
_ _ _ _ @ _
@ _ ! _ ! _
_ _ _ # _ #
# _ _ _ _ _
---- move by player 1  :  (3, 1)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): False, (5, 1): False, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! _ ! _
_ _ _ # _ #
# _ _ _ _ _
---- move by player 2  :  (5, 1)
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): False, (5, 1): 2, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! _ ! _
@ _ _ # _ #
# _ _ _ _ _
---- move by player 3  :  (4, 6)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ _ _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! _ ! #
@ _ _ # _ #
# _ _ _ _ _
---- move by player 1  :  (1, 4)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): False, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ ! _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! _ ! #
@ _ _ # _ #
# _ _ _ _ _
---- move by player 2  :  (5, 2)
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): False, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ ! _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! _ ! #
@ @ _ # _ #
# _ _ _ _ _
---- move by player 3  :  (4, 4)
board of  1 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): False, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ ! _ _
! _ _ @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ _ # _ #
# _ _ _ _ _
---- move by player 1  :  (2, 3)
board of  2 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): False, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ _ # _ #
# _ _ _ _ _
---- move by player 2  :  (6, 2)
board of  3 : {(1, 1): False, (1, 2): False, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ _ _ ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ _ # _ #
# @ _ _ _ _
---- move by player 3  :  (1, 2)
board of  1 : {(1, 1): False, (1, 2): 3, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): False, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ # _ ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ _ # _ #
# @ _ _ _ _
---- move by player 1  :  (5, 3)
board of  2 : {(1, 1): False, (1, 2): 3, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): False, (6, 4): False, (6, 5): False, (6, 6): False}
_ # _ ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # _ #
# @ _ _ _ _
---- move by player 2  :  (6, 4)
board of  3 : {(1, 1): False, (1, 2): 3, (1, 3): False, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): False, (6, 4): 2, (6, 5): False, (6, 6): False}
_ # _ ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # _ #
# @ _ @ _ _
---- move by player 3  :  (1, 3)
board of  1 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): False, (6, 4): 2, (6, 5): False, (6, 6): False}
_ # # ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # _ #
# @ _ @ _ _
---- move by player 1  :  (6, 3)
board of  2 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): False, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): False, (6, 6): False}
_ # # ! _ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # _ #
# @ ! @ _ _
---- move by player 2  :  (1, 5)
board of  3 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): False, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): False, (6, 6): False}
_ # # ! @ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # _ #
# @ ! @ _ _
---- move by player 3  :  (5, 5)
board of  1 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): False, (6, 6): False}
_ # # ! @ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ _ _
---- move by player 1  :  (6, 5)
board of  2 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): False, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ _
! _ ! @ _ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 2  :  (2, 5)
board of  3 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): False, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ _
! _ ! @ @ _
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 3  :  (2, 6)
board of  1 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): False, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ _
! _ ! @ @ #
! _ _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 1  :  (3, 2)
board of  2 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): False, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ _
! _ ! @ @ #
! ! _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 2  :  (1, 6)
board of  3 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): False, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ @
! _ ! @ @ #
! ! _ _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 3  :  (3, 3)
board of  1 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): False}
_ # # ! @ @
! _ ! @ @ #
! ! # _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! _
---- move by player 1  :  (6, 6)
board of  2 : {(1, 1): False, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
_ # # ! @ @
! _ ! @ @ #
! ! # _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! !
---- move by player 2  :  (1, 1)
board of  3 : {(1, 1): 2, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): False, (3, 5): 2, (3, 6): False, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
@ # # ! @ @
! _ ! @ @ #
! ! # _ @ _
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! !
---- move by player 3  :  (3, 6)
board of  1 : {(1, 1): 2, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): False, (3, 5): 2, (3, 6): 3, (4, 1): 2, (4, 2): False, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
@ # # ! @ @
! _ ! @ @ #
! ! # _ @ #
@ _ ! # ! #
@ @ ! # # #
# @ ! @ ! !
---- move by player 1  :  (4, 2)
board of  2 : {(1, 1): 2, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): False, (3, 5): 2, (3, 6): 3, (4, 1): 2, (4, 2): 1, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
@ # # ! @ @
! _ ! @ @ #
! ! # _ @ #
@ ! ! # ! #
@ @ ! # # #
# @ ! @ ! !
---- move by player 2  :  (3, 4)
board of  3 : {(1, 1): 2, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): False, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): 2, (3, 5): 2, (3, 6): 3, (4, 1): 2, (4, 2): 1, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
@ # # ! @ @
! _ ! @ @ #
! ! # @ @ #
@ ! ! # ! #
@ @ ! # # #
# @ ! @ ! !
---- move by player 3  :  (2, 2)
board of  1 : {(1, 1): 2, (1, 2): 3, (1, 3): 3, (1, 4): 1, (1, 5): 2, (1, 6): 2, (2, 1): 1, (2, 2): 3, (2, 3): 1, (2, 4): 2, (2, 5): 2, (2, 6): 3, (3, 1): 1, (3, 2): 1, (3, 3): 3, (3, 4): 2, (3, 5): 2, (3, 6): 3, (4, 1): 2, (4, 2): 1, (4, 3): 1, (4, 4): 3, (4, 5): 1, (4, 6): 3, (5, 1): 2, (5, 2): 2, (5, 3): 1, (5, 4): 3, (5, 5): 3, (5, 6): 3, (6, 1): 3, (6, 2): 2, (6, 3): 1, (6, 4): 2, (6, 5): 1, (6, 6): 1}
@ # # ! @ @
! # ! @ @ #
! ! # @ @ #
@ ! ! # ! #
@ @ ! # # #
# @ ! @ ! !
==== player 1 won: column 3
player 2 : Congratulations to player 1
player 3 : Congratulations to player 1
(venv) pascal➜  a4-dist$ (master) 
```