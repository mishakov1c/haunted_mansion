import dataclasses
from coin import Coin
from enemies import Ghost
from player import Player
from pygame.sprite import Group


@dataclasses.dataclass
class GameContext:
    walls: Group
    coin: Coin
    player: Player
    # empty_cells_coordinates: list[tuple[int, int]]
    score: int
    ghosts: list[Ghost]
