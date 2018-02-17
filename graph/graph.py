from queue import Queue

class Graph(object):

    def __init__(self, isDigraph = False):
        from collections import defaultdict
        self.verts = set()
        self.edges = defaultdict(list)
        self.isDigraph = isDigraph
        self.time = 0 # For bridges
        
    def add_vert(self,v):
        self.verts.add(v)

    def add_edge(self,v0,v1):
        self.verts.add(v0)
        self.verts.add(v1)        
        self.edges[v0].append(v1) 
        if not self.isDigraph:
            self.edges[v1].append(v0) 
         

    def all_paths(self, v0, v1):
#        print "Paths from", v0, "to", v1,"\n\n"
        stack = [(v0, [v0])]
        paths=[]
        while stack:
            (v, path) = stack.pop()
            nbrs = set(self.edges[v]) - set(path)
#            print "nbrs of", v,": ", list(nbrs)
            for nbr in nbrs:
#                print "  visit:", nbr
                if nbr == v1:
                    paths.append(path + [nbr])
#                    print "\n---> final path"," - ".join(paths[-1]),"\n"
           
                else:
#                    print "  path becomes ", " - ".join(path +[nbr])
                    stack.append((nbr, path + [nbr])) 
#                    print    
                                   
        return paths
    
    def find_path(self, v0, v1, path = []):
        path = path + [v0]      
        if v0 == v1:
            return path
        for v in self.edges[v0]:
            if v not in path:
                new_path = self.find_path(v, v1, path)
                if new_path:
                    return new_path
                return None                                        
                    

    
    def rec_any_path(self,v0,path=[]):
        path = path + [v0]
        nbrs = self.edges[v0]
        for nbr in nbrs:
            if nbr not in path:
                path = self.rec_any_path(nbr,path)
        return path
        
  
        
    def min_path(self, v0, v1, path =[]):
        path = path + [v0]
        if v0 == v1:
            return path
        minpath = None
        nbrs = self.edges[v0]
        for nbr in nbrs:
            if nbr not in path:
                temp = self.min_path(nbr, v1, path)
                if temp:
                    if (not minpath) or (len(temp) < len(minpath)):
                        minpath = temp
        return minpath                


    def cnntd_cmpt(self, v0):
        visited, to_visit = set(), [v0]
        while to_visit:
            vert = to_visit.pop()
            if vert not in visited:
                visited.add(vert)
                nbrs_vert = self.edges[vert]
                to_visit.extend(list(set(nbrs_vert) - visited))
        return list(visited)



    ########## DEPTH FIRST SEARCH ##########

    def dfs(self, node, discovered=set(), callback=lambda x: x):
        """
        Traverses a graph or tree, exploring child nodes before exploring
        neighbor nodes. To do something with the nodes, a callback can be passed
        whose output will be returned. Alternatively, add code to make things happen
        :param node: Node to start from
        :param discovered: Discovered set to exclude (optional)
        :param callback: Callback for every node to perform (optional)
        :return:
        """

        if node in discovered:
            return []


        # Add node to discovered set
        discovered.add(node)

        # Create list of results for this subtree
        result = []

        # Do something with the node
        result.append(callback(node))

        # Do the same for every child node
        for child in self.edges[node]:
            result += self.dfs(child, discovered, callback=callback)

        return result


    ########## BREADTH FIRST SEARCH ##########

    def bfs(self, start, target=None, callback=lambda x: x):
        """
        Traverses a graph with or without a target, exploring neighbor nodes first.
        When given a target, it construct a path to the target.
        Code could be added into the while loop to do something with the nodes
        :param problem: The node to search for
        :return:
        """

        # a FIFO open_set
        open_set = []
        # an empty set to maintain visited nodes
        closed_set = set()
        # a dictionary to maintain meta information (used for path formation)
        meta = dict()  # key -> (parent state, action to reach child)

        # initialize
        meta[start] = None
        open_set.append(start)

        res = []

        while not len(open_set) == 0:

            parent = open_set.pop()

            res.append(callback(parent))

            if parent == target:
                return self.construct_path(parent, meta)

            for child in self.edges[parent]:

                if child in closed_set:
                    continue

                if child not in open_set:
                    meta[child] = parent
                    open_set.insert(0, child)

            closed_set.add(parent)
        return res

    def construct_path(self, state, meta):
        action_list = [state]

        while True:
            state = meta[state]
            action_list.append(state)
            if state is None:
                break

        return action_list[::-1]


    ########## BRIDGE FINDING ##########
    '''A recursive function that finds and prints bridges
        using DFS traversal
        u --> The vertex to be visited next
        visited[] --> keeps tract of visited vertices
        disc[] --> Stores discovery times of visited vertices
        parent[] --> Stores parent vertices in DFS tree'''

    def bridge_util(self, u, visited, parent, low, disc):

        # Count of children in current node
        children = 0

        # result
        res = []

        # Mark the current node as visited and print it
        visited[u] = True

        # Initialize discovery time and low value
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        # Recur for all the vertices adjacent to this vertex
        for v in self.edges[u]:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if visited[v] == False:
                parent[v] = u
                children += 1
                res += self.bridge_util(v, visited, parent, low, disc)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                low[u] = min(low[u], low[v])

                ''' If the lowest vertex reachable from subtree
                under v is below u in DFS tree, then u-v is
                a bridge'''
                if low[v] > disc[u]:
                    res.append((u,v))


            elif v != parent[u]:  # Update low value of u for parent function calls.
                low[u] = min(low[u], disc[v])
        return res

    # DFS based function to find all bridges. It uses recursive
    # function bridgeUtil()
    def bridge(self):

        # Mark all the vertices as not visited and Initialize parent and visited,
        # and ap(articulation point) arrays
        visited = [False] * len(self.verts)
        disc = [float("Inf")] * len(self.verts)
        low = [float("Inf")] * len(self.verts)
        parent = [-1] * len(self.verts)

        res = []

        # Call the recursive helper function to find bridges
        # in DFS tree rooted with vertex 'i'
        for i in range(len(self.verts)):
            if visited[i] == False:
                res += self.bridge_util(i, visited, parent, low, disc)
        return res
        
 
    
g=Graph()

g.add_edge(1, 0)
g.add_edge(0, 2)
g.add_edge(2, 1)
g.add_edge(0, 3)
g.add_edge(3, 4)


print(g.find_path(1,4))
print(g.min_path(1,4))
print(g.all_paths(4,2))
print(g.cnntd_cmpt(2))
print(g.rec_any_path(1))

print(g.dfs(2, callback=lambda x: x))
print(g.bfs(2, callback=lambda x: x))

print(g.bridge())



