from limb_from_distance_matrix.main import LimbLength_ON


class Node:
    def __init__(self, id):
        self.id = id
        self.adjacent = []
        self.edges = []
    
    def add_connection_dual(self, second_node, length):
        self.adjacent.append(second_node)
        second_node.adjacent.append(self)
        
        self.edges.append(length)
        second_node.edges.append(length)
    
    def delete_connection_dual(self, second_node):
        i1 = self.adjacent.index(second_node)
        i2 = second_node.adjacent.index(self)
        self.adjacent.remove(second_node)
        second_node.adjacent.remove(self)
        
        d = self.edges[i1]
        del self.edges[i1]
        del second_node.edges[i2]
        return d
    
    def print_in_any_order(self):
        queue = [self]
        visited = set()
        for x_node in queue:
            if x_node not in visited:
                visited.add(x_node)
                print(x_node)
                queue.extend(x_node.adjacent)
            else:
                queue.pop(0)


def get_path_between_i_k_dfs(prev, x, y, path, distances, dist, find=False):
    if not find:
        path.append(x)
        distances.append(dist)
        
        if x == y:
            return True
        
        for e, child in enumerate(x.adjacent):
            if not find:
                if prev != child:
                    find = get_path_between_i_k_dfs(x, child, y, path, distances, x.edges[e], find)
        
        if not find:
            del path[-1]
            del distances[-1]
    return find


def get_node_at_distance_between_i_k(i_node, k_node, bald_distance, counter):
    path = []
    distances = []
    get_path_between_i_k_dfs(None, i_node, k_node, path, distances, 0)
    
    dist = 0
    for i, edge_distance in enumerate(distances[1:]):
        dist += edge_distance
        if dist == bald_distance:
            return path[i]
        elif dist > bald_distance:
            new_node = Node(id=counter())
            d = path[i].delete_connection_dual(path[i - 1])
            
            new_node.add_connection_dual(path[i - 1], dist - bald_distance)
            new_node.add_connection_dual(path[i], d - dist - bald_distance)
            
            return new_node
    
    raise ValueError("")


def find_node(node, i):
    queue = [node]
    visited = set()
    for x_node in queue:
        if x_node not in visited:
            visited.add(x_node)
            if x_node.id == i:
                return x_node
            else:
                neighbors = list(x_node.adjacent)
                queue.extend(neighbors)


def get_count(n):
    x = n - 1
    
    def count():
        nonlocal x
        x += 1
        return x
    
    return count


def additive_phylogeny(D):
    n = len(D)
    if n == 2:
        node0 = Node(id=0)
        node1 = Node(id=1)
        
        node0.add_connection_dual(node1, D[0][1])
        return node0
    
    limb_length, i_star, k_star = LimbLength_ON(D, n, n - 1)
    
    # Remove limb length from D
    for j in range(n - 1):
        D[j][n - 1] -= limb_length
        D[n - 1][j] = D[j][n - 1]
    bald_distance = D[i_star][n - 1]
    
    # D ← D with row n and column n removed
    D = D[:n - 1]
    for row in range(len(D)):
        D[row] = D[row][: n - 1]
    
    # create counter for new node Id
    counter = get_count(n)
    
    # T ← AdditivePhylogeny(D)
    T = additive_phylogeny(D)
    
    # v ← the (potentially new) node in T at distance x from i on the path between i and k
    i_node = find_node(T, i_star)
    k_node = find_node(T, k_star)
    v = get_node_at_distance_between_i_k(i_node, k_node, bald_distance, counter)
    
    # add new leaf
    new_leaf = Node(id=n - 1)
    new_leaf.add_connection_dual(v, limb_length)
    
    return T


if __name__ == '__main__':
    with open("data.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        
        D = []
        
        for line in file:
            line = line.rstrip('\n')
            line = line.split("\t")
            
            row = [int(num) for num in line]
            D.append(row)
        
        print(D)
        
        T = additive_phylogeny(D)
        
        T.print()
