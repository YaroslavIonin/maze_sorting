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
