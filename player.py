from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from card import Card
    from game import Game
    from space import Space

class Player:
    def __init__(self, id: int, piece: str):
        self.id = id
        self.piece = piece
        self.space = 0
        self.money = 1500
        self.properties: list['Space'] = []
        self.jail_free_cards: list['Card'] = []
        self.in_jail = False
        self.turns_in_jail = 0
        self.doubles_rolled = 0
        self.bankrupt = False
    
    def buy_property(self, space: 'Space', game: 'Game') -> bool:
        if self.money >= space.value:
            return True
        else:
            return False
        
    def lose(self, other: 'Player', game: 'Game'):
        for prop in self.properties.copy():
            prop.owner = other
            other.properties.append(prop)
        self.properties = []
        self.pay(self.money, other, game)
        other.jail_free_cards += self.jail_free_cards
        self.bankrupt = True
    
    def pay(self, rent: int, other: 'Player', game: 'Game'):
        if (self.money >= rent):
            self.money -= rent
            other.money += rent
        else:
            all_mortgaged = False
            while (self.money < rent and not all_mortgaged):
                for i, prop in enumerate(sorted(self.properties, key=lambda x: x.value)):
                    if not prop.mortgaged and ((prop.value // 2 + self.money) >= rent or all([prop.mortgaged for prop in self.properties[i+1:]])):
                        if prop.houses == 0:
                            game.mortgage_property(self, prop)
                        else:
                            game.sell_house(self, prop)
                        break
                all_mortgaged = all([prop.mortgaged for prop in self.properties])
            
            if not all_mortgaged:
                self.money -= rent
                other.money += rent
            else:
                self.lose(other, game)
    
    # 0 represents the player choosing not to bid
    # -1 represents the player not having enough money to bid
    # any other number represents the player's bid
    def make_auction_bid(self, bid: int, space: 'Space', game: 'Game') -> int:
        if bid > self.money:
            return -1
        else:
            set_matches = sum([1 for prop in self.properties if prop.set == space.set])

            if set_matches == 1:
                return bid + 5
            elif set_matches == 2:
                return bid + 10
            elif bid < space.value:
                return bid + 1
            
            return 0
    
    def doubles_or_pay_or_jfc(self, game: 'Game'):
        if self.turns_in_jail == 3 or game.turns < 25:
            if len(self.jail_free_cards) > 0:
                return 2
            else:
                return 1
        else:
            return 0
    
    def use_jail_free_card(self, game: 'Game'):
        card_to_use = self.jail_free_cards.pop(0)

        self.in_jail = False
        self.turns_in_jail = 0
        self.doubles_rolled = 0
        game.jail.remove(self)

        if (card_to_use.id == "9"):
            game.chance.append(card_to_use)
        else:
            game.community_chest.append(card_to_use)
