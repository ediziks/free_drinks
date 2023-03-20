import os
import sys
import unittest
from datetime import time
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from free_drinks.main import FreeDrinkEstimator


class TestFreeDrinkEstimator(unittest.TestCase):
    def setUp(self):
        # Creates a FreeDrinkEstimator object with a valid config string
        self.fd = FreeDrinkEstimator("Mon: 1200-1400 Tue: 0900-1100 Fri: 0000-2400")
        self.fd_case2 = FreeDrinkEstimator(
            "Mon: 1200-1400 Tue: 0900-1100 Fri: 2200-2400 Fri: 2000-2200"
        )
        self.fd_case3 = FreeDrinkEstimator("")
        self.fd_case4 = FreeDrinkEstimator("illegal input")

    def test_is_valid_day(self):
        self.assertTrue(self.fd.is_valid_day("Mon"))
        self.assertTrue(self.fd.is_valid_day("Tue"))
        self.assertTrue(self.fd.is_valid_day("Fri"))
        with self.assertRaises(AssertionError):
            self.fd.is_valid_day("Tues")

    def test_is_valid_time_range(self):
        self.assertTrue(self.fd.is_valid_time_range("1200-1400"))
        self.assertTrue(self.fd.is_valid_time_range("0900-1100"))
        self.assertTrue(self.fd.is_valid_time_range("0000-2400"))
        with self.assertRaises(AssertionError):
            self.fd.is_valid_time_range("1100-0900")
        with self.assertRaises(AssertionError):
            self.fd.is_valid_time_range("2400-0000")
        with self.assertRaises(AssertionError):
            self.fd.is_valid_time_range("12:00-14:00")

    def test_parse_time_range(self):
        self.assertEqual(
            self.fd.parse_time_range("1200-1400"), (time(12, 0), time(14, 0))
        )
        self.assertEqual(
            self.fd.parse_time_range("0900-1100"), (time(9, 0), time(11, 0))
        )
        self.assertEqual(
            self.fd.parse_time_range("0000-2400"),
            (time(0, 0), time(23, 59, 59, 999999)),
        )
        self.assertNotEqual(
            self.fd.parse_time_range("0900-1100"), (time(9, 0), time(10, 0))
        )

    def test_parse_config_string(self):
        expected = {
            "mon": [(time(12, 0), time(14, 0))],
            "tue": [(time(9, 0), time(11, 0))],
            "fri": [(time(0, 0), time(23, 59, 59, 999999))],
        }
        self.assertEqual(self.fd.parse_config_string(), expected)

        expected_case2 = {
            "mon": [(time(12, 0), time(14, 0))],
            "tue": [(time(9, 0), time(11, 0))],
            "fri": [
                (time(22, 0), time(23, 59, 59, 999999)),
                (time(20, 0), time(22, 0)),
            ],
        }
        self.assertEqual(self.fd_case2.parse_config_string(), expected_case2)

        with self.assertRaises(AssertionError):
            self.fd_case3.parse_config_string()

        with self.assertRaises(AssertionError):
            self.fd_case4.parse_config_string()

    # Test with the config string that allows/disallows free drinks on freezed time
    def test_can_get_free_drink(self):
        with freeze_time("2023-03-20 12:32"):  # Monday, 12:30 PM
            self.assertTrue(self.fd.can_get_free_drink())

        with freeze_time("2023-03-21 12:30"):  # Tuesday, 12:30 AM
            self.assertFalse(self.fd.can_get_free_drink())

        with freeze_time("2023-03-24 12:30"):  # Friday, 23:59 PM
            self.assertTrue(self.fd.can_get_free_drink())

        with freeze_time("2023-03-25 12:30"):  # Friday, 24:00 AM -> Saturday 00:00 AM
            self.assertFalse(self.fd.can_get_free_drink())


if __name__ == "__main__":
    unittest.main()
