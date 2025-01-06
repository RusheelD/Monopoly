count=${1:-1}

for ((i=1; i<=count; i++)); do
    echo "Running game $i"
    touch ./logs/game_$i.log
    python main.py > ./logs/game_$i.log
done