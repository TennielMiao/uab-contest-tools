from queue import Queue

class Graph(object):

    def __init__(self, isDigraph = False):
        from collections import defaultdict
        self.verts = set()
        self.edges = defaultdict(list)
        self.isDigraph = isDigraph
        
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


    def dfs(self, node, discovered=set(), callback=lambda x: []):
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

    def bfs(self, start, target=None):
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

        while not len(open_set) == 0:

            parent_state = open_set.pop()

            if parent_state == target:
                return self.construct_path(parent_state, meta)

            for child in self.edges[parent_state]:

                if child in closed_set:
                    continue

                if child not in open_set:
                    meta[child] = parent_state
                    open_set.insert(0, child)

            closed_set.add(parent_state)

    def construct_path(self, state, meta):
        action_list = [state]

        while True:
            state = meta[state]
            action_list.append(state)
            if state is None:
                break

        return action_list[::-1]


    
        
 
    
g=Graph()    
g.add_edge('a','b')
g.add_edge('b','c')
g.add_edge('c','d')
g.add_edge('a','e')
g.add_edge('d','e')
g.add_edge('c','e')



print(g.find_path("a","c"))
print(g.min_path("a","c"))
print(g.all_paths("a","c"))
print(g.cnntd_cmpt("b"))
print(g.rec_any_path("a"))

print(g.dfs("b", callback=lambda x: 1))
print(g.bfs("b", "c"))



