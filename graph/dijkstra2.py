import math
import heapq


class Node:
    def __init__(self, name, distance=math.inf, prev=None):
        self.name = name
        self.distance = distance
        self.prev = prev

    def __gt__(self, other):
        return self.distance > other.distance

    def __lt__(self, other):
        return self.distance < other.distance


def visit_node(node, conns):
    for conn in conns:
        if node in conn:
            source = conn.index(node)
            target = 1 - source
            if conn[target].distance > conn[source].distance + conn[2]:
                conn[target].distance = conn[source].distance + conn[2]
                conn[target].prev = conn[source]
    

def dijkstra(target, nodes, connections):
    backup = []
    for i in nodes:
        backup.append(i)
    while target in nodes:
        heapq.heapify(nodes)
        node = heapq.heappop(nodes)
        visit_node(node, connections)

    current = target.prev
    print("Go to", target.name)
    while current is not None:
        print("from", current.name)
        current = current.prev
        
    print("Total distance", target.distance)
            

conns = []
s = Node("s", 0)
a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")
f = Node("f")
g = Node("g")
h = Node("h")
i = Node("i")
j = Node("j")
k = Node("k")
l = Node("l")

nodes = [a, b, c, d, e, f, g, h, i, j, k, l, s]

conns.append((s, a, 7))
conns.append((a, b, 3))
conns.append((s, b, 2))
conns.append((b, d, 4))
conns.append((d, f, 5))
conns.append((f, h, 3))
conns.append((b, h, 1))
conns.append((h, g, 2))
conns.append((g, e, 20))
conns.append((s, a, 7))
conns.append((s, c, 3))
conns.append((c, l, 2))
conns.append((l, i, 4))
conns.append((l, j, 4))
conns.append((j, i, 6))
conns.append((i, k, 5))
conns.append((j, k, 4))
conns.append((k, e, 5))

dijkstra(e, nodes, conns)
