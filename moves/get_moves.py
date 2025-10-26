from models import State, MoveDirection
from checks import is_path_clear, is_room_available
from constants import (
    STOP_POS,
    ROOM_POS,
    TARGET_STATE, TARGET_ROOM,
)

from moves.get_move import move


def get_moves_from_room_to_hall(
        state: State,
) -> list[tuple[State, int]]:
    moves = []

    # варианты ходов из комнат в коридор
    for i, room in enumerate(state.rooms):
        # если комната готова - скипаем её
        if room == TARGET_STATE.rooms[i]:
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
