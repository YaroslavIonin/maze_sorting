from constants import TARGET_CHARS


def is_room_done(
        room: tuple[str, str],
        room_pos: int,
):
    return all(char == TARGET_CHARS[room_pos] for char in room)
