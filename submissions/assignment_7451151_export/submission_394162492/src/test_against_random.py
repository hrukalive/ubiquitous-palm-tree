# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE



from breakthrough import ag_eval_fn
from breakthrough import play_game
from breakthrough_agent import AlphaBetaAgent, RandomAgent
from src.breakthrough import defensive_eval_2


def main():
    win_count = 0
    for _ in range(5):  # Play each matchup 5 times
        w_agent = RandomAgent("Random")
        b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_2)
        res = play_game(w_agent, b_agent, max_moves=400, progress=True)
        print(res)
        if res["winner"] == "black":
            win_count += 1
    for _ in range(5):  # Play each matchup 5 times
        w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=ag_eval_fn)
        b_agent = RandomAgent("Random")
        res = play_game(w_agent, b_agent, max_moves=400, progress=True)
        print(res)
        if res["winner"] == "white":
            win_count += 1
    print(win_count)
    print("Pass." if win_count >= 7 else "Fail.")

if __name__ == '__main__':
    main()
