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

    def bfs_distances(start):
        distances = {}
        queue = deque([start])
        distances[start] = 0

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances

    def find_target_gateway(virus_position):
        distances = bfs_distances(virus_position)

        reachable_gates = [(gate, distances[gate]) for gate in gates if gate in distances]
        if not reachable_gates:
            return None

        min_dist = min(dist for _, dist in reachable_gates)

        candidate_gates = [gate for gate, dist in reachable_gates if dist == min_dist]
        return min(candidate_gates)

    def find_next_virus_move(virus_position, target_gate):
        distances = bfs_distances(target_gate)

        current_dist = distances[virus_position]
        candidates = []

        for neighbor in sorted(graph[virus_position]):
            if neighbor in distances and distances[neighbor] < current_dist:
                candidates.append(neighbor)

        return min(candidates) if candidates else None

    def get_all_gateway_links():
        links = []
        for gate in sorted(gates):
            for node in sorted(graph[gate]):
                links.append(f"{gate}-{node}")
        return links

    def is_critical_link(link, virus_position, target_gate):
        if not target_gate:
            return True

        gate, node = link.split('-')

        graph[gate].remove(node)
        graph[node].remove(gate)

        distances = bfs_distances(virus_position)
        can_still_reach = target_gate in distances

        graph[gate].append(node)
        graph[node].append(gate)

        return not can_still_reach

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
        if not target_gate:
            break

        all_links = get_all_gateway_links()
        if not all_links:
            break

        critical_links = []
        for link in all_links:
            if is_critical_link(link, virus, target_gate):
                critical_links.append(link)

        if critical_links:
            action = min(critical_links)
        else:
            action = min(all_links)

        result.append(action)
        gate, node = action.split('-')
        graph[gate].remove(node)
        graph[node].remove(gate)

        new_target_gate = find_target_gateway(virus)
        if not new_target_gate:
            break
        next_pos = find_next_virus_move(virus, new_target_gate)
        if not next_pos:
            break

        virus = next_pos

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
