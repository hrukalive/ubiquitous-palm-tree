"""
Tournament Configuration
All constants and TrueSkill environment parameters for Breakthrough tournament.
"""

import os
import trueskill

# Directory paths (configurable via environment variables)
SUBMISSIONS_DIR = r"D:\Downloads\submissions_final\assignment_7451151_export"
METADATA_FILE = os.path.join(SUBMISSIONS_DIR, "submission_metadata.yml")
RESULTS_DIR = "results"
STATE_FILE = "tournament_state.json"
LEADERBOARD_FILE = "leaderboard.txt"

# Eligibility
MIN_SCORE = 50.0  # Only submissions with Gradescope score >= 50.0 are eligible

# Game settings
AGENT_DEPTH = 3  # AlphaBeta search depth (uniform for all agents for fairness)
MAX_MOVES = 4000  # Per-game move limit (draws after this)
GAME_TIMEOUT = 60000  # Per-game timeout in seconds (5 minutes)

# Tournament settings
GAMES_PER_PAIRING = 2  # 2 = play both colors (white & black), 1 = single color
MAX_PARALLEL_WORKERS = 16  # For ProcessPoolExecutor
REPEAT_WINDOW = 3  # Avoid rematches within this many rounds

# TrueSkill parameters
# Using standard defaults from Microsoft TrueSkill paper
TS_MU = 25.0  # Default skill mean
TS_SIGMA = 25.0 / 3  # Default skill standard deviation (8.333)
TS_BETA = 25.0 / 6  # Skill class width (4.166)
TS_TAU = (
    25.0 / 300
)  # Dynamics factor (0.0833) - how much uncertainty increases per round
TS_DRAW_PROBABILITY = 0.05  # 5% draw probability (low for Breakthrough)

# Create TrueSkill environment
trueskill_env = trueskill.TrueSkill(
    mu=TS_MU,
    sigma=TS_SIGMA,
    beta=TS_BETA,
    tau=TS_TAU,
    draw_probability=TS_DRAW_PROBABILITY,
)

# Random seed for reproducibility
TOURNAMENT_SEED = 42
