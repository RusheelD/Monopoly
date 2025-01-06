from typing import Callable
import random
from default import DefaultSpaceRents

class Card:
    def __init__(self, id: str, text: str, function: str, on_draw: Callable[['Player', 'Game'], bool]):
        self.id = id
        self.text = text
        self.function = function
        self.on_draw = on_draw

class Player:
    def __init__(self, id: int, piece: str):
        self.id = id
        self.piece = piece
        self.space = 0
        self.money = 1500
        self.properties: list['Space'] = []
        self.jail_free_cards: list[Card] = []
        self.in_jail = False
        self.turns_in_jail = 0
        self.doubles_rolled = 0
    
    def buy_property(self, space: 'Space', game: 'Game') -> bool:
        if self.money >= space.value:
            return True
        else:
            return False
    
    def pay_rent(self, rent: int, owner: 'Player'):
        if (self.money >= rent):
            self.money -= rent
            owner.money += rent
        else:
            # Mortage properties to pay rent
            pass
    
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

class Space:
    def __init__(self, id: str, value: int, side: int, on_land: Callable[[Player, 'Game'], None] = None, rent: Callable[[Player, 'Game'], int] = None):
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
        
        self.owner: Player | None = None
        self.mortgaged = False
        self.set = self.id[:-1]

class Game:

    def __init__(self, num_players: int = 4):

        self.all_pieces = ["car", "thimble", "dog", "boot", "hat", "ship", "iron", "wheelbarrow", "t-rex", "cat"]
        self.chance: list[Card] = []
        self.community_chest: list[Card] = []
        self.jail: list[Player] = []

        random.shuffle(self.chance)
        random.shuffle(self.community_chest)

        random.shuffle(self.all_pieces)
        self.players = [Player(i, self.all_pieces[i]) for i in range(num_players)]

        self.dice = [0, 0]

        self.current_player = 0

        def pass_go(player: Player, game: 'Game'):
            player.money += 200
        
        def buy_or_auction(player: Player, game: 'Game'):
            space = game.spaces[player.space]

            player_choice = player.buy_property(space, game)

            if player_choice and player.money >= space.value:
                player.money -= space.value
                space.owner = player
                player.properties.append(space)
            else:
                max_bid = 10
                i = player.id
                auction_over = False
                auction_ending = False

                bids = [0] * len(self.players)
                bids[i] = max_bid

                while not auction_over:
                    i = (i + 1) % len(self.players)

                    bids[i] = self.players[i].make_auction_bid(max_bid, space, game)
                    valid_bids = sum([1 for bid in bids if bid > 0])

                    if (valid_bids == 1 and not auction_ending):
                        auction_ending = True
                    elif (valid_bids == 0 and auction_ending):
                        auction_over = True
                    else:
                        auction_ending = False
                    
                    max_bid = max(bids)

                max_bid = max(bids)
                winning_index = bids.index(max_bid)
                winning_player = self.players[winning_index]

                if winning_player.money >= max_bid:
                    winning_player.money -= max_bid
                    space.owner = winning_player
                    winning_player.properties.append(space)
                
        
        def community_chest(player: Player, game: 'Game'):
            card = game.community_chest.pop(0)
            replace = card.on_draw(player, game)
            if replace:
                game.community_chest.append(card)
        
        def chance(player: Player, game: 'Game'):
            card = game.chance.pop(0)
            replace = card.on_draw(player, game)
            if replace:
                game.chance.append(card)
        
        def income_tax(player: Player, game: 'Game'):
            player.money -= 200
        
        def go_to_jail(player: Player, game: 'Game'):
            player.space = 10
            player.in_jail = True
            game.jail.append(player)
        
        def luxury_tax(player: Player, game: 'Game'):
            player.money -= 100

        self.spaces: list[Space] = [
            Space("Go", 0, -1, pass_go),
            Space("BR1", 60, 0, buy_or_auction, DefaultSpaceRents.br1),
            Space("CommunityChest", 0, 0, community_chest),
            Space("BR2", 60, 0, buy_or_auction, DefaultSpaceRents.br2),
            Space("IncomeTax", 0, 0, income_tax),
            Space("RR1", 200, 0, buy_or_auction, DefaultSpaceRents.rr),
            Space("LB1", 100, 0, buy_or_auction, DefaultSpaceRents.lb1),
            Space("Chance", 0, 0, chance),
            Space("LB2", 100, 0, buy_or_auction, DefaultSpaceRents.lb2),
            Space("LB3", 120, 0, buy_or_auction, DefaultSpaceRents.lb3),
            Space("VisitJail", 0, -1),
            Space("P1", 140, 1, buy_or_auction, DefaultSpaceRents.p1),
            Space("Utility1", 150, 1, buy_or_auction, DefaultSpaceRents.utility),
            Space("P2", 140, 1, buy_or_auction, DefaultSpaceRents.p2),
            Space("P3", 160, 1, buy_or_auction, DefaultSpaceRents.p3),
            Space("RR2", 200, 1, buy_or_auction, DefaultSpaceRents.rr),
            Space("O1", 180, 1, buy_or_auction, DefaultSpaceRents.o1),
            Space("CommunityChest", 0, 1, community_chest),
            Space("O2", 180, 1, buy_or_auction, DefaultSpaceRents.o2),
            Space("O3", 200, 1, buy_or_auction, DefaultSpaceRents.o3),
            Space("FreeParking", 0, -1),
            Space("R1", 220, 2, buy_or_auction, DefaultSpaceRents.r1),
            Space("Chance", 0, 2, chance),
            Space("R2", 220, 2, buy_or_auction, DefaultSpaceRents.r2),
            Space("R3", 240, 2, buy_or_auction, DefaultSpaceRents.r3),
            Space("RR3", 200, 2, buy_or_auction, DefaultSpaceRents.rr),
            Space("Y1", 260, 2, buy_or_auction, DefaultSpaceRents.y1),
            Space("Y2", 260, 2, buy_or_auction, DefaultSpaceRents.y2),
            Space("Utility2", 150, 2, buy_or_auction, DefaultSpaceRents.utility),
            Space("Y3", 280, 2, buy_or_auction, DefaultSpaceRents.y3),
            Space("GoToJail", 0, -1, go_to_jail),
            Space("G1", 300, 3, buy_or_auction, DefaultSpaceRents.g1),
            Space("G2", 300, 3, buy_or_auction, DefaultSpaceRents.g2),
            Space("CommunityChest", 0, 3, community_chest),
            Space("G3", 320, 3, buy_or_auction, DefaultSpaceRents.g3),
            Space("RR4", 200, 3, buy_or_auction, DefaultSpaceRents.rr),
            Space("Chance", 0, 3, chance),
            Space("DB1", 350, 3, buy_or_auction, DefaultSpaceRents.db1),
            Space("LuxuryTax", 0, 3, luxury_tax),
            Space("DB2", 400, 3, buy_or_auction, DefaultSpaceRents.db2)
        ]
    
    def roll_dice(self):
        self.dice = [random.randint(1, 6), random.randint(1, 6)]
        return self.dice

    def mortgage_property(self, player: Player, space: Space):
        if space.owner == player and not space.mortgaged:
            space.mortgaged = True
            player.money += space.value // 2
    
    def unmortgage_property(self, player: Player, space: Space):
        if space.owner == player and space.mortgaged:
            space.mortgaged = False
            player.money -= (space.value // 2 * 1.1) // 1
    
    def build_house(self, player: Player, space: Space):
        set_can_build = space.set in ["BR", "LB", "P", "O", "R", "Y", "G", "DB"]

        has_enough_money = player.money >= space.side * 50

        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        has_all_in_set = (num_in_set == 3 or (num_in_set == 2 and (space.set == "DB" or space.set == "BR")))

        new_houses = space.houses + 1

        properties_in_set = [prop for prop in player.properties if prop.set == space.set]

        house_count_valid = all([(new_houses - prop.houses) < 2 for prop in properties_in_set])

        if set_can_build and has_all_in_set and space.houses < 5 and house_count_valid and has_enough_money:
            space.houses += 1
            player.money -= (space.side + 1) * 50
    
    def sell_house(self, player: Player, space: Space):
        set_can_sell = space.set in ["BR", "LB", "P", "O", "R", "Y", "G", "DB"]

        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        has_all_in_set = (num_in_set == 3 or (num_in_set == 2 and (space.set == "DB" or space.set == "BR")))

        new_houses = space.houses - 1

        properties_in_set = [prop for prop in player.properties if prop.set == space.set]

        house_count_valid = all([(prop.houses - new_houses) < 2 for prop in properties_in_set])

        if set_can_sell and has_all_in_set and space.houses > 0 and house_count_valid:
            space.houses -= 1
            player.money += (space.side + 1) * 25
    
    def trade(self, player1: Player, player2: Player, p1_money_give: int, p2_money_give: int, p1_properties_give: list[Space], p2_properties_give: list[Space]):
        p1_money = player1.money
        p2_money = player2.money

        p1_properties = player1.properties
        p2_properties = player2.properties

        p1_money += p1_money_give
        p2_money += p2_money_give

        for prop in p1_properties_give:
            if prop in p1_properties:
                p1_properties.remove(prop)
                p2_properties.append(prop)
        
        for prop in p2_properties_give:
            if prop in p2_properties:
                p2_properties.remove(prop)
                p1_properties.append(prop)
        
        player1.money = p1_money
        player2.money = p2_money

        player1.properties = p1_properties
        player2.properties = p2_properties
    
    def move_player(self, player: Player, spaces: int):
        player.space = (player.space + spaces) % len(self.spaces)
        self.spaces[player.space].on_land(player, self)
