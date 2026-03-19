"""
Tournament configuration for Breakthrough tournaments.
"""

import os

import trueskill

# Submission exports live under this root. Each export directory is expected to
# contain a submission_metadata.yml plus submission_<id>/ folders.
SUBMISSIONS_DIR = os.environ.get("BREAKTHROUGH_SUBMISSIONS_ROOT", "submissions")
LEADERBOARD_FILE = os.environ.get("BREAKTHROUGH_LEADERBOARD_FILE", "leaderboard.txt")
RESULTS_DIR = os.environ.get("BREAKTHROUGH_RESULTS_DIR", "results")
STATE_FILE = os.environ.get("BREAKTHROUGH_STATE_FILE", "tournament_state.json")
TIEBREAK_FILE = os.environ.get("BREAKTHROUGH_TIEBREAK_FILE", "tiebreak_results.json")

# Eligibility
MIN_SCORE = 50.0

# Game settings
AGENT_DEPTH = 2
MAX_MOVES = 4000
GAME_TIMEOUT = 300  # 5 minutes per game

# Tournament settings
GAMES_PER_PAIRING = 2
MAX_PARALLEL_WORKERS = 16
REPEAT_WINDOW = 3

# Tiebreak settings
TIEBREAK_SCORE_PRECISION = 6
TIEBREAK_MAX_ROUNDS = 3

# TrueSkill parameters
TS_MU = 25.0
TS_SIGMA = 25.0 / 3
TS_BETA = 25.0 / 6
TS_TAU = 25.0 / 300
TS_DRAW_PROBABILITY = 0.05

trueskill_env = trueskill.TrueSkill(
    mu=TS_MU,
    sigma=TS_SIGMA,
    beta=TS_BETA,
    tau=TS_TAU,
    draw_probability=TS_DRAW_PROBABILITY,
)

TOURNAMENT_SEED = 42
