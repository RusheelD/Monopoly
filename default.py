from typing import TYPE_CHECKING
from card import Card
if TYPE_CHECKING:
    from game import Game, Player

class DefaultChance:
    # Generate the default chance deck
    @staticmethod
    def generate_chance_deck():
        return [
            Card("1", "Advance to Boardwalk", "Advance to DB4", DefaultChance.c1),
            Card("2", "Advance to GO", "Advance to GO", DefaultChance.c2),
            Card("3", "Advance to Illinois Avenue", "Advance to R4", DefaultChance.c3),
            Card("4", "Advance to St. Charles Place", "Advance to P1", DefaultChance.c4),
            Card("5", "Advance to nearest Railroad", "Advance to nearest RR", DefaultChance.c5),
            Card("6", "Advance to nearest Railroad", "Advance to nearest RR", DefaultChance.c6),
            Card("7", "Advance to nearest Utility", "Advance to nearest utility", DefaultChance.c7),
            Card("8", "Bank pays you dividend of $50", "Bank pays you $50", DefaultChance.c8),
            Card("9", "Get out of jail free", "Get out of jail free", DefaultChance.c9),
            Card("10", "Go back 3 spaces", "Go back 3 spaces", DefaultChance.c10),
            Card("11", "Go directly to jail, do not pass GO", "Go to jail", DefaultChance.c11),
            Card("12", "Make general repairs, $25 per house and $100 per hotel", "Make general repairs", DefaultChance.c12),
            Card("13", "Speeding fine, $15", "Speeding fine", DefaultChance.c13),
            Card("14", "Take a trip to Reading Railroad", "Take a trip to RR1", DefaultChance.c14),
            Card("15", "You have been elected chairman of the board, pay each player $50", "Elected chairman", DefaultChance.c15),
            Card("16", "Your building loan matures, collect $150", "Building loan matures", DefaultChance.c16)
        ]

    # Advance to DB2
    @staticmethod
    def c1(player: 'Player', game: 'Game'):
        player.space = len(game.spaces) - 1
        db2 = game.spaces[-1]
        if db2.owner is not None and db2.owner != player:
            rent = DefaultSpaceRents.db2(db2.owner, game)
            player.pay(rent, db2.owner, game)
        return True
    
    # Advance to GO
    @staticmethod
    def c2(player: 'Player', game: 'Game'):
        player.space = 0
        game.bank.pay(200, player, game)
        return True
    
    # Advance to R4
    @staticmethod
    def c3(player: 'Player', game: 'Game'):
        if player.space > 24:
            game.bank.pay(200, player, game)
        player.space = 24
        r4 = game.spaces[24]
        if r4.owner is not None and r4.owner != player:
            rent = DefaultSpaceRents.r3(r4.owner, game)
            player.pay(rent, r4.owner, game)
        return True
    
    # Advance to P1
    @staticmethod
    def c4(player: 'Player', game: 'Game'):
        if player.space > 11:
            game.bank.pay(200, player, game)
        player.space = 11
        p1 = game.spaces[11]
        if p1.owner is not None and p1.owner != player:
            rent = DefaultSpaceRents.p1(p1.owner, game)
            player.pay(rent, p1.owner, game)
        return True
    
    # Advance to nearest RR
    @staticmethod
    def c5(player: 'Player', game: 'Game'):
        railroads = [5, 15, 25, 35]

        if player.space > 35:
            game.bank.pay(200, player, game)
            player.space = 5
        else:
            player.space = min(railroads, key=lambda x: max(x - player.space, 0))
        
        new_space = game.spaces[player.space]
        
        if new_space.owner is not None and new_space.owner != player:
            rent = DefaultSpaceRents.rr(new_space.owner, game) * 2
            player.pay(rent, new_space.owner, game)
        return True
    
    # Advance to nearest RR again
    @staticmethod
    def c6(player: 'Player', game: 'Game'):
        return DefaultChance.c5(player, game)
    
    # Advance to nearest utility
    @staticmethod
    def c7(player: 'Player', game: 'Game'):
        utilities = [12, 28]

        if player.space > 28:
            game.bank.pay(200, player, game)
            player.space = 12
        else:
            player.space = min(utilities, key=lambda x: max(x - player.space, 0))
        
        new_space = game.spaces[player.space]
        
        if new_space.owner is not None and new_space.owner != player:
            rent = sum(game.dice) * 10
            player.pay(rent, new_space.owner, game)
        return True
    
    # Bank pays you $50
    @staticmethod
    def c8(player: 'Player', game: 'Game'):
        game.bank.pay(50, player, game)
        return True
    
    # Get out of jail free
    @staticmethod
    def c9(player: 'Player', game: 'Game'):
        return False

    # Go back 3 spaces
    @staticmethod
    def c10(player: 'Player', game: 'Game'):
        player.space = (player.space - 3) % len(game.spaces)
        return True
    
    # Go to jail
    @staticmethod
    def c11(player: 'Player', game: 'Game'):
        game.go_to_jail(player)
        return True

    # Make general repairs
    @staticmethod
    def c12(player: 'Player', game: 'Game'):
        rent = 0
        for prop in player.properties:
            if prop.houses == 5:
                rent += 100
            else:
                rent += prop.houses * 25
        player.pay(rent, game.bank, game)
        return True
    
    # Speeding fine
    @staticmethod
    def c13(player: 'Player', game: 'Game'):
        player.pay(15, game.bank, game)
        return True
    
    # Take a trip to RR1
    @staticmethod
    def c14(player: 'Player', game: 'Game'):
        if player.space > 5:
            game.bank.pay(200, player, game)
        player.space = 5
        rr1 = game.spaces[5]
        if rr1.owner is not None and rr1.owner != player:
            rent = DefaultSpaceRents.rr(rr1.owner, game)
            player.pay(rent, rr1.owner, game)
        return True
    
    # Elected chairman
    @staticmethod
    def c15(player: 'Player', game: 'Game'):
        for p in game.players:
            if p != player:
                player.pay(50, p, game)
        return True
    
    # Building loan matures
    @staticmethod
    def c16(player: 'Player', game: 'Game'):
        game.bank.pay(150, player, game)
        return True

