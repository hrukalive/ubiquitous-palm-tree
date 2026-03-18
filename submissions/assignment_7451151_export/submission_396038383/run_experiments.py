import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
from tqdm import tqdm
from datetime import datetime
import json
from datetime import datetime

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Jonah
# YOUR WPI ID: 901011123
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
# Perform the necessary experiments here to generate data required by the report.
def run_matchup(label, white_agent, black_agent, max_moves=400, runs=1, progress=False, display_final=False):
    """
    Runs a matchup 'runs' times. Returns a list of result dicts (from play_game),
    plus (optionally) final board render for the last run.
    """
    results = []
    last_final_board = None

    for i in range(runs):
        # eset tracking arrays so averages are per-game, not cumulative
        white_agent.reset()
        black_agent.reset()

        res = play_game(white_agent, black_agent, max_moves=max_moves, display=False, progress=progress)
        res["matchup"] = label
        res["run_index"] = i + 1
        results.append(res)

        if display_final and i == runs - 1:
            white_agent.reset()
            black_agent.reset()
            _ = play_game(white_agent, black_agent, max_moves=max_moves, display=True, progress=False)

    return results


def pretty_print_results(label, results):
    """
    Print a report-friendly summary. If multiple runs, prints per-run + simple averages.
    """
    print("\n" + "=" * 80)
    print(label)
    print("=" * 80)

    # Per-run lines
    for r in results:
        print(
            f"Run {r['run_index']}: winner={r['winner']}, total_moves={r['total_moves']}, "
            f"captures(W/B)={r['white_captures']}/{r['black_captures']}, "
            f"nodes(W/B)={r['white_nodes']}/{r['black_nodes']}, "
            f"avg_nodes_per_move(W/B)={r['white_nodes_per_move']:.1f}/{r['black_nodes_per_move']:.1f}, "
            f"avg_time_per_move(W/B)={r['white_time_per_move']:.4f}/{r['black_time_per_move']:.4f}"
        )

    # If multiple runs, compute averages
    if len(results) > 1:
        avg = lambda k: sum(r[k] for r in results) / len(results)
        print("\nAverages over runs:")
        print(f"  avg total_moves: {avg('total_moves'):.2f}")
        print(f"  avg white_nodes / black_nodes: {avg('white_nodes'):.2f} / {avg('black_nodes'):.2f}")
        print(
            f"  avg white_nodes_per_move / black_nodes_per_move: "
            f"{avg('white_nodes_per_move'):.2f} / {avg('black_nodes_per_move'):.2f}"
        )
        print(
            f"  avg white_time_per_move / black_time_per_move: "
            f"{avg('white_time_per_move'):.4f} / {avg('black_time_per_move'):.4f}"
        )
        print(f"  avg captures (W/B): {avg('white_captures'):.2f} / {avg('black_captures'):.2f}")

        winners = [r["winner"] for r in results]
        print(f"  winners: {winners}")

        print("\nFinal Board:")

        board = r["final_board"]

        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}

        for row in board:
            print("".join(chars[cell] for cell in row))

def main():

    runs_per_matchup = 1
    max_moves = 400
    show_progress_bar = False  # True = tqdm bar for each game
    display_final_board = False  # True prints final board for each matchup (slower, noisier)


    # Depths: assignment suggests minimax depth 2-3 and alpha-beta deeper
    minimax_depth = 3
    alphabeta_depth = 4

    #  agents used in experiments
    mm_off1 = MinimaxAgent(f"Minimax d={minimax_depth} Off1", depth=minimax_depth, eval_fn=offensive_eval_1)

    ab_off1 = AlphaBetaAgent(f"AlphaBeta d={alphabeta_depth} Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)
    ab_def1 = AlphaBetaAgent(f"AlphaBeta d={alphabeta_depth} Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1)

    ab_off2 = AlphaBetaAgent(f"AlphaBeta d={alphabeta_depth} Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2)
    ab_def2 = AlphaBetaAgent(f"AlphaBeta d={alphabeta_depth} Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2)

    matchups = [
        ("1) Minimax (Off1) vs Alpha-beta (Off1)", mm_off1, ab_off1),
        ("2) Alpha-beta (Off2) vs Alpha-beta (Def1)", ab_off2, ab_def1),
        ("3) Alpha-beta (Def2) vs Alpha-beta (Off1)", ab_def2, ab_off1),
        ("4) Alpha-beta (Off2) vs Alpha-beta (Off1)", ab_off2, ab_off1),
        ("5) Alpha-beta (Def2) vs Alpha-beta (Def1)", ab_def2, ab_def1),
        ("6) Alpha-beta (Off2) vs Alpha-beta (Def2)", ab_off2, ab_def2),
    ]

    all_results = {
        "meta": {
            "runs_per_matchup": runs_per_matchup,
            "max_moves": max_moves,
            "minimax_depth": minimax_depth,
            "alphabeta_depth": alphabeta_depth,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        },
        "matchups": []
    }

    for label, white_agent, black_agent in matchups:
        results = run_matchup(
            label,
            white_agent,
            black_agent,
            max_moves=max_moves,
            runs=runs_per_matchup,
            progress=show_progress_bar,
            display_final=display_final_board
        )
        pretty_print_results(label, results)
        all_results["matchups"].append({
            "label": label,
            "white_agent": white_agent.name,
            "black_agent": black_agent.name,
            "results": results
        })


    out_file = "breakthrough_experiment_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print("\nSaved results to:", out_file)


if __name__ == '__main__':
    main()
