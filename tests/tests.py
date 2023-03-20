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
        self.fd_case1 = FreeDrinkEstimator(
            "Mon: 1200-1400 Tue: 0900-1100 Fri: 0000-2400"
        )
        self.fd_case2 = FreeDrinkEstimator(
            "Mon: 1200-1400 Tue: 0900-1100 Fri: 2200-2400 Fri: 2000-2200"
        )
        self.fd_case3 = FreeDrinkEstimator("")
        self.fd_case4 = FreeDrinkEstimator("illegal input")

    def test_is_valid_day_valid(self):
        """
        Test if the is_valid_day method returns True for valid day strings.
        """
        self.assertTrue(self.fd_case1.is_valid_day("Mon"))
        self.assertTrue(self.fd_case1.is_valid_day("Tue"))
        self.assertTrue(self.fd_case1.is_valid_day("Wed"))
        self.assertTrue(self.fd_case1.is_valid_day("Thu"))
        self.assertTrue(self.fd_case1.is_valid_day("Fri"))
        self.assertTrue(self.fd_case1.is_valid_day("Sat"))
        self.assertTrue(self.fd_case1.is_valid_day("Sun"))

    def test_is_valid_day_invalid(self):
        """
        Test if the is_valid_day method asserts Error for invalid day strings.
        """
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_day("Tues")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_day("Monday")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_day("")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_day(" ")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_day("123")

    def test_is_valid_time_range_valid(self):
        """
        Test if the is_valid_time_range method returns True for valid time range strings.
        """
        self.assertTrue(self.fd_case1.is_valid_time_range("1200-1400"))
        self.assertTrue(self.fd_case1.is_valid_time_range("0900-1100"))
        self.assertTrue(self.fd_case1.is_valid_time_range("0000-2400"))

    def test_is_valid_time_range_invalid(self):
        """
        Test if the is_valid_time_range method asserts Error for invalid time range strings.
        """
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_time_range("1100-0900")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_time_range("2400-0000")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_time_range("12:00-14:00")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_time_range("hhmm-hhmm")
        with self.assertRaises(AssertionError):
            self.fd_case1.is_valid_time_range("")

    def test_parse_time_range_valid(self):
        """
        Test if the parse_time_range method returns the correct time tuple for valid time range strings.
        """
        self.assertEqual(
            self.fd_case1.parse_time_range("1200-1400"), (time(12, 0), time(14, 0))
        )
        self.assertEqual(
            self.fd_case1.parse_time_range("0900-1100"), (time(9, 0), time(11, 0))
        )
        self.assertEqual(
            self.fd_case1.parse_time_range("0000-2400"),
            (time(0, 0), time(23, 59, 59, 999999)),
        )

    def test_parse_time_range_invalid(self):
        """
        Test if the parse_time_range method asserts Error for invalid time range strings.
        """
        self.assertNotEqual(
            self.fd_case1.parse_time_range("0900-1100"), (time(9, 0), time(10, 0))
        )
        self.assertNotEqual(
            self.fd_case1.parse_time_range("0000-2400"),
            (time(0, 0), time(23, 59, 59, 999998)),
        )

    def test_parse_config_string_valid(self):
        """
        Test if the parse_config_string method returns the correct dictionary for valid config strings.
        """
        expected = {
            "mon": [(time(12, 0), time(14, 0))],
            "tue": [(time(9, 0), time(11, 0))],
            "fri": [(time(0, 0), time(23, 59, 59, 999999))],
        }
        self.assertEqual(self.fd_case1.parse_config_string(), expected)

        expected_case2 = {
            "mon": [(time(12, 0), time(14, 0))],
            "tue": [(time(9, 0), time(11, 0))],
            "fri": [
                (time(22, 0), time(23, 59, 59, 999999)),
                (time(20, 0), time(22, 0)),
            ],
        }
        self.assertEqual(self.fd_case2.parse_config_string(), expected_case2)

    def test_parse_config_string_invalid(self):
        """
        Test if the parse_config_string method asserts Error for invalid config strings.
        """
        with self.assertRaises(AssertionError):
            self.fd_case3.parse_config_string()

        with self.assertRaises(AssertionError):
            self.fd_case4.parse_config_string()

    def test_can_get_free_drink_valid(self):
        """
        Test if the can_get_free_drink method returns True for valid time strings.
        Tested with the config string that allows free drinks on freezed time
        """
        # fd_case1 -> Mon: 1200-1400 Tue: 0900-1100 Fri: 0000-2400
        with freeze_time("2023-03-20 12:30"):  # Monday, 12:30 PM
            self.assertTrue(self.fd_case1.can_get_free_drink())

        with freeze_time("2023-03-24 23:59"):  # Friday, 23:59 PM
            self.assertTrue(self.fd_case1.can_get_free_drink())

        # fd_case2 -> Mon: 1200-1400 Tue: 0900-1100 Fri: 2200-2400 Fri: 2000-2200
        with freeze_time("2023-03-24 20:30"):  # Friday, 20:30 PM
            self.assertTrue(self.fd_case2.can_get_free_drink())

        with freeze_time("2023-03-24 22:30"):  # Friday, 22:30 PM
            self.assertTrue(self.fd_case2.can_get_free_drink())

    def test_can_get_free_drink_invalid(self):
        """
        Test if the can_get_free_drink method returns False for invalid time strings.
        Tested with the config string that disallows free drinks on freezed time
        """
        # fd_case1 -> Mon: 1200-1400 Tue: 0900-1100 Fri: 0000-2400
        with freeze_time("2023-03-21 12:30"):  # Tuesday, 12:30 AM
            self.assertFalse(self.fd_case1.can_get_free_drink())

        with freeze_time("2023-03-25 00:00"):  # Friday, 24:00 AM -> Saturday, 00:00 AM
            self.assertFalse(self.fd_case1.can_get_free_drink())

        # fd_case2 -> Mon: 1200-1400 Tue: 0900-1100 Fri: 2200-2400 Fri: 2000-2200
        with freeze_time("2023-03-21 12:30"):  # Tuesday, 12:30 AM
            self.assertFalse(self.fd_case2.can_get_free_drink())

        with freeze_time("2023-03-25 22:00"):  # Friday, 22:00 AM
            self.assertFalse(self.fd_case2.can_get_free_drink())


if __name__ == "__main__":
    unittest.main()
