(*===========================================================================*)
(* the following functions are given *)

fun map f [] = []
  | map f (a::l) = (f a) :: (map f l);

fun reduce f init (h::t) = f h (reduce f init t)
  | reduce f init []     = init;

fun accumulate f init (h::t) = accumulate f (f init h) t
  | accumulate f init []     = init;

fun exists test [] = false
  | exists test (a::l) = if (test a) then true else exists test l;

fun forall test [] = true
  | forall test (a::l) = if (test a) then (forall test l) else false;

infix through;
fun m through n = if m>n then [] else m :: ((m+1) through n);

(*===========================================================================*)

(* code only used for testing *)

val list1 = [1,2,3,4];
val list2 = [5,6,7,8];

fun ff h t = h::t;
reduce ff list1 list2;

(* output = [5,6,7,8,1,2,3,4] *)

fun append a b = reduce (fn x => fn y => x::y) b a;

append list1 list2;


(* generating a list from 1..n *)
List.tabulate(5, fn x => x+1);
(* this generates List.List *)


fun makeList 0 result = result
    | makeList n result = makeList (n-1) (n :: result);
makeList 5 [];


( 1 through 5);

fun replicate x n = map (fn t => x) (makeList n []);

replicate "Help" 5;

fun f_reduce h t = h::t;
reduce f_reduce list1 list2;

fun f_acc h t = h + t;
accumulate f_acc 0 list1;

fun f_exists a = (a mod 3) = 0;
exists f_exists [1, 14, 21];

fun f_forall a = a > 3;
forall f_forall [1, 2, 3, 4, 100];




fun member x [] = false
  | member x (y::ys) = (x=y) orelse member x ys;

fun unique1 [] = []
  | unique1 (x::xs) = let val u = unique1 xs
                     in if (member x u) then u else x::u end;



fun prime1 n =
  let fun prime2 n m = if m>=n then true
                     else if n mod m = 0 then false
                      else prime2 n (m+1)
  in (n>1) andalso prime2 n 2 end;


map prime1 (1 through 10);

val n = 10;
(2 through n);

(*==========================================================================*)

(* Solutions *)

(* cuts: takes list as input and returns list fo all its cuts *)
fun cuts (h::t) = [([], (h::t))] @ (map (fn (x1,x2) => (h::x1, x2)) (cuts t))
            | cuts [] = [([], [])];

cuts [1,2,3,4,5,6];


(* append a and b *)
fun append a b = reduce (fn x => fn y => x::y) b a;

append [1,2,3] [];
append ["Spring", "Summer", "Fall"] ["Winter"];


(* replicate list s n times *)
fun replicate s n = map (fn x => s) (1 through n);

replicate "Help" 5;
replicate () 10;

(* remove duplicates from list s *)

fun unique (h::t) = reduce (fn x => fn y => 
      (if (exists (fn z => z = x) y) 
        then y else x::y)) [] (h::t);

unique ["u", "n", "i", "q", "u", "e"];
unique [1,2,3];
unique [1,1,1,2,2,2,3,3,3,2,1,3,2,4,1,2,3,1,4,3,2,3,4,3];

(* check if an integer is prime *)

fun prime n = if n = 1 then false 
              else forall (fn x => (n mod x > 0))
              (2 through n-1);

map prime (1 through 10);
prime 329;

