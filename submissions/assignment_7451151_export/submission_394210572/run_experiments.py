import json

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
# YOUR NAME: Peter Liehr III
# YOUR WPI ID: 478388612
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
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

def main():
    ...  # YOUR EXPERIMENTS HERE

    # First Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = MinimaxAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = offensive_eval_1
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = offensive_eval_1
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Minimax(Offensive Evaluation 1) vs Alpha-beta(Offensive Evaluation 1)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")


    # Second Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = AlphaBetaAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = offensive_eval_2
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = defensive_eval_1
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 1)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")


    # Third Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = AlphaBetaAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = defensive_eval_2
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = offensive_eval_1
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Alpha-beta(Defensive Evaluation 2) vs Alpha-beta(Offensive Evaluation 1)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")


    # Fourth Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = AlphaBetaAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = offensive_eval_2
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = offensive_eval_1
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Offensive Evaluation 1)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")


    # Fifth Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = AlphaBetaAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = defensive_eval_2
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = defensive_eval_1
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Alpha-beta(Defensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 1)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")


    # Sixth Experiment!
    whiteWins = 0
    blackWins = 0

    avgWhiteNode = 0
    avgBlackNode = 0

    avgWhiteNodePerMove = 0
    avgBlackNodePerMove = 0

    avgWhiteTimePerMove = 0
    avgBlackTimePerMove = 0

    avgWhiteCaptures = 0
    avgBlackCaptures = 0


    for i in range(0, 100):
        if i == 99:
            show = True
        else:
            show = False
    
        whitePlayer = AlphaBetaAgent(
            name = "Whitey",
            depth = 3,
            eval_fn = offensive_eval_2
        )

        blackPlayer = AlphaBetaAgent(
            name = "Blackey",
            depth = 3,
            eval_fn = defensive_eval_2
        )

        gameResult = play_game(whitePlayer, 
                                blackPlayer,
                                max_moves = 400,
                                display = show,
                                progress = True)
        

        if gameResult['winner'] == 'white':
            whiteWins = whiteWins + 1
        else:
            blackWins = blackWins + 1

        avgWhiteNode = (avgWhiteNode  + gameResult['white_nodes'])
        avgBlackNode = (avgBlackNode  + gameResult['black_nodes'])

        avgWhiteNodePerMove = (avgWhiteNodePerMove  + gameResult['white_nodes_per_move'])
        avgBlackNodePerMove = (avgBlackNodePerMove  + gameResult['black_nodes_per_move'])
        avgWhiteTimePerMove = (avgWhiteTimePerMove  + gameResult['white_time_per_move'])
        avgBlackTimePerMove = (avgBlackTimePerMove  + gameResult['black_time_per_move'])

        avgWhiteCaptures = (avgWhiteCaptures  + gameResult['white_captures'])
        avgBlackCaptures = (avgBlackCaptures  + gameResult['black_captures'])

    print("")
    print("Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 2)")
    print("---------------------------------------------------------------------")
    print("    - White Win Count: ", whiteWins)
    print("    - Black Win Count: ", blackWins)
    print("")
    print("----------------")
    print("    - Average White Nodes Expanded: ", avgWhiteNode / 100.0)
    print("    - Average Black Nodes Expanded: ", avgBlackNode / 100.0)
    print("")
    print("----------------")
    print("    - Average White Nodes Per Move: ", avgWhiteNodePerMove / 100.0)
    print("    - Average Black Nodes Per Move: ", avgBlackNodePerMove / 100.0)
    print("")
    print("    - Average White Time Per Move: ", avgWhiteTimePerMove / 100.0)
    print("    - Average Black Time Per Move: ", avgBlackTimePerMove / 100.0)
    print("")
    print("----------------")
    print("    - Average White Captures: ", avgWhiteCaptures / 100.0)
    print("    - Average Black Captures: ", avgBlackCaptures / 100.0)
    print("")
    print("")
    print("")
    



if __name__ == '__main__':
    main()
