import sys
import itertools

from heapq import heappush, heappop

from models import State
from moves import get_moves
from constants import TARGET_STATE
from utils import parse_input_lines


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """

    base_state: State = parse_input_lines(lines)

    counter = itertools.count()
    heap = [(0, next(counter), base_state)]

    best_moves = {
        base_state: 0,
    }

    while heap:
        cost, _, state = heappop(heap)
        if state == TARGET_STATE:
            return cost

        if cost > best_moves[state]:
            continue

        moves = get_moves(state)
        for new_state, extra_cost in moves:
            new_cost = cost + extra_cost
            if new_state not in best_moves or new_cost < best_moves[new_state]:
                best_moves[new_state] = new_cost
                heappush(heap, (new_cost, next(counter), new_state))

    return None


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
