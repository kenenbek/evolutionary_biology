from limb_from_distance_matrix.main import LimbLength_ON


class PhyloGeneticTree:
    def __init__(self, n):
        self.adjacency_matrix = []
        for i in range(n):
            row = [None for _ in range(n)]
            row[i] = 0
            self.adjacency_matrix.append(row)
    
    def add_node(self):
        n = len(self.adjacency_matrix)
        new_row = [None for _ in range(n + 1)]
        new_row[n] = 0
        
        for row in range(n):
            self.adjacency_matrix[row].append(None)
        
        self.adjacency_matrix.append(new_row)
    
    def add_edge(self, i, j, length):
        self.adjacency_matrix[i][j] = length
        self.adjacency_matrix[j][i] = length
    
    def remove_edge(self, i, j):
        self.adjacency_matrix[i][j] = None
        self.adjacency_matrix[j][i] = None
    
    def __getitem__(self, item):
        return self.adjacency_matrix[item]
    
    def __len__(self):
        return len(self.adjacency_matrix)
    
    def __str__(self):
        result = []
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] is not None and i != j:
                    result.append(str(i) + "->" + str(j) + ":" + str(int(self.adjacency_matrix[i][j])))
                    
        return "\n".join(result)
    
    
def get_path_between_i_k_dfs(phylo_tree, prev, x, y, path, find=False):
    if not find:
        path.append(x)
        
        if x == y:
            return True
        for neighbor, dist in enumerate(phylo_tree[x]):
            if not find and dist is not None and prev != neighbor and neighbor != x:
                find = get_path_between_i_k_dfs(phylo_tree, x, neighbor, y, path, find)
        
        if not find:
            del path[-1]
    return find


def find_i_and_k(D, n, limb_length):
    for i in range(n):
        for k in range(n):
            if D[i][k] == D[i][n] + D[n][k] - 2 * limb_length:
                return i, k
    raise ValueError("error")


def get_node_at_distance_between_i_k(phylo_tree, i, k, bald_distance):
    path = []
    get_path_between_i_k_dfs(phylo_tree, None, i, k, path)
    
    dist = 0
    for i in range(1, len(path)):
        dist += phylo_tree[path[i - 1]][path[i]]
        
        if dist == bald_distance:
            return path[i]
        elif dist > bald_distance:
            new_node = len(phylo_tree)
            phylo_tree.add_node()
            
            phylo_tree.add_edge(path[i], new_node, dist - bald_distance)
            phylo_tree.add_edge(path[i - 1], new_node, phylo_tree[path[i]][path[i - 1]] - (dist - bald_distance))
            
            phylo_tree.remove_edge(path[i], path[i - 1])
            
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


def additive_phylogeny(D, phylo_tree):
    n = len(D)
    if n == 2:
        phylo_tree.add_edge(0, 1, D[0][1])
        return
    
    limb_length, i, k = LimbLength_ON(D, n, n - 1)
    # i, k = find_i_and_k(D, n - 1, limb_length)
    
    # Remove limb length from D
    for j in range(n - 1):
        D[j][n - 1] -= limb_length
        D[n - 1][j] = D[j][n - 1]
    bald_distance = D[i][n - 1]
    
    # D ← D with row n and column n removed
    D = D[:n - 1]
    for row in range(len(D)):
        D[row] = D[row][: n - 1]
    
    # T ← additive_phylogeny(D)
    additive_phylogeny(D, phylo_tree)
    
    # v ← the (potentially new) node in T at distance x from i on the path between i and k
    v = get_node_at_distance_between_i_k(phylo_tree, i, k, bald_distance)
    
    # add new leaf n-1 to its parent v
    phylo_tree.add_edge(v, n-1, limb_length)
    
    return


if __name__ == '__main__':
    import random
    
    random.seed(42)
    with open("dataset_10330_6.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        
        D = []
        
        for line in file:
            line = line.rstrip('\n')
            line = line.split()
            
            row = [int(num) for num in line]
            D.append(row)
        
        print(D)
        
        phylo_tree = PhyloGeneticTree(n_leaves)
        additive_phylogeny(D, phylo_tree)
        
        print(phylo_tree)
