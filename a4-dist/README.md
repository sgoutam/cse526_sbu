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

Pros:
+ 