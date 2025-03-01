import random
from default import DefaultSpaceRents, DefaultChance, DefaultCommunityChest
from card import Card
from player import Player
from space import Space

class Game:

    def __init__(self, num_players: int = 4, max_turns = 2500, debug = False):
        self.debug = debug
        self.max_turns_before_draw = max_turns
        self.all_pieces = ["Car", "Thimble", "Dog", "Boot", "Hat", "Ship", "Iron", "Wheelbarrow", "T-Rex", "Cat"]
        self.chance: list[Card] = DefaultChance.generate_chance_deck()
        self.community_chest: list[Card] = DefaultCommunityChest.generate_community_chest_deck()
        self.jail: list[Player] = []
        self.bank = Player(-1, "Bank")
        self.bank.money = 10000000
        self.draw_game = False

        random.shuffle(self.chance)
        random.shuffle(self.community_chest)

        random.shuffle(self.all_pieces)
        self.players = [Player(i, self.all_pieces[i], debug=self.debug) for i in range(num_players)]

        self.dice = [0, 0]

        self.current_player = 0
        self.turns = 0

        
        self.buyable_properties = [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35, 37, 39]

        def pass_go(player: Player, game: 'Game'):
            self.bank.pay(200, player, game)
        
        def buy_or_auction(player: Player, game: 'Game'):
            space = game.spaces[player.space]

            player_choice = player.buy_property(space, game)

            if player_choice and player.money >= space.value:
                player.pay(space.value, game.bank, game)
                space.owner = player
                player.properties.append(space)
            else:
                max_bid = 10
                i = player.id
                auction_over = False
                auction_ending = False

                if self.debug:
                    print(f"Auction for {space.id} starting")

                bids = [0] * len(self.players)
                bids[i] = max_bid

                while not auction_over:
                    if self.debug:
                        print(f"Bids: {bids}")

                    i = (i + 1) % len(self.players)

                    if (not auction_ending) or (auction_ending and bids[i] == 0):
                        bids[i] = self.players[i].make_auction_bid(max_bid, space, game)
                    valid_bids = sum([1 for bid in bids if bid > 0])

                    if (valid_bids == 1 and not auction_ending):
                        auction_ending = True
                    elif (valid_bids == 1 and auction_ending):
                        auction_over = True
                    else:
                        auction_ending = False
                    
                    max_bid = max(bids)

                max_bid = max(bids)
                winning_index = bids.index(max_bid)
                winning_player = self.players[winning_index]

                if winning_player.money >= max_bid:
                    winning_player.pay(max_bid, game.bank, game)
                    space.owner = winning_player
                    winning_player.properties.append(space)
                
        
        def community_chest(player: Player, game: 'Game'):
            card = game.community_chest.pop(0)

            if self.debug:
                print(f"{player.piece} drew {card.text}")

            replace = card.on_draw(player, game)
            if replace:
                game.community_chest.append(card)
            else:
                player.jail_free_cards.append(card)
        
        def chance(player: Player, game: 'Game'):
            card = game.chance.pop(0)

            if self.debug:
                print(f"{player.piece} drew {card.text}")

            replace = card.on_draw(player, game)
            if replace:
                game.chance.append(card)
            else:
                player.jail_free_cards.append(card)
        
        def income_tax(player: Player, game: 'Game'):
            player.pay(200, game.bank, game)
        
        def luxury_tax(player: Player, game: 'Game'):
            player.pay(100, game.bank, game)

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
            Space("U1", 150, 1, buy_or_auction, DefaultSpaceRents.utility),
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
            Space("U2", 150, 2, buy_or_auction, DefaultSpaceRents.utility),
            Space("Y3", 280, 2, buy_or_auction, DefaultSpaceRents.y3),
            Space("GoToJail", 0, -1, lambda player, game: self.go_to_jail(player)),
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

    def go_to_jail(self, player: Player):
            
        if self.debug:
            print(f"{player.piece} is going to jail")

        player.space = 10
        self.jail.append(player.id)
        player.in_jail = True
        player.turns_in_jail = 0
        player.doubles_rolled = 0
    
    def out_of_jail(self, player: Player):

        if self.debug:
            print(f"{player.piece} is leaving jail")

        player.in_jail = False
        player.turns_in_jail = 0
        player.doubles_rolled = 0
        self.jail.remove(player.id)

    def roll_dice(self):
        self.dice = [random.randint(1, 6), random.randint(1, 6)]
        return self.dice

    def mortgage_property(self, player: Player, space: Space):
        if space.owner == player and not space.mortgaged and space.houses == 0:
            space.mortgaged = True
            self.bank.pay(space.value // 2, player, self)

            if self.debug:
                print(f"{player.piece} mortgaged {space.id}, new total: ${player.money}")
    
    def unmortgage_property(self, player: Player, space: Space):
        if space.owner == player and space.mortgaged:
            space.mortgaged = False
            player.pay((space.value // 2 * 1.1) // 1, self.bank, self)
    
    def has_all_in_set(self, player: Player, space: Space):
        if space.set in ["RR", "U"]:
            return False
        
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        return (num_in_set == 3 or (num_in_set == 2 and (space.set == "DB" or space.set == "BR")))

    def can_build_house(self, player: Player, space: Space):

        if space.mortgaged:
            return False

        set_can_build = space.set in ["BR", "LB", "P", "O", "R", "Y", "G", "DB"]

        has_enough_money = player.money >= space.side * 50

        has_all_in_set = self.has_all_in_set(player, space)

        new_houses = space.houses + 1

        properties_in_set = [prop for prop in player.properties if prop.set == space.set]

        if any([prop.mortgaged for prop in properties_in_set]):
            return False

        house_count_valid = all([abs(new_houses - prop.houses) < 2 for prop in properties_in_set])

        return set_can_build and has_all_in_set and space.houses < 5 and house_count_valid and has_enough_money
    
    def can_sell_house(self, player: Player, space: Space):
        set_can_sell = space.set in ["BR", "LB", "P", "O", "R", "Y", "G", "DB"]

        has_all_in_set = self.has_all_in_set(player, space)

        new_houses = space.houses - 1

        properties_in_set = filter(lambda x: x.set == space.set, player.properties)

        house_count_valid = all([abs(prop.houses - new_houses) < 2 for prop in properties_in_set])

        return set_can_sell and has_all_in_set and space.houses > 0 and house_count_valid
    
    def build_house(self, player: Player, space: Space):
        if self.can_build_house(player, space):
            space.houses += 1
            player.pay((space.side + 1) * 50, self.bank, self)
    
    def sell_house(self, player: Player, space: Space):
        if self.can_sell_house(player, space):
            space.houses -= 1
            self.bank.pay((space.side + 1) * 25, player, self)
    
    def trade(self,
              player1: Player, player2: Player,
              p1_money_give: int, p2_money_give: int,
              p1_properties_give: list[Space], p2_properties_give: list[Space],
              p1_jail_free_give: list[Card], p2_jail_free_give: list[Card]
            ):
        
        p1_jail_free = player1.jail_free_cards
        p2_jail_free = player2.jail_free_cards

        p1_properties = player1.properties
        p2_properties = player2.properties

        player1.pay(p1_money_give, player2, self)
        player2.pay(p2_money_give, player1, self)

        for prop in p1_properties_give:
            if prop in p1_properties:
                p1_properties.remove(prop)
                p2_properties.append(prop)
        
        for prop in p2_properties_give:
            if prop in p2_properties:
                p2_properties.remove(prop)
                p1_properties.append(prop)

        for card in p1_jail_free_give:
            if card in p1_jail_free:
                p1_jail_free.remove(card)
                p2_jail_free.append(card)
        
        for card in p2_jail_free_give:
            if card in p2_jail_free:
                p2_jail_free.remove(card)
                p1_jail_free.append(card)

        player1.properties = p1_properties
        player2.properties = p2_properties

        player1.jail_free_cards = p1_jail_free
        player2.jail_free_cards = p2_jail_free
    
    def move_player(self, player: Player, spaces: int):
        if player.space + spaces >= len(self.spaces):
            self.bank.pay(200, player, self)
        
        player.space = (player.space + spaces) % len(self.spaces)
        space_landed = self.spaces[player.space]

        if self.debug:
            print(f"{player.piece} landed on {space_landed.id}")
            if space_landed.owner is not None:
                print(f"Owner: {space_landed.owner.piece}")

        if space_landed.owner is not None and space_landed.owner.piece != player.piece and not space_landed.mortgaged:
            player.pay(space_landed.rent(space_landed.owner, self), space_landed.owner, self)
        elif space_landed.owner is None:
            space_landed.on_land(player, self)
    
    def next_player(self):
        self.players[self.current_player].doubles_rolled = 0
        self.current_player = (self.current_player + 1) % len(self.players)

    def play_turn(self):
        player = self.players[self.current_player]
        doubles = False

        if player.bankrupt:
            self.next_player()
            return False
        
        def make_dice_roll():
            self.roll_dice()
            if self.debug:
                print(f"{player.piece} rolled the dice: {self.dice}")
            if self.dice[0] == self.dice[1]:
                player.doubles_rolled += 1
                return True
            return False


        if player.in_jail:
            match player.doubles_or_pay_or_jfc(self):
                case 0:
                    doubles = make_dice_roll()
                    if self.dice[0] == self.dice[1]:
                        self.out_of_jail(player)
                    else:
                        player.turns_in_jail += 1
                        self.next_player()
                        self.turns += 1

                        if self.debug:
                            print(f"{player.piece} is still in jail")

                        return True
                case 1:
                    player.pay(50, self.bank, self)

                    if player.bankrupt:
                        self.next_player()
                        self.turns += 1
                        return True

                    doubles = make_dice_roll()
                    self.out_of_jail(player)
                case 2:
                    player.use_jail_free_card(self)
                    doubles = make_dice_roll()
                    self.out_of_jail(player)
        else:
            doubles = make_dice_roll()

        if player.doubles_rolled == 3:
            self.go_to_jail(player)
            self.next_player()
            self.turns += 1
            return True

        self.move_player(player, sum(self.dice))

        house_build_choice = player.build_house(self)
        if house_build_choice != None:
            self.build_house(player, house_build_choice)

        unmortgage_choice = player.unmortgage_property(self)
        if unmortgage_choice != None:
            self.unmortgage_property(player, unmortgage_choice)

        if not doubles:
            self.next_player()
        
        self.turns += 1

        if self.turns >= self.max_turns_before_draw:
            self.draw_game = True
        
        props_in_bank = [self.spaces[i] for i in self.buyable_properties if self.spaces[i].owner is None]
        if len(props_in_bank) == 0:
            prop_sets = 0
            for player in self.players:
                seen = set()
                for prop in player.properties:
                    if prop.set not in seen and self.has_all_in_set(player, prop):
                        prop_sets += 1
                    elif prop.set == "RR" and len([p for p in player.properties if p.set == "RR"]) == 4:
                        prop_sets += 1
                    seen.add(prop.set)

                    
            if prop_sets == 0:
                self.draw_game = True
                if self.debug:
                    print("\n\nNo properties left in bank and no full sets owned by players")
        
        return True
    
    def print_game_state(self):

        props_in_bank = [self.spaces[i] for i in self.buyable_properties if self.spaces[i].owner is None]
        print("\n")

        print(f"Turn: {self.turns}")
        print(f"Bank: ")
        for p in props_in_bank:
            print(f"\t{p.id} - ${p.value}")
        if len(props_in_bank) == 0:
            print("\tNo properties in bank")
        print()

        for player in self.players:
            if player.bankrupt:
                print(f"{player.piece} is bankrupt\n")
                continue

            if player.space == 10 and player.in_jail:
                print(f"{player.piece} is in jail with ${player.money}")
            else:
                print(f"{player.piece} is on {self.spaces[player.space].id} with ${player.money}")
            print(f"Jail Free Cards: {len(player.jail_free_cards)}")
            print("Properties: ")
            for prop in sorted(player.properties, key=lambda x: x.set):
                print(f"\t{prop.id}{(3-len(prop.id))*" "} - ${prop.value}",end='')
                if prop.mortgaged:
                    print("\t(Mortgaged)")
                elif prop.houses > 0:
                    print(f"\t- {prop.houses} houses")
                else:
                    print()
            print()
        print()
