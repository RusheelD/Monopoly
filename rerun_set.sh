rm -rf ./logs
rm -rf ./logs_4
rm -rf ./logs_8
rm -rf ./logs_4_1000
rm -rf ./logs_8_1000

./run_games.sh -p 4 100
mv ./logs ./logs_4
./run_games.sh -p 8 100
mv ./logs ./logs_8
./run_games.sh -p 4 1000
mv ./logs ./logs_4_1000
./run_games.sh -p 8 1000
mv ./logs ./logs_8_1000
python count_wins.py ./logs_4
python count_wins.py ./logs_8
python count_wins.py ./logs_4_1000
python count_wins.py ./logs_8_1000

read -p "Press any key to continue... " -n1 -s