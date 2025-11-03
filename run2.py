import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
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
        distances = {start: 0}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances

    def find_target_gateway(pos):
        distances = bfs_distances(pos)
        gateway_dists = [(gw, distances[gw]) for gw in gates if gw in distances]

        if not gateway_dists:
            return None

        min_dist = min(dist for _, dist in gateway_dists)
        candidates = [gw for gw, dist in gateway_dists if dist == min_dist]

        candidates.sort()
        return candidates[0]

    def find_next_node(pos, target_gw):
        distances = bfs_distances(target_gw)

        candidates = []
        current_dist = distances[pos]

        for neighbor in sorted(graph[pos]):
            if neighbor in distances and distances[neighbor] == current_dist - 1:
                candidates.append(neighbor)

        return candidates[0] if candidates else None

    def get_gateway_links():
        links = []
        for gate in sorted(gates):
            for node_ in sorted(graph[gate]):
                links.append(f"{gate}-{node_}")
        return links

    while True:
        target_gateway = find_target_gateway(virus)
        if target_gateway is None:
            break

        critical_links = []
        for neighbor in graph[virus]:
            if neighbor in gates:
                critical_links.append(f"{neighbor}-{virus}")

        if critical_links:
            action = min(critical_links)
            result.append(action)

            gw, node = action.split('-')
            graph[gw].remove(node)
            graph[node].remove(gw)

            continue

        all_gateway_links = get_gateway_links()

        if not all_gateway_links:
            break

        target_path_distances = bfs_distances(target_gateway)

        best_links = []
        for link in all_gateway_links:
            gw, node = link.split('-')
            if node in target_path_distances:
                best_links.append(link)

        action = min(best_links) if best_links else min(all_gateway_links)
        result.append(action)

        gw, node = action.split('-')
        graph[gw].remove(node)
        graph[node].remove(gw)

        new_target = find_target_gateway(virus)
        if new_target is None:
            break

        next_node = find_next_node(virus, new_target)
        if next_node is None:
            break

        virus = next_node

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
