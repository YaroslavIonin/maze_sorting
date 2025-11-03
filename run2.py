import sys
from collections import deque


def find_virus_move(start, target, graph):
    prev_nodes = {
        start: None,
    }
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in sorted(graph.get(current, [])):
            if neighbor not in prev_nodes:
                prev_nodes[neighbor] = current
                queue.append(neighbor)

    if target not in prev_nodes:
        return None

    path = []
    while target:
        path.append(target)
        target = prev_nodes[target]
    return list(reversed(path))


def find_gate(virus, gates, graph):
    best = None
    for gw in gates:
        path = find_virus_move(virus, gw, graph)
        if not path:
            continue
        dist = len(path) - 1
        if best is None or (dist, gw) < (best[0], best[1]):
            best = (dist, gw, path)
    return best


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
        next_move = find_gate(virus, gates, graph)
        if not next_move:
            break

        dist, gate, path = next_move
        if len(path) < 2:
            break

        cut_node = path[-2]
        result.append(f"{gate}-{cut_node}")
        graph[gate].remove(cut_node)
        graph[cut_node].remove(gate)

        next_move = find_gate(virus, gates, graph)
        if not next_move:
            break

        _, _, path = next_move

        if len(path) > 1:
            virus = path[1]

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
