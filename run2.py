import sys
from collections import deque


def find_virus_move(start, graph, gates):
    distances = {
        start: 0,
    }
    prev_nodes = {
        start: None,
    }
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                prev_nodes[neighbor] = current
                queue.append(neighbor)

    reachable_gates = [g for g in gates if g in distances]
    if not reachable_gates:
        return None

    min_dist = min(distances[g] for g in reachable_gates)
    target_gate = min(list(g for g in reachable_gates if distances[g] == min_dist))

    path = []
    current = target_gate
    while current != start:
        path.append(current)
        current = prev_nodes[current]
    path.reverse()

    return path[0] if path else target_gate


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    graph = {}
    for n1, n2 in edges:
        graph.setdefault(n1, set()).add(n2)
        graph.setdefault(n2, set()).add(n1)

    gates = {node for node in graph if node.isupper()}

    virus = 'a'
    result = []

    while True:
        if virus in gates:
            break

        next_move = find_virus_move(virus, graph, gates)

        candidate_edges = []
        for gate in gates:
            for node in graph.get(gate, set()):
                candidate_edges.append((gate, node))
        candidate_edges.sort()

        found_safe = False
        for gate, node in candidate_edges:
            temp_graph = {}
            for k, v in graph.items():
                temp_graph[k] = v.copy()

            temp_graph[gate].discard(node)
            temp_graph[node].discard(gate)

            next_after_cut = find_virus_move(virus, temp_graph, gates)
            if next_after_cut is None or next_after_cut not in gates:
                result.append(f"{gate}-{node}")
                graph[gate].remove(node)
                graph[node].remove(gate)
                found_safe = True
                break

        if not found_safe and candidate_edges:
            gate, node = candidate_edges[0]
            result.append(f"{gate}-{node}")
            graph[gate].remove(node)
            graph[node].remove(gate)

        if next_move in graph and virus in graph and next_move in graph[virus]:
            virus = next_move
        else:
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
