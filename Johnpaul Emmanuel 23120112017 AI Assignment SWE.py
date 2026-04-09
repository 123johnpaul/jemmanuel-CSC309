import heapq
from collections import deque

# --------- Graph Definition ---------
graph = {
    'A': {'B': 2, 'C': 5, 'D': 1},
    'B': {'A': 2, 'D': 2, 'E': 3},
    'C': {'A': 5, 'D': 2, 'F': 3},
    'D': {'A': 1, 'B': 2, 'C': 2, 'E': 1, 'F': 4},
    'E': {'B': 3, 'D': 1, 'G': 2},
    'F': {'C': 3, 'D': 4, 'G': 1},
    'G': {'E': 2, 'F': 1, 'H': 3},
    'H': {'G': 3}
}

heuristic = {
    'A': 7,
    'B': 6,
    'C': 6,
    'D': 4,
    'E': 2,
    'F': 2,
    'G': 1,
    'H': 0
}

start = 'A'
goal = 'H'

# -----------------------------
# DFS
# -----------------------------
def dfs(graph, start, goal):
    stack = [(start, [start], 0)]
    visited = set()
    nodes = 0

    while stack:
        node, path, cost = stack.pop()
        nodes += 1

        if node == goal:
            return path, cost, nodes

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                stack.append((neighbor, path + [neighbor], cost + weight))

    return None, float('inf'), nodes


# -----------------------------
# BFS (ignores weights)
# -----------------------------
def bfs(graph, start, goal):
    queue = deque([(start, [start], 0)])
    visited = set()
    nodes = 0

    while queue:
        node, path, cost = queue.popleft()
        nodes += 1

        if node == goal:
            return path, cost, nodes

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                queue.append((neighbor, path + [neighbor], cost + weight))

    return None, float('inf'), nodes


# -----------------------------
# UCS
# -----------------------------
def ucs(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()
    nodes = 0

    while pq:
        cost, node, path = heapq.heappop(pq)
        nodes += 1

        if node == goal:
            return path, cost, nodes

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return None, float('inf'), nodes


# -----------------------------
# A*
# -----------------------------
def a_star(graph, heuristic, start, goal):
    pq = [(heuristic[start], 0, start, [start])]
    visited = set()
    nodes = 0

    while pq:
        f, cost, node, path = heapq.heappop(pq)
        nodes += 1

        if node == goal:
            return path, cost, nodes

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                g = cost + weight
                h = heuristic[neighbor]
                heapq.heappush(pq, (g + h, g, neighbor, path + [neighbor]))

    return None, float('inf'), nodes


# -----------------------------
# RUN & COMPARE
# -----------------------------
def print_result(name, result):
    path, cost, nodes = result
    print(f"\n{name}")
    print("-" * 30)
    print(f"Path: {' -> '.join(path)}")
    print(f"Total Cost: {cost}")
    print(f"Nodes Expanded: {nodes}")


def compare():
    dfs_res = dfs(graph, start, goal)
    bfs_res = bfs(graph, start, goal)
    ucs_res = ucs(graph, start, goal)
    astar_res = a_star(graph, heuristic, start, goal)

    print("\n=== INDIVIDUAL RESULTS ===")
    print_result("DFS", dfs_res)
    print_result("BFS", bfs_res)
    print_result("UCS", ucs_res)
    print_result("A*", astar_res)

    print("\n=== COMPARISON SUMMARY ===")
    print("-" * 50)
    print(f"{'Algorithm':<10}{'Cost':<10}{'Nodes':<10}{'Optimal':<10}")

    results = {
        "DFS": dfs_res,
        "BFS": bfs_res,
        "UCS": ucs_res,
        "A*": astar_res
    }

    optimal_cost = min(r[1] for r in results.values())

    for name, (path, cost, nodes) in results.items():
        optimal = "Yes" if cost == optimal_cost else "No"
        print(f"{name:<10}{cost:<10}{nodes:<10}{optimal:<10}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    compare()