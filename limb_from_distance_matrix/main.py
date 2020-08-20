import math
import random


def LimbLength_ON2(D, n_leaves, j):
    limb = math.inf
    for i in range(n_leaves):
        if i == j:
            continue
        for k in range(n_leaves):
            if k == j or i == k:
                continue
            pos_limb = (D[i][j] + D[j][k] - D[i][k]) / 2
            if pos_limb < limb:
                limb = pos_limb
    return limb


def LimbLength_ON(D, n_leaves, j):
    """
    My solution: You are free to choose i as any node such that i!=j, it will have to be in one sub-graph.
    Then you can just go through all k!=j or k!=i and you will find a node not in the same subgraph
     because tree(D) is simple.
    """
    limb = math.inf
    
    indices = list(range(n_leaves))
    indices.remove(j)
    i = random.choice(indices)
    indices.remove(i)
    k_ = None
    for k in indices:
        pos_limb = (D[i][j] + D[j][k] - D[i][k]) / 2
        if pos_limb < limb:
            limb = pos_limb
            k_ = k
    return limb, i, k_


if __name__ == '__main__':
    with open("data.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        j = int(file.readline().rstrip('\n'))
        print(n_leaves, j)
        
        D = []
        
        for line in file:
            line = line.rstrip('\n')
            line = line.split("\t")
            
            row = [int(num) for num in line]
            D.append(row)
            
        limb = LimbLength_ON(D, n_leaves, j)
        print(limb)