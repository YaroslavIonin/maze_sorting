from utils import get_cost
from models import State, MoveDirection


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
