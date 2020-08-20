import math


class Node:
    def __init__(self, id, age):
        self.id = id
        self.age = age
        self.children = []
    
    def __eq__(self, other):
        return self.id == other


class PhyloGeneticTree:
    def __init__(self, D):
        self.tree_nodes = {}
        self.clusters = {}
        self.D = D
        self.D_leaves = D[:]
        self.n_nodes = len(self.D) - 1
        self.index_to_id = []
        self.age_matrix = None
        
        for i in range(len(self.D)):
            node = Node(i, 0)
            self.tree_nodes[i] = node
            self.clusters[i] = [node]
            self.index_to_id.append(i)
    
    def find_closest_clusters(self):
        min_value = math.inf
        i_min = None
        j_min = None
        for i in range(len(self.D)):
            for j in range(i + 1, len(self.D)):
                if self.D[i][j] < min_value:
                    min_value = self.D[i][j]
                    i_min = i
                    j_min = j
        return i_min, j_min
    
    def merge_two_clusters(self, i_min, j_min):
        self.n_nodes += 1
        new_node_id = self.n_nodes
        i_id = self.index_to_id[i_min]
        j_id = self.index_to_id[j_min]
        
        age = self.D[i_min][j_min] / 2
        new_node = Node(new_node_id, age)

        # remove i and j clusters
        c_i = self.clusters.pop(i_id)
        c_j = self.clusters.pop(j_id)
        
        self.clusters[new_node_id] = c_i[:] + c_j[:]
        return new_node, c_i, c_j
    
    def add_node_to_tree(self, node, i_min, j_min):
        i_id = self.index_to_id[i_min]
        j_id = self.index_to_id[j_min]
        
        i_node = self.tree_nodes[i_id]
        j_node = self.tree_nodes[j_id]
        node.children.append(i_node)
        node.children.append(j_node)
        
        self.tree_nodes[node.id] = node
        del self.tree_nodes[i_id]
        del self.tree_nodes[j_id]
    
    def remove_Cij_from_D(self, i_min, j_min):
        self.old_D = self.D[:]
        del self.D[i_min]
        del self.D[j_min-1]
        for i in range(len(self.D)):
            del self.D[i][i_min]
            del self.D[i][j_min-1]
        
        del self.index_to_id[i_min]
        del self.index_to_id[j_min-1]
    
    def add_new_row_D(self, i_min, i_cluster, j_min, j_cluster, new_id):
        new_row = []
        
        indices = list(range(len(self.old_D)))
        indices.remove(i_min)
        indices.remove(j_min)
        
        for m in indices:
            d = self.calculate_distance_clusters(i_min, i_cluster, j_min, j_cluster, m)
            new_row.append(d)
        
        for i in range(len(self.D)):
            self.D[i].append(new_row[i])
        
        new_row.append(0)
        self.D.append(new_row)
        
        self.index_to_id.append(new_id)
    
    def calculate_distance_clusters(self, i_min, i_cluster, j_min, j_cluster, m):
        # between m and merging i and j
        D = self.old_D
        C1_len = len(i_cluster)
        C2_len = len(j_cluster)
        
        d1 = D[i_min][m]
        d2 = D[j_min][m]
        return (d1 * C1_len + d2 * C2_len) / (C1_len + C2_len)
        
    def age_dfs(self, parent, node):
        if parent is not None:
            edge_age = parent.age - node.age
            self.age_matrix[parent.id][node.id] = edge_age
            self.age_matrix[node.id][parent.id] = edge_age
        
        for child in node.children:
            self.age_dfs(node, child)
    
    def print(self):
        for i in range(len(self.age_matrix)):
            for j in range(len(self.age_matrix)):
                if self.age_matrix[i][j] is not None:
                    print(str(i) + "->" + str(j) + ":" + str(round(self.age_matrix[i][j], 2)))
    
    def upgma(self):
        while len(self.clusters) > 1:
            i_min, j_min = self.find_closest_clusters()
            new_node, i_cluster, j_cluster = self.merge_two_clusters(i_min, j_min)
            self.add_node_to_tree(new_node, i_min, j_min)
            self.remove_Cij_from_D(i_min, j_min)
            self.add_new_row_D(i_min, i_cluster, j_min, j_cluster, new_node.id)
        
        assert len(self.tree_nodes) == 1
        
        self.age_matrix = [[None] * (self.n_nodes + 1) for _ in range(self.n_nodes+1)]
        root = list(self.tree_nodes.keys())[0]
        
        self.age_dfs(None, self.tree_nodes[root])
        self.print()
        

if __name__ == '__main__':
    with open("../neighbor_joining/dataset_10333_7.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        
        D = []
        
        for line in file:
            line = line.rstrip('\n')
            line = line.split()
            
            row = [int(num) for num in line]
            D.append(row)
        
        # print(D)
        
        phylo_tree = PhyloGeneticTree(D)
        phylo_tree.upgma()
