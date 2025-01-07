rm -rf ./logs
rm -rf ./logs_4
rm -rf ./logs_8

./run_games.sh -p 4 100
mv ./logs ./logs_4
./run_games.sh -p 8 100
mv ./logs ./logs_8