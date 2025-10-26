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
