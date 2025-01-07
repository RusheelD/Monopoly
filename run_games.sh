count=1
players=4
max_turns=2500

while getopts "p:m:" opt; do
    case $opt in
        p)
            players=$OPTARG
            ;;
        m)
            max_turns=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))
count=${1:-1}

mkdir -p ./logs

echo "Running $count games with $players players and $max_turns turns at most"

for ((i=1; i<=count; i++)); do
    echo "Running game $i"
    touch ./logs/game_$i.log
    python main.py -d -p $players -m $max_turns > ./logs/game_$i.log
done