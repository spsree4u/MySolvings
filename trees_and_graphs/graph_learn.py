
# Basic representations of a Graph
"""
Uses:
Graphs are used to represent networks. The networks may include paths in a
city or telephone network or circuit network. Graphs are also used in social
networks like linkedIn, Facebook. For example, in Facebook, each person is
represented with a vertex(or node). Each node is a structure and contains
information like person id, name, gender and locale.
"""


# Adjacency list representation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Graph:
    def __init__(self, num_of_vertices):
        self.number_of_vertices = num_of_vertices
        # each element is adjacency list - a node which points to it's children
        self.graph = [None] * self.number_of_vertices

    def add_edge(self, src, dst):
        # create destination node
        node = Node(dst)
        # point created node's next to source node
        node.next = self.graph[src]
        # update source node
        self.graph[src] = node

        # repeat the above steps from src to dst as graph is not directional
        node = Node(src)
        node.next = self.graph[dst]
        self.graph[dst] = node

    def show_graph(self):
        print(self.graph)
        for i in range(self.number_of_vertices):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" ->  {} ".format(temp.data), end="")
                temp = temp.next
            print(" \n")


V = 5
graph = Graph(V)
graph.add_edge(0, 1)
graph.add_edge(0, 4)
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 3)
graph.add_edge(3, 4)

graph.show_graph()


# A simple representation of graph using Adjacency Matrix
# https://ide.geeksforgeeks.org/9je5j6jJ13
class Graph2:
    def __init__(self, numvertex):
        self.adjMatrix = [[-1] * numvertex for _ in range(numvertex)]
        self.numvertex = numvertex
        self.vertices = {}
        self.verticeslist = [0] * numvertex

    def set_vertex(self, vtx, vtx_id):
        if 0 <= vtx <= self.numvertex:
            self.vertices[vtx_id] = vtx
            self.verticeslist[vtx] = vtx_id

    def set_edge(self, frm, to, cost=0):
        frm = self.vertices[frm]
        to = self.vertices[to]
        self.adjMatrix[frm][to] = cost
        # for directed graph do not add this
        self.adjMatrix[to][frm] = cost

    def get_vertex(self):
        return self.verticeslist

    def get_edges(self):
        edges = []
        for i in range(self.numvertex):
            for j in range(self.numvertex):
                if self.adjMatrix[i][j] != -1:
                    edges.append((self.verticeslist[i], self.verticeslist[j],
                                  self.adjMatrix[i][j]))
        return edges

    def get_matrix(self):
        return self.adjMatrix


G = Graph2(6)
G.set_vertex(0, 'a')
G.set_vertex(1, 'b')
G.set_vertex(2, 'c')
G.set_vertex(3, 'd')
G.set_vertex(4, 'e')
G.set_vertex(5, 'f')
G.set_edge('a', 'e', 10)
G.set_edge('a', 'c', 20)
G.set_edge('c', 'b', 30)
G.set_edge('b', 'e', 40)
G.set_edge('e', 'd', 50)
G.set_edge('f', 'e', 60)
print("Vertices of Graph")
print(G.get_vertex())
print("Edges of Graph")
print(G.get_edges())
print("Adjacency Matrix of Graph")
print(G.get_matrix())
