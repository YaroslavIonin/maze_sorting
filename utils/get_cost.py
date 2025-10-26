from constants import COST


def get_cost(
        char: str,
        start_pos: int,
        target_pos: int,
        extra_step: int,
):
    count_steps = abs(start_pos - target_pos) + extra_step + 1
    return count_steps * COST[char]
