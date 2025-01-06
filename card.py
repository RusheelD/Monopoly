from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from game import Player, Game

class Card:
    def __init__(self, id: str, text: str, function: str, on_draw: Callable[['Player', 'Game'], bool]):
        self.id = id
        self.text = text
        self.function = function
        self.on_draw = on_draw