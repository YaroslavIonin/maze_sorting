from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    hallway: tuple[str, ...]
    rooms: tuple[tuple[str, str], ...]
