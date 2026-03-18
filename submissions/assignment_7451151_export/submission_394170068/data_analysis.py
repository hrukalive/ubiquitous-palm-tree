import json
import matplotlib.pyplot as plt

def plot_matchup(json_path, matchup_key,save_fig_name=None):
    # Load data
    with open(json_path, "r") as f:
        data = json.load(f)

    match = data[matchup_key]
    matchup_key_split = matchup_key.split(" v ")
    reversed_match_key = matchup_key_split[1] + " v "+ matchup_key_split[0]
    reversed_match = data[reversed_match_key]
    # Metrics to plot (paired white vs black)
    
    labels = [
        "Nodes Expanded",
        "Nodes / Move",
        "Time / Move (s)",
        "Captures"
    ]

    white_values = [
        (match["white_nodes"] + reversed_match["black_nodes"])/2,
        (match["white_nodes_per_move"] + reversed_match["black_nodes_per_move"])/2,
        (match["white_time_per_move"] + reversed_match["black_time_per_move"])/2,
        (match["white_captures"] + reversed_match["black_captures"])/2
    ]

    black_values = [
        (reversed_match["white_nodes"] + match["black_nodes"])/2,
        (reversed_match["white_nodes_per_move"] + match["black_nodes_per_move"])/2,
        (reversed_match["white_time_per_move"] + match["black_time_per_move"])/2,
        (reversed_match["white_captures"] + match["black_captures"])/2
    ]
    
    white_wins = 0
    black_wins = 0

    if match["winner"] == "white":
        white_wins += 1
    elif match["winner"] == "black":
        black_wins += 1

    if reversed_match["winner"] == "white":
        black_wins += 1
    elif reversed_match["winner"] == "black":
        white_wins += 1
        
    
    # white_values = [
    #     match["white_nodes"],
    #     match["white_nodes_per_move"],
    #     match["white_time_per_move"],
    #     match["white_captures"]
    # ]

    # black_values = [
    #     match["black_nodes"],
    #     match["black_nodes_per_move"],
    #     match["black_time_per_move"],
    #     match["black_captures"]
    #     ]

    winner_name = match["white_name"] if white_wins > black_wins else match["black_name"]
    result = f"{matchup_key} performance analysis. Winner: {winner_name} in {(match["total_moves"]+reversed_match["total_moves"])/2} moves. Total nodes expanded: White {int(white_values[0]):,d}, Black {int(black_values[0]):,d}. Average nodes per move: White {white_values[1]:,.2f}, Black {black_values[1]:,.2f}. Average time per move: White {white_values[2]:.3f}, Black {black_values[2]:.3f}. Captures: White {int(white_values[3])}, Black {int(black_values[3])}."
    result = result.replace("_","\\_")
    print(result)
    x = range(len(labels))
    width = 0.35

    # Plot
    plt.figure()
    plt.bar(x, white_values, width, label=match["white_name"])
    plt.bar([i + width for i in x], black_values, width, label=match["black_name"])

    plt.xticks([i + width / 2 for i in x], labels, rotation=20)
    plt.ylabel("Value")
    plt.title(f"Matchup Statistics\n{matchup_key}")
    legend = plt.legend()
    legend_texts = legend.get_texts()

    if white_wins > black_wins:
        legend_texts[0].set_color("green")
        legend_texts[1].set_color("red")
    elif black_wins > white_wins:
        legend_texts[0].set_color("red")
        legend_texts[1].set_color("green")
    else:
        legend_texts[0].set_color((0.78, 0.72, 0.35, 0.85))
        legend_texts[1].set_color((0.78, 0.72, 0.35, 0.85))
    # plt.legend()
    plt.tight_layout()
    plt.yscale('log')
    if save_fig_name:
        plt.savefig(save_fig_name)
    # plt.show()


if __name__ == "__main__":
    match_ups = [
        "offensive_eval_2 v defensive_eval_2",
        "defensive_eval_1 v offensive_eval_2",
        "offensive_eval_1 v defensive_eval_2",
        "offensive_eval_1 v offensive_eval_2",
        "defensive_eval_1 v defensive_eval_2",
        "offensive_eval_1_MiniMax v offensive_eval_1_AlphaBeta"
        ]
    for match in match_ups:
        file = match.replace(" ","_")
        plot_matchup(json_path="data/round_robin_results.json",matchup_key=match,save_fig_name="figures/"+file)