from copy import deepcopy
# Python3 implementation of the above approach
v = [[] for i in range(100)]


# An utility function to add an edge in an
# undirected graph.
def addEdge(x, y):
    v[x].append(y)
    v[y].append(x)


def DFS(prev, x, y, stack, find=False):
    if not find:
        stack.append(x)
        if x == y:
            return True
        
        for child in v[x]:
            if not find:
                if prev != child:
                    find = DFS(x, child, y, stack, find)
        
        if not find:
            del stack[-1]
    return find


def DFSCall(x, y, stack):
    DFS(None, x, y, stack)
    print(stack)


if __name__ == '__main__':
    # Driver Code
    n = 10
    stack = []
    
    # Vertex numbers should be from 1 to 9.
    addEdge(1, 2)
    addEdge(1, 3)
    addEdge(2, 4)
    addEdge(2, 5)
    addEdge(2, 6)
    addEdge(3, 7)
    addEdge(3, 8)
    addEdge(3, 9)
    
    # Function Call
    DFSCall(7, 1, [])