class DefaultCommunityChest:
    # Generate the default community chest deck
    @staticmethod
    def generate_community_chest_deck():
        return [
            Card("1", "Advance to GO", "Advance to GO", DefaultCommunityChest.c1),
            Card("2", "Bank error in your favor, collect $200", "Bank error, collect $200", DefaultCommunityChest.c2),
            Card("3", "Doctor's fees, pay $50", "Doctor's fees, pay $50", DefaultCommunityChest.c3),
            Card("4", "From sale of stock you get $50", "Sale of stock, get $50", DefaultCommunityChest.c4),
            Card("5", "Get out of jail free", "Get out of jail free", DefaultCommunityChest.c5),
            Card("6", "Go to jail, go directly to jail, do not pass GO", "Go to jail", DefaultCommunityChest.c6),
            Card("7", "Holiday fund matures, collect $100", "Holiday fund matures, collect $100", DefaultCommunityChest.c7),
            Card("8", "Income tax refund, collect $20", "Income tax refund, collect $20", DefaultCommunityChest.c8),
            Card("9", "It's your birthday, collect $10 from each player", "It's your birthday", DefaultCommunityChest.c9),
            Card("10", "Life insurance matures, collect $100", "Life insurance matures", DefaultCommunityChest.c10),
            Card("11", "Pay hospital fees of $100", "Pay hospital fees", DefaultCommunityChest.c11),
            Card("12", "Pay school fees of $50", "Pay school fees", DefaultCommunityChest.c12),
            Card("13", "Receive $25 consultancy fee", "Receive $25", DefaultCommunityChest.c13),
            Card("14", "You are assessed for street repairs, $40 per house, $115 per hotel", "Street repairs", DefaultCommunityChest.c14),
            Card("15", "You have won second prize in a beauty contest, collect $10", "Beauty contest prize", DefaultCommunityChest.c15),
            Card("16", "You inherit $100", "Inherit $100", DefaultCommunityChest.c16)
        ]

    # Advance to GO
    @staticmethod
    def c1(player: 'Player', game: 'Game'):
        player.space = 0
        game.bank.pay(200, player, game)
        return True
    
    # Bank error in your favor
    @staticmethod
    def c2(player: 'Player', game: 'Game'):
        game.bank.pay(200, player, game)
        return True
    
    # Doctor's fee
    @staticmethod
    def c3(player: 'Player', game: 'Game'):
        player.pay(50, game.bank, game)
        return True

    # From sale of stock you get $50
    @staticmethod
    def c4(player: 'Player', game: 'Game'):
        game.bank.pay(50, player, game)
        return True
    
    # Get out of jail free
    @staticmethod
    def c5(player: 'Player', game: 'Game'):
        return False
    
    # Go to jail
    @staticmethod
    def c6(player: 'Player', game: 'Game'):
        game.go_to_jail(player)
        return True
    
    # Holiday fund matures
    @staticmethod
    def c7(player: 'Player', game: 'Game'):
        game.bank.pay(100, player, game)
        return True

    # Income tax refund
    @staticmethod
    def c8(player: 'Player', game: 'Game'):
        game.bank.pay(20, player, game)
        return True
    
    # It's your birthday
    @staticmethod
    def c9(player: 'Player', game: 'Game'):
        for p in game.players:
            if p != player:
                p.pay(10, player, game)
        return True
    
    # Life insurance matures
    @staticmethod
    def c10(player: 'Player', game: 'Game'):
        game.bank.pay(100, player, game)
        return True
    
    # Pay hospital fees
    @staticmethod
    def c11(player: 'Player', game: 'Game'):
        player.pay(100, game.bank, game)
        return True
    
    # Pay school fees
    @staticmethod
    def c12(player: 'Player', game: 'Game'):
        player.pay(50, game.bank, game)
        return True
    
    # Receive $25 consultancy fee
    @staticmethod
    def c13(player: 'Player', game: 'Game'):
        game.bank.pay(25, player, game)
        return True
    
    # You are assessed for street repairs
    @staticmethod
    def c14(player: 'Player', game: 'Game'):
        rent = 0
        for prop in player.properties:
            if prop.houses == 5:
                rent += 115
            else:
                rent += prop.houses * 40
        player.pay(rent, game.bank, game)
        return True
    
    # You have won second prize in a beauty contest
    @staticmethod
    def c15(player: 'Player', game: 'Game'):
        game.bank.pay(10, player, game)
        return True
    
    # You inherit $100
    @staticmethod
    def c16(player: 'Player', game: 'Game'):
        game.bank.pay(100, player, game)
        return True

