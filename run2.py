import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    gates = set()

    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)
        if node1.isupper():
            gates.add(node1)
        if node2.isupper():
            gates.add(node2)

    virus = 'a'
    result = []

    def bfs_shortest_path(start, target):
        if start == target:
            return [start]

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()
            for neighbor in sorted(graph[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == target:
                        return new_path
                    queue.append((neighbor, new_path))
        return None

    def find_target_gateway(virus_pos):
        min_dist = float('inf')
        target_gate = None

        for gate in sorted(gates):
            path = bfs_shortest_path(virus_pos, gate)
            if path and len(path) < min_dist:
                min_dist = len(path)
                target_gate = gate
            elif path and len(path) == min_dist and (target_gate is None or gate < target_gate):
                target_gate = gate

        return target_gate

    def get_gateway_links():
        links = []
        for gate in sorted(gates):
            for node in sorted(graph[gate]):
                links.append(f"{gate}-{node}")
        return links

    while True:
        immediate_threats = []
        for neighbor in graph[virus]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{virus}")

        if immediate_threats:
            action = min(immediate_threats)
            result.append(action)
            gate, node = action.split('-')
            graph[gate].remove(node)
            graph[node].remove(gate)
            continue

        target_gate = find_target_gateway(virus)
        if target_gate is None:
            break  # No path to any gateway

        critical_links = []
        all_gateway_links = get_gateway_links()

        for link in all_gateway_links:
            gate, node = link.split('-')
            graph[gate].remove(node)
            graph[node].remove(gate)

            path_exists = bfs_shortest_path(virus, target_gate) is not None

            graph[gate].append(node)
            graph[node].append(gate)

            if not path_exists:
                critical_links.append(link)

        if critical_links:
            action = min(critical_links)
        else:
            if all_gateway_links:
                action = min(all_gateway_links)
            else:
                break

        result.append(action)
        gate, node = action.split('-')
        graph[gate].remove(node)
        graph[node].remove(gate)

        target_gate_after_cut = find_target_gateway(virus)
        if target_gate_after_cut is None:
            break

        path = bfs_shortest_path(virus, target_gate_after_cut)
        if path and len(path) > 1:
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
