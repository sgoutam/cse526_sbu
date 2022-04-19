append([],Ys,Ys).
append([X|Xs],Ys,[X|Zs]) :- append(Xs,Ys,Zs).


% suffix/2
% suffix([1,2], [1,2,3,4]) = [3,4]
% suffix([1,2], [3,4]) = False
% find Z s.t. X+Z = Y

suffix(X,Y) :- append(X, Z, Y), write(Z).

% Test suffix
suffix([1,2],[1,2,3,4]).
suffix([1,2], [3,4]).

% cut(X)
% cut([1,2,3]) = [], [1,2,3]
% [1], [2,3]
% [1,2], [3]
% [1,2,3], []
% find Y,Z s.t. Y+Z = X

cut(X) :- append(Y, Z, X), write(Y), write(" "), write(Z), writeln(" "), fail.
cut([1,2,3]).

% Graph reachability

source(1).
edge(0,1).
edge(1,2).
edge(1,3).
edge(2,5).
edge(3,5).
edge(3,6).
edge(5,7).
edge(5,9).
edge(6,8).
edge(7,9).
edge(9,11).
edge(10,12).
edge(10,13).
edge(11,13).
%edge(13,5).

% tabling for efficient lookup and to avoid stack overflow
:- table reach/1.

reach(X) :- source(X).
reach(X) :- edge(Y,X), reach(Y).

printReach :- reach(X), write(X), write(" "), fail.
printReach.

% path(A,B) iff there is a sequence of edges from A to B
:- table path/2.
path(A,B) :- edge(A,B) | path(A,X), edge(X,B).

% cycle(A) iff a is in a cycle
cycle(A) :- path(A,A).
printCycles :- cycle(X), write(X), writeln(" "), fail.
printCycles.

% Timing functions

timeReach :- get_time(T0), printReach, get_time(T1), T is (T1 - T0)*1000, write(T).

timeCycle :- get_time(T0), printCycles, get_time(T1), T is (T1 - T0) * 1000, write(T).





