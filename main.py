import argparse

from game import Game

def main():
    parser = argparse.ArgumentParser(description="Play a game of Monopoly", prog="python main.py")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information", default=False)
    parser.add_argument("-m", "--max-turns", type=int, help="Maximum number of turns to play", default=2500)
    parser.add_argument("-p", "--players", type=int, help="Number of players", default=4)
    args = parser.parse_args()
    
    g = Game(debug=args.debug, max_turns=args.max_turns, num_players=args.players)
    bankrupt_count = 0
    g.print_game_state()
    while bankrupt_count < args.players - 1 and not g.draw_game:
        progress_made = g.play_turn()
        if progress_made and args.debug:
            g.print_game_state()
        bankrupt_count = sum([1 for player in g.players if player.bankrupt])
    
    print("Game over!")
    if g.draw_game:
        print("It's a draw!")
    else:
        print(f"{[player.piece for player in g.players if not player.bankrupt][0]} wins!")
    return

if __name__ == '__main__':
    main()
