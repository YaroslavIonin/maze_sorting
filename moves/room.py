from models import State
from utils import get_cost


def move_from_hall_to_room(
        state: State,
        char: str,
        start_pos: int,
        target_pos: int,
        room_idx: int,
        target_room_idx: int,
) -> tuple[State, int]:
    cost = get_cost(
        char=char,
        start_pos=start_pos,
        target_pos=target_pos,
        extra_step=target_room_idx,
    )

    # новые комнаты
    new_rooms = list(map(list, state.rooms))
    new_rooms[room_idx][target_room_idx] = char
    new_rooms = tuple(map(tuple, new_rooms))

    # новый коридор
    new_hall = list(state.hallway)
    new_hall[start_pos] = '.'
    new_hall = tuple(new_hall)

    new_state = State(
        hallway=new_hall,
        rooms=new_rooms,
    )

    return new_state, cost
