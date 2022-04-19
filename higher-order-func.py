#! /usr/bin/python3

"""
__author__ : Sanket Goutam

"""



class SML_python:
    """
        See lectnotes.txt for functions defined in SML.

        Define in Python the corresponding functions for:
        (1) inc
        (2) the second twice that uses lambda's
        (3) map

        and print the values of:
        (a) inc applied to 3
        (b) twice
        (c) a call to twice
        (d) the value of (c) applied to inc
        (e) the value of (d) applied to 3
        (f) map applied to inc and [1,2,3]

        Bonus: define in Python the corresponding function for

        fun reduce f init (h::t) = f h (reduce f init t)
        | reduce f init []     = init;

        and print the value of reduce applied to the + function, 0, and [1,2,3]

    """

    def inc(self, n):
        """
            fun inc n = n+1;
            inc five;
        """
        return n+1

    def twice(self, func, x):
        """
            (* lambda *)
            val twice = fn f => (fn x => f(f(x)));
        """
        return lambda func,x: func(func(x))
    
    def map(self, func, input_list):
        """
            fun map f [] = []
                  | map f (x::xs) = f x :: (map f xs);
            map inc [1,2,3];
        """
        output_list = list(map(func, input_list))
        return output_list

    def reduce(self, func, init, input_list, output_list):
        """
            fun reduce f init (h::t) = f h (reduce f init t)
                    | reduce f init []     = init;
        """
        if len(input_list) == 0:
            return output_list.append(init)
        
        output_list.append(func(input_list[0]))
        self.reduce(func, init, input_list[1:], output_list)
        



sml = SML_python()

val = 3
# (a) inc applied to 3
print("a. ",sml.inc(val))

# (b) twice
print("b. ", sml.twice)

# (c) call to twice
twice_output = sml.twice(sml.inc, val)
print("c. ", twice_output)

# (d) value of (c) applied to inc
# (e) value of (d) applied to 3
print("d,e. ", twice_output(sml.inc, val))

# (f) map applied to inc and [1,2,3]
input_list = [1,2,3]
print("f. ", sml.map(sml.inc, input_list))

# Bonus for "reduce" function
output_list = []
sml.reduce(sml.inc, 0, input_list, output_list)
print("Bonus: ", output_list)