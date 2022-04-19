#! /usr/bin/python3

def gen_sequence_from():
    """
    generates infinite sequence of numbers starting from 0

    Ref: https://riptutorial.com/python/example/2527/infinite-sequences
    """
    n = 0
    while True:
        yield n
        n += 1

def map(func, l):
    """
    implementation of map from B.2
    """
    return [func(x) for x in l]

def reduce(func, init, l):
    """
    implementation of reduce from B.2
    """
    if l:
        return func(l[0], reduce(func, init, l[1:]))
    return init

def accumulate(func, init, l):
    """
    accumulate from B.2
    """
    if l:
        return accumulate(func, func(init, l[0]), l[1:])
    return init

def append(a,b):
    """
    fun append a b = reduce (fn x => fn y => x::y) b a;
    """
    res = reduce(lambda x,y: y.insert(0,x) or y, a,b)
    return res

def replicate(s,n):
    """
    fun replicate s n = map (fn x => s) (1 through n);
    """
    res = map(lambda x: s, range(0,n))
    return res




if __name__ == "__main__":

    for num in gen_sequence_from():
        if num == 5:
            break
        print(num)

    print(append([1,2,3], [4,5,6]))
    print(replicate("Hello", 5))
    print(accumulate(lambda h, t: h + t, 0, [1, 2, 3]))
