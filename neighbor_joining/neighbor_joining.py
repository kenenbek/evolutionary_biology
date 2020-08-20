import math
import copy


class Node:
    def __init__(self, id):
        self.id = id


class PhyloTree:
    def __init__(self, n):
        self.node_index = n - 1
        self.tree = None
        self.adjacency_matrix = []
        self.index_to_id = []
        
        for i in range(n):
            row = [None for _ in range(n)]
            self.adjacency_matrix.append(row)
            self.index_to_id.append(i)
    
    def create_d_star(self, D):
        D_star = copy.deepcopy(D)
        n = len(D)
        for i in range(n):
            for j in range(n):
                D_star[i][j] = (n - 2) * D[i][j] - self.total_distance(D, i) - self.total_distance(D, j)
        return D_star
    
    def total_distance(self, D, i):
        return sum(D[i])
    
    def find_min_D_star(self, D_star):
        minx = math.inf
        i_min = None
        j_min = None
        for i in range(len(D_star)):
            for j in range(i + 1, len(D_star)):
                if D_star[i][j] < minx:
                    minx = D_star[i][j]
                    i_min = i
                    j_min = j
        return i_min, j_min
    
    def add_new_row_column(self, D, i_min, j_min):
        row = []
        for k in range(len(D)):
            row.append(0.5 * (D[k][i_min] + D[k][j_min] - D[i_min][j_min]))
        
        for i in range(len(D)):
            D[i].append(row[i])
        
        row.append(0)
        D.append(row)
        
        self.node_index += 1
        self.index_to_id.append(self.node_index)
        
        # adjacency_matrix
        n = len(self.adjacency_matrix)
        new_row = [None for _ in range(n + 1)]
        
        for row in range(n):
            self.adjacency_matrix[row].append(None)
        
        self.adjacency_matrix.append(new_row)
        return D
    
    def delete_i_j_row_column(self, D, i_min, j_min):
        for k in range(len(D)):
            del D[k][i_min]
            del D[k][j_min - 1]
        del D[i_min]
        del D[j_min - 1]
        
        del self.index_to_id[i_min]
        del self.index_to_id[j_min - 1]
        return D
    
    def add_edge(self, i, j, edge):
        self.adjacency_matrix[i][j] = edge
        self.adjacency_matrix[j][i] = edge
    
    def print(self):
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] is not None:
                    print(str(i) + "->" + str(j) + ":" + str(round(self.adjacency_matrix[i][j], 2)))
    
    def neighbor_joining(self, D):
        n = len(D)
        if n == 2:
            i_ind = self.index_to_id[0]
            j_ind = self.index_to_id[1]
            self.add_edge(i_ind, j_ind, D[0][1])
            return
        D_star = self.create_d_star(D)
        i_min, j_min = self.find_min_D_star(D_star)
        i_ind = self.index_to_id[i_min]
        j_ind = self.index_to_id[j_min]
        delta = (self.total_distance(D, i_min) - self.total_distance(D, j_min)) / (n - 2)
        
        limb_length_i = 0.5 * (D[i_min][j_min] + delta)
        limb_length_j = 0.5 * (D[i_min][j_min] - delta)
        
        D = self.add_new_row_column(D, i_min, j_min)
        m = self.index_to_id[-1]
        D = self.delete_i_j_row_column(D, i_min, j_min)
        self.neighbor_joining(D)
        
        self.add_edge(i_ind, m, limb_length_i)
        self.add_edge(j_ind, m, limb_length_j)


if __name__ == '__main__':
    with open("dataset_10333_7.txt") as file:
        n_leaves = int(file.readline().rstrip('\n'))
        
        D = []
        
        for line in file:
            line = line.rstrip('\n')
            line = line.split()
            
            row = [int(num) for num in line]
            D.append(row)
        
        print(D)
        
        p = PhyloTree(len(D))
        
        p.neighbor_joining(D)
        
        p.print()
