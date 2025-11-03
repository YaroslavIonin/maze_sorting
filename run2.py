import sys
import collections


def bfs(graph, root):
    queue = collections.deque([root])
    distance = {
        root: [0, []]
    }
    while queue:
        vertex = queue.popleft()
        for neighbour in sorted(graph[vertex]):
            if neighbour not in distance:
                path = distance[vertex][1] + [neighbour]
                distance[neighbour] = [
                    distance[vertex][0] + 1,
                    path
                ]
                queue.append(neighbour)
    return distance


def get_next_step(graph, current):
    distance = bfs(graph, current)
    upper_distance = {node: dist for node, dist in distance.items() if node.isupper()}
    if not upper_distance:
        return None

    def custom_sort(item):
        key_, value_ = item
        number = value_[0]
        letters_list = value_[1]

        return number, key_, letters_list

    upper_distance = dict(sorted(upper_distance.items(), key=custom_sort))
    next_step = None
    for key, value in upper_distance.items():
        next_step = key, value
        break
    return next_step


def solve(edges):
    graph = collections.defaultdict(list)
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)

    virus = 'a'
    result = []

    while True:
        # print("Шаг 1")
        next_step = get_next_step(graph, virus)
        if next_step is None:
            # print("Нет больше заглавных узлов")
            break
        # else:
        # print("Следующий шаг:")
        # print(next_step)

        target_node, (_, path) = next_step
        if len(path) < 2:
            target_node_neighbour = virus
        else:
            target_node_neighbour = path[-2]
        # print(
        #     "target_node", f"{target_node}\n",
        #     "path", f"{path}\n",
        #     "target_node_neighbour", f"{target_node_neighbour}",
        # )

        # Отключаю узел
        # print("Граф до отключения узла")
        # print(graph)
        graph[target_node].remove(target_node_neighbour)
        graph[target_node_neighbour].remove(target_node)
        result.append(f"{target_node}-{target_node_neighbour}")
        # print("Граф после отключения узла")
        # print(graph)

        # Шаг вируса
        next_step = get_next_step(graph, virus)
        if next_step is None:
            # print("Нет больше заглавных узлов")
            break
        # else:
        #     print("Шаг вируса:")
        #     print(next_step)

        _, (_, path) = next_step
        virus = path[0]
        # print("Вирус шагает на", virus)
        # break
        # print()

    # print()
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
