################################################################################
# constants.py
################################################################################
ROOM_POS = (2, 4, 6, 8)
STOP_POS = (0, 1, 3, 5, 7, 9, 10)
COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET_CHARS = 'ABCD'
TARGET_ROOM = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

################################################################################
# models module
################################################################################
# state.py
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    hallway: tuple[str, ...]
    rooms: tuple[tuple[str, str], ...]


# direction.py
from enum import Enum, auto


class MoveDirection(Enum):
    TO_HALL = auto()
    TO_ROOM = auto()


################################################################################
# checks module
################################################################################
# available_room.py
def is_room_available(
        room: tuple[str, str],
        char: str,
):
    """
    Функция проверяет, свободна ли комната для входа конкретного символа.

    :param room: текущее состояние комнаты

    :param char: целевой символ

    :return: True, если комната свободна, иначе False
    """
    return all(ch in ('.', char) for ch in room)


# clear_path.py
def is_path_clear(
        hall: tuple[str],
        start_pos: int,
        target_pos: int,
) -> bool:
    """
    Функция проверяет свободен ли путь между двумя позициями в коридоре

    :param hall: текущее состояние коридора

    :param start_pos: текущая позиция в коридоре

    :param target_pos: целевая позиция в коридоре

    :return: True, если путь свободен, иначе False
    """
    if start_pos < target_pos:
        path = hall[start_pos + 1:target_pos + 1]
    else:
        path = hall[target_pos:start_pos]
    return all(ch == '.' for ch in path)


# room_done.py
def is_room_done(
        room: tuple[str, str],
        room_pos: int,
):
    return all(char == TARGET_CHARS[room_pos] for char in room)


################################################################################
# moves module
################################################################################
# get_move.py
def move(
        state: State,
        char: str,
        start_pos: int,
        target_pos: int,
        room_idx: int,
        char_room_idx: int,
        direction: MoveDirection,
) -> tuple[State, int]:
    cost = get_cost(
        char=char,
        start_pos=start_pos,
        target_pos=target_pos,
        extra_step=char_room_idx,
    )

    new_rooms = list(map(list, state.rooms))
    new_hall = list(state.hallway)

    if direction == MoveDirection.TO_HALL:
        new_rooms[room_idx][char_room_idx] = '.'
        new_hall[target_pos] = char
    else:
        new_rooms[room_idx][char_room_idx] = char
        new_hall[start_pos] = '.'

    new_rooms = tuple(map(tuple, new_rooms))
    new_hall = tuple(new_hall)

    new_state = State(
        hallway=new_hall,
        rooms=new_rooms,
    )

    return new_state, cost


# get_moves.py
def get_moves_from_room_to_hall(
        state: State,
) -> list[tuple[State, int]]:
    moves = []

    # варианты ходов из комнат в коридор
    for i, room in enumerate(state.rooms):
        # если комната готова - скипаем её
        if is_room_done(room, i):
            continue

        # пеолучаем индекс и первый символ в комнате
        current_char = ''
        current_char_index = 0
        for j, char in enumerate(room):
            if char != '.':
                current_char = char
                current_char_index = j
                break
        # если не находим символ - скипаем комнату
        if current_char == '':
            continue

        # перебираем возможные пути в коридор
        for pos_idx in STOP_POS:
            # если путь занят - скипаем
            if not is_path_clear(
                    hall=state.hallway,
                    start_pos=ROOM_POS[i],
                    target_pos=pos_idx,
            ):
                continue
            moves.append(
                move(
                    state=state,
                    char=current_char,
                    start_pos=ROOM_POS[i],
                    target_pos=pos_idx,
                    room_idx=i,
                    char_room_idx=current_char_index,
                    direction=MoveDirection.TO_HALL,
                )
            )

    return moves


def get_moves_from_hall_to_room(
        state: State,
) -> list[tuple[State, int]]:
    moves = []
    hall = list(state.hallway)
    for i, char in enumerate(hall):
        if char == '.':
            continue

        target_pos = ROOM_POS[TARGET_ROOM[char]]
        if not (
                is_path_clear(
                    hall=state.hallway,
                    start_pos=i,
                    target_pos=target_pos,
                ) and
                is_room_available(
                    room=state.rooms[TARGET_ROOM[char]],
                    char=char,
                )
        ):
            continue

        target_room_idx = -1
        room_idx = TARGET_ROOM[char]
        for j, ch in enumerate(state.rooms[room_idx]):
            if ch == char:
                target_room_idx = j - 1
                break
        if target_room_idx == -1:
            target_room_idx = len(state.rooms[room_idx]) - 1

        moves.append(
            move(
                state=state,
                char=char,
                start_pos=i,
                target_pos=target_pos,
                room_idx=room_idx,
                char_room_idx=target_room_idx,
                direction=MoveDirection.TO_ROOM,
            )
        )

    return moves


def get_moves(
        state: State,
) -> list[tuple[State, int]]:
    all_moves = [
        *get_moves_from_room_to_hall(state),
        *get_moves_from_hall_to_room(state),
    ]
    return all_moves


################################################################################
# utils module
################################################################################
# get_cost.py
def get_cost(
        char: str,
        start_pos: int,
        target_pos: int,
        extra_step: int,
):
    count_steps = abs(start_pos - target_pos) + extra_step + 1
    return count_steps * COST[char]


# parse_inputs.py
def get_base_and_target_states(lines: list[str]) -> tuple[State, State]:
    base_hall = tuple(lines[1][1:-1])
    base_rooms = tuple(
        tuple(line[1:-1][col] for line in lines[2:-1])
        for col in ROOM_POS
    )

    target_hall = tuple('.' * 11)
    target_rooms = tuple(
        tuple(char for _ in range(len(base_rooms[0])))
        for char in 'ABCD'
    )
    return State(base_hall, base_rooms), State(target_hall, target_rooms)


################################################################################
# other module
################################################################################
# memory.py
import tracemalloc


def memory_checker(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(current / 1024 / 1024, peak / 1024 / 1024)
        return result

    return wrapper


# time.py
import time


def time_checker(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Потраченное время: {end_time - start_time:.4f}")
        return result

    return wrapper


################################################################################
# main module
################################################################################
# run.py
import sys
import itertools

from heapq import heappush, heappop


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """

    base_state, target_state = get_base_and_target_states(lines)

    counter = itertools.count()
    heap = [(0, next(counter), base_state)]

    best_moves = {
        base_state: 0,
    }

    while heap:
        cost, _, state = heappop(heap)
        if state == target_state:
            return cost

        if cost > best_moves[state]:
            continue

        moves = get_moves(state)
        for new_state, extra_cost in moves:
            new_cost = cost + extra_cost
            if new_state not in best_moves or new_cost < best_moves[new_state]:
                best_moves[new_state] = new_cost
                heappush(heap, (new_cost, next(counter), new_state))

    return 0


# @time_checker
# @memory_checker
def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
