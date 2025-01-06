from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game, Player

class DefaultChance:

    # Advance to Boardwalk
    def c1(player: Player, game: Game):
        player.space = len(game.spaces) - 1
    
    # Advance to GO
    def c2(player: Player, game: Game):
        player.space = 0
        player.money += 200
    
    # Advance to R4
    def c3(player: Player, game: Game):
        if player.space > 24:
            player.money += 200
        player.space = 24
    
    # Advance to P1
    def c4(player: Player, game: Game):
        if player.space > 11:
            player.money += 200
        player.space = 11
    
    # Advance to nearest RR
    def c5(player: Player, game: Game):
        railroads = [5, 15, 25, 35]

        if player.space > 35:
            player.money += 200
            player.space = 5
        else:
            player.space = min(railroads, key=lambda x: max(x - player.space, 0))
        
        new_space = game.spaces[player.space]
        
        if new_space.owner is not None and new_space.owner != player:
            rent = DefaultSpaceRents.rr(new_space.owner, game) * 2
            player.pay_rent(rent, new_space.owner)

class DefaultCommunityChest:
    pass

class DefaultSpaceRents:
    @staticmethod
    def br1(player: Player, game: Game): # type: ignore
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
    def br2(player: Player, game: Game):
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
    def rr(player: Player, game: Game):
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
    def lb1(player: Player, game: Game):
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
    def lb2(player: Player, game: Game):
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
    def lb3(player: Player, game: Game):
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
    def p1(player: Player, game: Game):
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
    def utility(player: Player, game: Game):
        num_in_set = sum([1 for prop in player.properties if prop.set == "Utility"])
        match num_in_set:
            case 1:
                return 4 * sum(game.dice)
            case 2:
                return 10 * sum(game.dice)
    
    @staticmethod
    def p2(player: Player, game: Game):
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
    def p3(player: Player, game: Game):
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
    def o1(player: Player, game: Game):
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
    def o2(player: Player, game: Game):
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
    def o3(player: Player, game: Game):
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
    def r1(player: Player, game: Game):
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
    def r2(player: Player, game: Game):
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
    def r3(player: Player, game: Game):
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
    def y1(player: Player, game: Game):
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
    def y2(player: Player, game: Game):
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
    def y3(player: Player, game: Game):
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
    def g1(player: Player, game: Game):
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
    def g2(player: Player, game: Game):
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
    def g3(player: Player, game: Game):
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
    def db1(player: Player, game: Game):
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
    def db2(player: Player, game: Game):
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
    