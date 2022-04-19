#const n = 20.

% n-Queens encoding

{ q(I,1..n) } == 1 :- I = 1..n.
{ q(1..n,J) } == 1 :- J = 1..n.
:- { q(D-J,J) } >= 2, D =   2..2*n.
:- { q(D+J,J) } >= 2, D = 1-n..n-1.

I1 = I2, J1 = J2 :- q(I1, J1), q(I2, J2) , |I1 - I2| + |J1 - J2| < 5.