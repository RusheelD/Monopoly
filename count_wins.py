
from io import SEEK_SET
import sys

import os

def get_files_in_folder(folder_path):
    files = []
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            files.append(full_path)  # Use entry for relative path
    return files

def count_wins():
    log_folder = sys.argv[1]
    files = get_files_in_folder(log_folder)
    game_files = list(filter(lambda x: not("overview" in x), files))

    winners = {}

    total = 0
    wins = 0
    sweeps = 0

    for file in game_files:
        with open(file, 'r') as f:
            total += 1
            lines = f.readlines()[-3:]
            for line in lines:
                if "wins!" in line:
                    winner = line.split(" ")[0]
                    f.seek(0, SEEK_SET)
                    l2 = f.readlines()
                    sweep = True

                    for l in l2:
                        if ("has gone bankrupt to" in l) and (not winner in l):
                            sweep = False
                            break

                    if sweep:
                        sweeps += 1

                    winners.update({file: sweep})
                    wins += 1
    
    print(f"Total games: {total}")
    print(f"Total wins: {wins}")
    print(f"Total sweeps: {sweeps}")
    print(f"Win rate: {wins / total * 100}%")
    print(f"Sweep rate: {sweeps / total * 100}%")
    print(f"Sweep proportion: {sweeps / wins * 100}%")

    with open(log_folder + "/_overview.txt", 'w') as f:
        game_num_start = len(log_folder) + 6
        for file in sorted(game_files, key=lambda x: int(x[game_num_start:-4])):
            f.write(f"{file[game_num_start:-4]}\t{"win " if file in winners else "draw"}\t{"(sweep)" if file in winners and winners[file] else "(no sweep)"}\n")

    # print("Winning logs:")
    # for winner in winners.keys():
    #     print(winner,end='')
    #     if winners[winner]:
    #         print(" (it was a sweep)")
    #     else:
    #         print()



if __name__ == '__main__':
    count_wins()