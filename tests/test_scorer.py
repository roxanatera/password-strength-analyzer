import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scorer import score_password


class TestScorePassword:
    def test_returns_required_keys(self):
        result = score_password("TestPass123!")
        required = {"password", "score", "label", "color", "entropy", "crack_time", "warnings", "suggestions"}
        assert required.issubset(result.keys())

    def test_score_between_0_and_100(self):
        for pwd in ["a", "password", "Tr0ub4dor&3!", "correct-horse-battery-staple"]:
            result = score_password(pwd)
            assert 0 <= result["score"] <= 100

    def test_very_weak_password(self):
        result = score_password("123456")
        assert result["label"] == "VERY WEAK"
        assert result["score"] < 20

    def test_weak_password(self):
        result = score_password("password123")
        assert result["score"] < 50

    def test_strong_password(self):
        result = score_password("Tr0ub4dor&3!")
        assert result["score"] >= 80
        assert result["label"] in ("STRONG", "VERY STRONG")

    def test_very_strong_passphrase(self):
        result = score_password("correct-horse-battery-staple")
        assert result["score"] >= 80
        assert result["entropy"] > 100

    def test_common_password_penalized(self):
        common = score_password("qwerty")
        unique = score_password("Xk9#mP2!vL")
        assert unique["score"] > common["score"]

    def test_longer_password_higher_entropy(self):
        short = score_password("Abc1!")
        long = score_password("Abc1!Abc1!Abc1!")
        assert long["entropy"] > short["entropy"]

    def test_color_matches_label(self):
        color_map = {
            "VERY WEAK": "red",
            "WEAK": "orange1",
            "FAIR": "yellow",
            "STRONG": "green",
            "VERY STRONG": "bright_green",
        }
        for pwd in ["123", "password1", "Hello123", "Tr0ub4dor&3!", "correct-horse-battery-staple-2024!"]:
            result = score_password(pwd)
            assert result["color"] == color_map[result["label"]]

    def test_warnings_is_list(self):
        result = score_password("anything")
        assert isinstance(result["warnings"], list)

    def test_suggestions_is_list(self):
        result = score_password("anything")
        assert isinstance(result["suggestions"], list)
