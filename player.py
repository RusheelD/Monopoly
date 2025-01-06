from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from card import Card
    from game import Game
    from space import Space

class Player:
    def __init__(self, id: int, piece: str, debug: bool = False, is_ai: bool = True):
        self.debug = debug
        self.is_ai = is_ai
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
        if self.is_ai:
            if self.money >= space.value:
                return True
            else:
                return False
        else:
            # TODO: Get user input
            pass
        
    def lose(self, other: 'Player', game: 'Game'):
        for prop in self.properties.copy():
            prop.owner = other
            other.properties.append(prop)
        self.properties = []
        self.pay(self.money, other, game)
        other.jail_free_cards += self.jail_free_cards
        self.bankrupt = True
    
    def sell_in_set(self, prop: 'Space', game: 'Game'):
        props_in_set: list['Space'] = list(filter(lambda x: x.set == prop.set, self.properties))
        for p in sorted(props_in_set, key=lambda x: x.houses):
            if game.can_sell_house(self, p):
                game.sell_house(self, p)
                break
    
    def pay(self, rent: int, other: 'Player', game: 'Game'):
        if self.debug and self.piece != "Bank":
            print(f"{self.piece} needs to pay {other.piece} ${rent}")
            print(f"{self.piece} has ${self.money}")
        
        if (self.money >= rent):
            self.money = int(self.money - rent)
            other.money = int(other.money + rent)
        else:
            if self.debug:
                print(f"{self.piece} does not have enough money to pay {other.piece}")
                print("Attempting to mortgage and sell houses to pay rent")
            
            all_mortgaged = False
            while (self.money < rent and not all_mortgaged):

                if not self.is_ai:
                    # TODO: Get user input
                    continue

                sorted_props = sorted(self.properties, key=lambda x: x.value)
                for i, prop in enumerate(sorted_props):
                    if not prop.mortgaged and ((prop.value // 2 + self.money) >= rent or all([p.mortgaged for p in sorted_props[i+1:]])):
                        if prop.houses == 0:

                            if self.debug:
                                print(f"Mortgaging {prop.id} to pay rent")

                            game.mortgage_property(self, prop)
                        elif game.can_sell_house(self, prop):

                            if self.debug:
                                print(f"Selling house on {prop.id} to pay rent")

                            game.sell_house(self, prop)
                        else:

                            if self.debug:
                                print(f"Selling house on {prop.set} set to pay rent")

                            self.sell_in_set(prop, game)
                        break
                all_mortgaged = all([prop.mortgaged for prop in self.properties])
            
            if not all_mortgaged:
                self.money = int(self.money - rent)
                other.money = int(other.money + rent)
            else:
                self.lose(other, game)
    
    # 0 represents the player choosing not to bid
    # -1 represents the player not having enough money to bid
    # any other number represents the player's bid
    def make_auction_bid(self, bid: int, space: 'Space', game: 'Game') -> int:
        if not self.is_ai:
            user_input = 0
            # TODO: Get user input
            return user_input
        
        if (bid + 1) > self.money:
            return -1
        else:
            set_matches = sum([1 for prop in self.properties if prop.set == space.set])

            if set_matches == 1:
                return min(bid + 5, self.money)
            elif set_matches == 2:
                return min(bid + 10, self.money)
            elif bid < space.value:
                return bid + 1
            
            return 0
    
    def doubles_or_pay_or_jfc(self, game: 'Game'):
        if not self.is_ai:
            user_input = 0
            # TODO: Get user input
            return user_input

        if self.turns_in_jail == 3 or game.turns < 25:
            if len(self.jail_free_cards) > 0:
                return 2
            else:
                return 1
        else:
            return 0
    
    def use_jail_free_card(self, game: 'Game'):
        card_to_use = self.jail_free_cards.pop(0)

        if (card_to_use.id == "9"):
            game.chance.append(card_to_use)
        else:
            game.community_chest.append(card_to_use)
    
    def build_house(self, game: 'Game'):

        if not self.is_ai:
            user_input = 0
            # TODO: Get user input
            return self.properties[user_input]

        if len(self.properties) == 0:
            return None
        
        sorted_props: list['Space'] = sorted(self.properties, key=lambda x: x.value, reverse=True)
        
        for prop in sorted_props:
            if prop.houses < 5 and game.can_build_house(self, prop):
                return prop
        
        return None

    def unmortgage_property(self, game: 'Game'):

        if not self.is_ai:
            user_input = 0
            # TODO: Get user input
            return self.properties[user_input]

        if len(self.properties) == 0:
            return None
        
        sorted_props: list['Space'] = sorted(self.properties, key=lambda x: x.value, reverse=True)
        for prop in sorted_props:
            if prop.mortgaged and self.money >= (((prop.value // 2) * 1.1) // 1):
                return prop
        
        return None
