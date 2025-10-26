from models import State
from constants import ROOM_POS


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
