import math


class Node:
    def __init__(self):
        self.left = None
        self.right = None


class Edge:
    def __init__(self, inp, out, weight):
        self.inp = inp
        self.out = out
        self.weight = weight

    
def update_matrix(matrix, i, j, distance):
    matrix[i][j] = distance
    matrix[j][i] = distance
    return matrix


def floyd_warshall_algorithm(dm, n_nodes):
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i == j:
                dm[i][j] = 0
    
    for k in range(n_nodes):
        for i in range(n_nodes):
            for j in range(n_nodes):
                if dm[i][k] < math.inf and dm[k][j] < math.inf and dm[i][j] > dm[i][k] + dm[j][k]:
                    dm[i][j] = dm[i][k] + dm[k][j]
    
    return dm


if __name__ == '__main__':
    edges = []
    with open("dataset_10328_12.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        print(n_leaves)
        
        nodes = set()
        for line in file:
            line = line.rstrip('\n')
            print(line.split("->"))
            
            arr = line.split("->")
            arr1 = arr[1].split(":")
            i = int(arr[0])
            j = int(arr1[0])
            distance = int(arr1[1])
            
            edges.append(Edge(i, j, distance))
            nodes.add(i)
            nodes.add(j)

        n_nodes = len(nodes)
        dm = [[math.inf] * n_nodes for i in range(n_nodes)]
        
        for edge in edges:
            update_matrix(dm, edge.inp, edge.out, edge.weight)
        
        dm = floyd_warshall_algorithm(dm, n_nodes)
        
        for i in range(n_leaves):
            print(*dm[i][:n_leaves], sep=" ")