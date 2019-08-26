from collections import defaultdict


def readGraph():
    g = defaultdict(set)
    file = open("edges.txt", "r")
    edges = file.readlines()
    m = len(edges)
    n=0
    for t in edges:
        x,y = map(int,t.split(','))
        n = max(n,max(x,y))
        g[x].add(y)
    file.close()
    return g, n, m

g, n, m = readGraph()

visited = []

def dfs(graph, v):
    visited[v]=True
    for i in graph[v]:
        if visited[i]==False:
            dfs(graph, i)

stack = []
def topological_sort(graph, v):
    visited[v] = True
    for i in graph[v]:
        if visited[i]==False:
            topological_sort(graph, i)
    stack.append(v)

def reverseGraph(graph):
    gT = defaultdict(set)
    for x in graph:
        for y in graph[x]:
            gT[y].add(x)
    return gT


visited = [False]*(n+1)
for i in range(1, n+1):
    if visited[i]==False:
        topological_sort(g,i)

gT = reverseGraph(g)
visited = [False]*(n+1)
count=0
while stack:
    i = stack.pop()
    if visited[i] == False:
        dfs(gT,i)
        count+=1
print("Number of SCC: ", count)
