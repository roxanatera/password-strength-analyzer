import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.patterns import detect_patterns, get_suggestions, _deleet


class TestDeleet:
    def test_at_becomes_a(self):
        assert _deleet("p@ss") == "pass"

    def test_zero_becomes_o(self):
        assert _deleet("passw0rd") == "password"

    def test_three_becomes_e(self):
        assert _deleet("s3cr3t") == "secret"

    def test_no_leet_unchanged(self):
        assert _deleet("hello") == "hello"


class TestDetectPatterns:
    def test_keyboard_walk_detected(self):
        warnings = detect_patterns("qwerty123")
        types = [w["type"] for w in warnings]
        assert "keyboard_walk" in types

    def test_common_word_detected(self):
        warnings = detect_patterns("password")
        types = [w["type"] for w in warnings]
        assert "common_word" in types

    def test_leet_speak_detected(self):
        warnings = detect_patterns("p@ssw0rd")
        types = [w["type"] for w in warnings]
        assert "leet_speak" in types

    def test_repeated_chars_detected(self):
        warnings = detect_patterns("aaabbbccc")
        types = [w["type"] for w in warnings]
        assert "repeated_chars" in types

    def test_year_detected(self):
        warnings = detect_patterns("summer2024")
        types = [w["type"] for w in warnings]
        assert "year" in types

    def test_digits_only_detected(self):
        warnings = detect_patterns("123456789")
        types = [w["type"] for w in warnings]
        assert "digits_only" in types

    def test_too_short_detected(self):
        warnings = detect_patterns("abc")
        types = [w["type"] for w in warnings]
        assert "too_short" in types

    def test_strong_password_no_warnings(self):
        warnings = detect_patterns("Tr0ub4dor&3!")
        # Should have no critical warnings
        critical = [w for w in warnings if w["penalty"] >= 25]
        assert len(critical) == 0

    def test_warnings_have_required_keys(self):
        warnings = detect_patterns("password123")
        for w in warnings:
            assert "type" in w
            assert "detail" in w
            assert "penalty" in w


class TestGetSuggestions:
    def test_short_password_gets_length_tip(self):
        warnings = detect_patterns("abc")
        tips = get_suggestions("abc", warnings)
        assert any("12 characters" in t for t in tips)

    def test_common_word_gets_dictionary_tip(self):
        warnings = detect_patterns("password123")
        tips = get_suggestions("password123", warnings)
        assert any("dictionary" in t for t in tips)

    def test_strong_password_gets_positive_feedback(self):
        warnings = detect_patterns("Tr0ub4dor&3!")
        tips = get_suggestions("Tr0ub4dor&3!", warnings)
        assert any("good" in t.lower() for t in tips)

    def test_suggestions_are_strings(self):
        warnings = detect_patterns("qwerty")
        tips = get_suggestions("qwerty", warnings)
        assert all(isinstance(t, str) for t in tips)
