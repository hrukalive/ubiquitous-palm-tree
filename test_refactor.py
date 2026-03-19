import unittest
from unittest.mock import patch

from matchmaker import generate_tiebreaker_matchups
from result_collector import generate_leaderboard
from tie_detector import detect_ties


class TieDetectorTests(unittest.TestCase):
    def test_detect_ties_uses_conservative_score(self):
        state = {
            "ratings": {
                "sub_a": {"mu": 30.0, "sigma": 5.0},
                "sub_b": {"mu": 29.0, "sigma": 14.0 / 3.0},
                "sub_c": {"mu": 40.0, "sigma": 5.0},
            }
        }

        tied_groups = detect_ties(state, precision=6)

        self.assertEqual(tied_groups, [["sub_a", "sub_b"]])


class LeaderboardTests(unittest.TestCase):
    @patch(
        "result_collector.load_submission_details",
        return_value={
            "sub_1": {
                "name": "Alice",
                "username": "alice",
                "profile": "Alpha",
                "student_id": "stu-1",
            },
            "sub_2": {
                "name": "Alice",
                "username": "alice",
                "profile": "Beta",
                "student_id": "stu-1",
            },
            "sub_3": {
                "name": "Bob",
                "username": "bob",
                "profile": "Gamma",
                "student_id": "stu-2",
            },
        },
    )
    def test_leaderboard_keeps_best_submission_per_student(self, _mock_details):
        state = {
            "ratings": {
                "sub_1": {"mu": 30.0, "sigma": 5.0},
                "sub_2": {"mu": 30.0, "sigma": 5.0},
                "sub_3": {"mu": 28.0, "sigma": 5.0},
            },
            "records": {
                "sub_1": {"wins": 2, "losses": 1, "draws": 0},
                "sub_2": {"wins": 2, "losses": 1, "draws": 0},
                "sub_3": {"wins": 1, "losses": 2, "draws": 0},
            },
        }
        tiebreak_results = {
            "score_precision": 6,
            "state_fingerprint": "ignored-in-direct-call",
            "rankings": {
                "sub_1": {"main_score": 15.0, "score": 10.0, "rank": 2},
                "sub_2": {"main_score": 15.0, "score": 12.0, "rank": 1},
            }
        }

        leaderboard = generate_leaderboard(state, tiebreak_results)

        self.assertIn("sub_2", leaderboard)
        self.assertIn("sub_3", leaderboard)
        self.assertNotIn("sub_1", leaderboard)

    @patch(
        "result_collector.load_submission_details",
        return_value={
            "sub_a": {
                "name": "Alice A",
                "username": "alicea",
                "profile": "A",
                "student_id": "stu-a",
            },
            "sub_b": {
                "name": "Bob B",
                "username": "bobb",
                "profile": "B",
                "student_id": "stu-b",
            },
        },
    )
    def test_leaderboard_uses_tiebreak_within_same_main_score_bucket(self, _mock_details):
        state = {
            "ratings": {
                "sub_a": {"mu": 30.0000004, "sigma": 5.0},
                "sub_b": {"mu": 30.0000003, "sigma": 5.0},
            },
            "records": {
                "sub_a": {"wins": 1, "losses": 0, "draws": 0},
                "sub_b": {"wins": 1, "losses": 0, "draws": 0},
            },
        }
        tiebreak_results = {
            "score_precision": 6,
            "state_fingerprint": "ignored-in-direct-call",
            "rankings": {
                "sub_a": {"main_score": 15.0, "score": 10.0, "rank": 2},
                "sub_b": {"main_score": 15.0, "score": 12.0, "rank": 1},
            },
        }

        leaderboard = generate_leaderboard(state, tiebreak_results)
        sub_b_index = leaderboard.index("sub_b")
        sub_a_index = leaderboard.index("sub_a")

        self.assertLess(sub_b_index, sub_a_index)


class TiebreakMatchmakerTests(unittest.TestCase):
    def test_small_tiebreak_group_uses_full_round_robin(self):
        state = {
            "ratings": {
                "sub_1": {"mu": 25.0, "sigma": 8.333},
                "sub_2": {"mu": 25.0, "sigma": 8.333},
                "sub_3": {"mu": 25.0, "sigma": 8.333},
            },
            "match_history": [],
        }

        matches = generate_tiebreaker_matchups(
            ["sub_1", "sub_2", "sub_3"], state, round_num=1
        )

        self.assertEqual(len(matches), 6)
        self.assertTrue(all(match["black"] is not None for match in matches))
        pairings = {
            tuple(sorted((match["white"], match["black"])))
            for match in matches
        }
        self.assertEqual(
            pairings,
            {
                ("sub_1", "sub_2"),
                ("sub_1", "sub_3"),
                ("sub_2", "sub_3"),
            },
        )

    def test_odd_sized_tiebreak_group_has_no_byes(self):
        state = {
            "ratings": {
                f"sub_{idx}": {"mu": 25.0, "sigma": 8.333}
                for idx in range(1, 6)
            },
            "match_history": [],
        }

        players = [f"sub_{idx}" for idx in range(1, 6)]
        matches = generate_tiebreaker_matchups(players, state, round_num=1)

        self.assertTrue(matches)
        self.assertTrue(all(match["black"] is not None for match in matches))
        covered = set()
        for match in matches:
            covered.add(match["white"])
            covered.add(match["black"])
        self.assertEqual(covered, set(players))


if __name__ == "__main__":
    unittest.main()
