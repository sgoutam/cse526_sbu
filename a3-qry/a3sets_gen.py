import random
import sys

def generate_graph(G, S):
    """
    generate a random graph based on input params.
    params:
        G: (V,E)   # Graph represented as a set
        V: number of vertices
        E: number of edges
        S: number of source nodes
    output:
        set of edges represented as (a,b) for an edge between nodes a & b
        set of source nodes
    """
    V,E = G
    edge_set = set()
    snode_set = set()
    while (len(edge_set) < E):
        l, r = random.randint(1, V), random.randint(1, V)
        if (not (l == r)):
            edge_set.add((l, r))
        if (len(snode_set) < S):
            snode_set.add(l)
    with open(('./reach.in.%s_%s_%s' % (V, E, S)), 'w+') as outfile:
        outfile.write(('%s\n' % edge_set))
        outfile.write(('%s' % snode_set))
    # print(edge_set)
    # print("\n\n\n", snode_set)


if __name__ == "__main__":
    if (len(sys.argv) == 4):
        V, E, S = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    else:
        V,E,S = 100,200,20    
    # print(V,E,S)
    G = (V,E)
    generate_graph(G,S)
    # print(G,S)