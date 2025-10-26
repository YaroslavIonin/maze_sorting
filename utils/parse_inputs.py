from models import State
from constants import ROOM_POS


def parse_input_lines(lines: list[str]) -> State:
    hall = tuple(lines[1][1:-1])

    rooms = tuple(
        tuple(line[1:-1][col] for line in lines[2:-1])
        for col in ROOM_POS
    )
    return State(hall, rooms)
