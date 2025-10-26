from models import State
from utils import get_cost


def move_from_room_to_hall(
        state: State,
        char: str,
        start_pos: int,
        target_pos: int,
        room_idx: int,
        char_room_idx: int,
) -> tuple[State, int]:
    cost = get_cost(
        char=char,
        start_pos=start_pos,
        target_pos=target_pos,
        extra_step=char_room_idx,
    )

    # новые комнаты
    new_rooms = list(map(list, state.rooms))
    new_rooms[room_idx][char_room_idx] = '.'
    new_rooms = tuple(map(tuple, new_rooms))

    # новый коридор
    new_hall = list(state.hallway)
    new_hall[target_pos] = char
    new_hall = tuple(new_hall)

    new_state = State(
        hallway=new_hall,
        rooms=new_rooms,
    )
    return new_state, cost
