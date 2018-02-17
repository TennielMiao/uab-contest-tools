

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
   

    
        
 
    
g=Graph()    
g.add_edge('a','b')
g.add_edge('b','c')
g.add_edge('c','d')
g.add_edge('a','e')
g.add_edge('d','e')
g.add_edge('c','e')



print g.find_path("a","c")
print g.min_path("a","c")
print g.all_paths("a","c")
print g.cnntd_cmpt("b")
print g.rec_any_path("a")



