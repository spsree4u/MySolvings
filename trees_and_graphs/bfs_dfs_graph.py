
# BFS and DFS in a Graph


from collections import defaultdict


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, a, b):
        self.graph[a].append(b)

    def bfs(self, start):
        visited = [False] * len(self.graph)

        queue = list()
        queue.append(start)
        visited[start] = True

        while queue:
            start = queue.pop(0)
            print(start, end=" ")

            for i in self.graph[start]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True

    def dfs(self, start):
        visited = [False] * len(self.graph)
        self.dfs_lib(start, visited)

    def dfs_lib(self, v, visited):
        print(v, end=" ")
        visited[v] = True

        for i in self.graph[v]:
            if not visited[i]:
                self.dfs_lib(i, visited)

    def dfs_for_disconnected_graph(self):
        """To be learn more"""
        visited = [False] * len(self.graph)
        for i in range(len(self.graph)):
            if not visited[i]:
                self.dfs_lib(i, visited)

    def bfs_for_disconnected_graph(self):
        """To be implemented"""
        pass


g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(2, 0)
g.add_edge(2, 3)
g.add_edge(3, 3)

print("Following is Breadth First Traversal"
      " (starting from vertex 2)")
g.bfs(2)
print("\nFollowing is DFS from (starting from vertex 2)")
g.dfs(2)
# g.dfs_for_disconnected_graph(2)
