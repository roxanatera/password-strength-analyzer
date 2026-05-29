import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entropy import calculate_entropy, get_charset_size, estimate_crack_time


class TestCharsetSize:
    def test_lowercase_only(self):
        assert get_charset_size("abcdef") == 26

    def test_lowercase_uppercase(self):
        assert get_charset_size("abcABC") == 52

    def test_with_digits(self):
        assert get_charset_size("abc123") == 36

    def test_full_charset(self):
        assert get_charset_size("aA1!") == 94

    def test_digits_only(self):
        assert get_charset_size("123456") == 10


class TestCalculateEntropy:
    def test_short_password_low_entropy(self):
        entropy = calculate_entropy("abc")
        assert entropy < 20

    def test_long_password_high_entropy(self):
        entropy = calculate_entropy("correct-horse-battery-staple")
        assert entropy > 100

    def test_mixed_charset_higher_than_lowercase(self):
        lower_entropy = calculate_entropy("abcdefghij")
        mixed_entropy = calculate_entropy("aB1!eF2@iJ")
        assert mixed_entropy > lower_entropy

    def test_entropy_increases_with_length(self):
        short = calculate_entropy("abc123")
        long = calculate_entropy("abc123abc123")
        assert long > short


class TestEstimateCrackTime:
    def test_very_low_entropy_is_instant(self):
        assert estimate_crack_time(10) == "instantly"

    def test_high_entropy_is_centuries(self):
        assert estimate_crack_time(100) == "centuries"

    def test_medium_entropy_returns_string(self):
        result = estimate_crack_time(40)
        assert isinstance(result, str)
        assert len(result) > 0
