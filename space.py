from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
    from player import Player

class Space:
    def __init__(self, id: str, value: int, side: int, on_land: Callable[['Player', 'Game'], None] = None, rent: Callable[['Player', 'Game'], int] = None):
        self.id = id
        self.value = value
        self.houses = 0
        self.side = side

        if on_land is None:
            self.on_land = lambda player, game: None
        else:
            self.on_land = on_land
        
        if rent is None:
            self.rent = lambda player, game: 0
        else:
            self.rent = rent
        
        self.owner: 'Player' | None = None
        self.mortgaged = False
        self.set = self.id[:-1]
