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

    reachable_gates = []
    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                prev_nodes[neighbor] = current
                queue.append(neighbor)

                for gate in gates:
                    if gate in graph[neighbor]:
                        reachable_gates.append((distances[neighbor] + 1, gate, neighbor))

    if not reachable_gates:
        return None

    reachable_gates.sort()
    return reachable_gates[0][1:]


def find_path(start, target, graph):
    queue = deque([start])
    par = {start: None}
    while queue:
        cur = queue.popleft()
        if cur == target:
            break
        for nxt in sorted(graph[cur]):
            if nxt not in par:
                par[nxt] = cur
                queue.append(nxt)
    path_ = []
    x = target
    while x is not None:
        path_.append(x)
        x = par[x]
    return list(reversed(path_))


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
        next_move = find_virus_move(virus, graph, gates)
        if next_move:
            gate, neighbor = next_move
        else:
            possible = [(gate, neighbor) for gate in gates for neighbor in graph[gate]]
            if not possible:
                break
            possible.sort()
            gate, neighbor = possible[0]

        result.append(f"{gate}-{neighbor}")
        graph[gate].remove(neighbor)
        graph[neighbor].remove(gate)

        next_move = find_virus_move(virus, graph, gates)
        if next_move:
            target_gate = next_move[1]
            path = find_path(virus, target_gate, graph)
            if len(path) > 1:
                virus = path[1]
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
