from game import Game

def main():
    g = Game(debug=True)
    bankrupt_count = 0
    g.print_game_state()
    while bankrupt_count < 3 and not g.draw_game:
        progress_made = g.play_turn()
        if progress_made:
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
