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
    nodes = set()

    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)
        nodes.add(node1)
        nodes.add(node2)

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

        gateway_dists.sort(key=lambda x: (x[1], x[0]))
        return gateway_dists[0][0]

    def find_virus_move(pos, target_gw):
        """Определяет следующий ход вируса"""
        dist_from_gw = {}
        prev = {}
        queue = deque([target_gw])
        dist_from_gw[target_gw] = 0
        prev[target_gw] = None

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in dist_from_gw:
                    dist_from_gw[neighbor] = dist_from_gw[current] + 1
                    prev[neighbor] = current
                    queue.append(neighbor)

        if pos not in dist_from_gw:
            return None

        current_dist = dist_from_gw[pos]
        candidates = []

        for neighbor in graph[pos]:
            if neighbor in dist_from_gw and dist_from_gw[neighbor] == current_dist - 1:
                candidates.append(neighbor)

        return min(candidates) if candidates else None

    def get_all_gateway_links():
        links = []
        for gw in sorted(gates):
            for node in sorted(graph[gw]):
                links.append(f"{gw}-{node}")
        return links

    def is_critical_link(gw, node, virus_position):
        if node == virus_position:
            return True

        graph[gw].remove(node)
        graph[node].remove(gw)

        distances = bfs_distances(virus_position)
        path_exists = gw in distances

        graph[gw].append(node)
        graph[node].append(gw)

        return not path_exists

    def find_best_link_to_cut(virus_position, target_gw):
        gateway_links = get_all_gateway_links()

        critical_links = []
        for link in gateway_links:
            gw, node = link.split('-')
            if is_critical_link(gw, node, virus_position):
                critical_links.append(link)

        if critical_links:
            return min(critical_links)

        target_distances = bfs_distances(target_gw)
        path_links = []

        for link in gateway_links:
            gw, node = link.split('-')
            if node in target_distances:
                path_links.append(link)

        if path_links:
            return min(path_links)

        return min(gateway_links) if gateway_links else None

    while True:
        immediate_threats = []
        for neighbor in graph[virus]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{virus}")

        if immediate_threats:
            action = min(immediate_threats)
            result.append(action)
            gw, node = action.split('-')
            graph[gw].remove(node)
            graph[node].remove(gw)
            continue

        target_gateway = find_target_gateway(virus)
        if target_gateway is None:
            break

        best_action = find_best_link_to_cut(virus, target_gateway)
        if best_action is None:
            break

        result.append(best_action)
        gw, node = best_action.split('-')
        graph[gw].remove(node)
        graph[node].remove(gw)

        new_target = find_target_gateway(virus)
        if new_target is None:
            break

        next_node = find_virus_move(virus, new_target)
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