class DefaultSpaceRents:
    @staticmethod
    def br1(player: 'Player', game: 'Game'): # type: ignore
        space = game.spaces[1]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 2:
            return 2
        else:
            match space.houses:
                case 0:
                    return 4
                case 1:
                    return 10
                case 2:
                    return 30
                case 3:
                    return 90
                case 4:
                    return 160
                case 5:
                    return 250
    
    @staticmethod
    def br2(player: 'Player', game: 'Game'):
        space = game.spaces[3]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 2:
            return 4
        else:
            match space.houses:
                case 0:
                    return 8
                case 1:
                    return 20
                case 2:
                    return 60
                case 3:
                    return 180
                case 4:
                    return 320
                case 5:
                    return 450
    
    @staticmethod
    def rr(player: 'Player', game: 'Game'):
        num_in_set = sum([1 for prop in player.properties if prop.set == "RR"])
        match num_in_set:
            case 1:
                return 25
            case 2:
                return 50
            case 3:
                return 100
            case 4:
                return 200
    
    @staticmethod
    def lb1(player: 'Player', game: 'Game'):
        space = game.spaces[6]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 6
        else:
            match space.houses:
                case 0:
                    return 12
                case 1:
                    return 30
                case 2:
                    return 90
                case 3:
                    return 270
                case 4:
                    return 400
                case 5:
                    return 550
    
    @staticmethod
    def lb2(player: 'Player', game: 'Game'):
        space = game.spaces[8]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 6
        else:
            match space.houses:
                case 0:
                    return 12
                case 1:
                    return 30
                case 2:
                    return 90
                case 3:
                    return 270
                case 4:
                    return 400
                case 5:
                    return 550
    
    @staticmethod
    def lb3(player: 'Player', game: 'Game'):
        space = game.spaces[9]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 8
        else:
            match space.houses:
                case 0:
                    return 16
                case 1:
                    return 40
                case 2:
                    return 100
                case 3:
                    return 300
                case 4:
                    return 450
                case 5:
                    return 600
    
    @staticmethod
    def p1(player: 'Player', game: 'Game'):
        space = game.spaces[11]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 10
        else:
            match space.houses:
                case 0:
                    return 20
                case 1:
                    return 50
                case 2:
                    return 150
                case 3:
                    return 450
                case 4:
                    return 625
                case 5:
                    return 750
    
    @staticmethod
    def utility(player: 'Player', game: 'Game'):
        num_in_set = sum([1 for prop in player.properties if prop.set == "U"])
        match num_in_set:
            case 1:
                return 4 * sum(game.dice)
            case 2:
                return 10 * sum(game.dice)
    
    @staticmethod
    def p2(player: 'Player', game: 'Game'):
        space = game.spaces[13]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 10
        else:
            match space.houses:
                case 0:
                    return 20
                case 1:
                    return 50
                case 2:
                    return 150
                case 3:
                    return 450
                case 4:
                    return 625
                case 5:
                    return 750
    
    @staticmethod
    def p3(player: 'Player', game: 'Game'):
        space = game.spaces[14]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 12
        else:
            match space.houses:
                case 0:
                    return 24
                case 1:
                    return 60
                case 2:
                    return 180
                case 3:
                    return 500
                case 4:
                    return 700
                case 5:
                    return 900
    
    @staticmethod
    def o1(player: 'Player', game: 'Game'):
        space = game.spaces[16]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 14
        else:
            match space.houses:
                case 0:
                    return 28
                case 1:
                    return 70
                case 2:
                    return 200
                case 3:
                    return 550
                case 4:
                    return 750
                case 5:
                    return 950
    
    @staticmethod
    def o2(player: 'Player', game: 'Game'):
        space = game.spaces[18]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 14
        else:
            match space.houses:
                case 0:
                    return 28
                case 1:
                    return 70
                case 2:
                    return 200
                case 3:
                    return 550
                case 4:
                    return 750
                case 5:
                    return 950
    
    @staticmethod
    def o3(player: 'Player', game: 'Game'):
        space = game.spaces[19]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 16
        else:
            match space.houses:
                case 0:
                    return 32
                case 1:
                    return 80
                case 2:
                    return 220
                case 3:
                    return 600
                case 4:
                    return 800
                case 5:
                    return 1000
    
    @staticmethod
    def r1(player: 'Player', game: 'Game'):
        space = game.spaces[21]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 18
        else:
            match space.houses:
                case 0:
                    return 36
                case 1:
                    return 90
                case 2:
                    return 250
                case 3:
                    return 700
                case 4:
                    return 875
                case 5:
                    return 1050
    
    @staticmethod
    def r2(player: 'Player', game: 'Game'):
        space = game.spaces[23]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 18
        else:
            match space.houses:
                case 0:
                    return 36
                case 1:
                    return 90
                case 2:
                    return 250
                case 3:
                    return 700
                case 4:
                    return 875
                case 5:
                    return 1050
    
    @staticmethod
    def r3(player: 'Player', game: 'Game'):
        space = game.spaces[24]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 20
        else:
            match space.houses:
                case 0:
                    return 40
                case 1:
                    return 100
                case 2:
                    return 300
                case 3:
                    return 750
                case 4:
                    return 925
                case 5:
                    return 1100
    
    @staticmethod
    def y1(player: 'Player', game: 'Game'):
        space = game.spaces[26]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 22
        else:
            match space.houses:
                case 0:
                    return 44
                case 1:
                    return 110
                case 2:
                    return 330
                case 3:
                    return 800
                case 4:
                    return 975
                case 5:
                    return 1150
    
    @staticmethod
    def y2(player: 'Player', game: 'Game'):
        space = game.spaces[27]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 22
        else:
            match space.houses:
                case 0:
                    return 44
                case 1:
                    return 110
                case 2:
                    return 330
                case 3:
                    return 800
                case 4:
                    return 975
                case 5:
                    return 1150
    
    @staticmethod
    def y3(player: 'Player', game: 'Game'):
        space = game.spaces[29]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 24
        else:
            match space.houses:
                case 0:
                    return 48
                case 1:
                    return 120
                case 2:
                    return 360
                case 3:
                    return 850
                case 4:
                    return 1025
                case 5:
                    return 1200
    
    @staticmethod
    def g1(player: 'Player', game: 'Game'):
        space = game.spaces[31]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 26
        else:
            match space.houses:
                case 0:
                    return 52
                case 1:
                    return 130
                case 2:
                    return 390
                case 3:
                    return 900
                case 4:
                    return 1100
                case 5:
                    return 1275
    
    @staticmethod
    def g2(player: 'Player', game: 'Game'):
        space = game.spaces[32]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 26
        else:
            match space.houses:
                case 0:
                    return 52
                case 1:
                    return 130
                case 2:
                    return 390
                case 3:
                    return 900
                case 4:
                    return 1100
                case 5:
                    return 1275
    
    @staticmethod
    def g3(player: 'Player', game: 'Game'):
        space = game.spaces[34]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 3:
            return 28
        else:
            match space.houses:
                case 0:
                    return 56
                case 1:
                    return 150
                case 2:
                    return 450
                case 3:
                    return 1000
                case 4:
                    return 1200
                case 5:
                    return 1400
    
    @staticmethod
    def db1(player: 'Player', game: 'Game'):
        space = game.spaces[37]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 2:
            return 35
        else:
            match space.houses:
                case 0:
                    return 70
                case 1:
                    return 175
                case 2:
                    return 500
                case 3:
                    return 1100
                case 4:
                    return 1300
                case 5:
                    return 1500
    
    @staticmethod
    def db2(player: 'Player', game: 'Game'):
        space = game.spaces[39]
        num_in_set = sum([1 for prop in player.properties if prop.set == space.set])
        if num_in_set != 2:
            return 50
        else:
            match space.houses:
                case 0:
                    return 100
                case 1:
                    return 200
                case 2:
                    return 600
                case 3:
                    return 1400
                case 4:
                    return 1700
                case 5:
                    return 2000
    