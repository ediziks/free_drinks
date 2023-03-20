from datetime import datetime, time
from typing import Tuple


class FreeDrinkEstimator:
    """
    A class to estimate free drinks promotion at vending machines.
    """

    def __init__(self, config_string: str):
        self.config_string = config_string

    def is_valid_config_string(self) -> bool:
        """
        Check if a config string is valid. Return false if the config string is empty or contains invalid day or time range.

        Returns:
            bool: True if the config string is valid, False otherwise.

        Example:
            # Assuming the config_string is "Mon: 0900-1100 Tue: 0900-1100 Fri: 0000-2400"
            >>> is_valid_config_string()
            True
            # Assuming the config_string is ""
            >>> is_valid_config_string()
            AssertionError: Invalid config_string
        """
        if (
            not self.config_string
            or self.config_string.isspace()
            or self.config_string == ""
        ):
            assert False, "Invalid config_string provided"
        else:
            return True

    def is_valid_day(self, day: str) -> bool:
        """
        Check if a day string is valid.

        Args:
            day (str): The day string to check.

        Returns:
            bool: True if the day string is valid, False otherwise.

        Example:
            >>> is_valid_day("Tue")
            True
            >>> is_valid_day("Tues")
            False
        """
        try:
            datetime.strptime(day, "%a")
            return True
        except ValueError:
            assert False, "Invalid day in config_string"

    def is_valid_time_range(self, time_range: str) -> bool:
        """
        Check if a time range string is valid.

        Args:
            time_range (str): The time range string to check.

        Returns:
            bool: True if the time range string is valid, False otherwise.

        Example:
            >>> is_valid_time_range("0900-1100")
            True
            >>> is_valid_time_range("1100-0900")
            False
        """
        try:
            start_time, end_time = self.parse_time_range(time_range)
            if start_time < end_time:
                return True
            else:
                assert False, "Invalid time range in config_string"
        except (ValueError, AttributeError):
            assert False, "Invalid time range in config_string"

    def parse_time_range(self, time_range: str) -> Tuple[time, time]:
        """
        Parse a time range string into start and end time objects.

        Args:
            time_range (str): The time range string to parse.

        Returns:
            Tuple[time, time]: A tuple of start and end time objects.

        Example:
            >>> parse_time_range("0900-1100")
            (datetime.time(9, 0), datetime.time(11, 0))
        """
        start_time_str, end_time_str = time_range.split("-")
        start_time = datetime.strptime(start_time_str, "%H%M").time()
        if end_time_str == "2400":
            end_time = time.max
        else:
            end_time = datetime.strptime(end_time_str, "%H%M").time()
        return start_time, end_time

    def parse_config_string(self) -> dict:
        """
        Parse a config string into a dictionary of valid time ranges keyed by days.

        Returns:
            dict: A dictionary of valid time ranges keyed by days and valued by list of time ranges.

        Example:
            >>> parse_config_string()
            {
                'mon': [(datetime.time(12, 0), datetime.time(14, 0))],
                'tue': [(datetime.time(9, 0), datetime.time(11, 0))],
                'fri': [(datetime.time(0, 0), datetime.time(23, 59, 59, 999999))]
            }
        """
        day_ranges = {}
        self.is_valid_config_string()
        config_string = self.config_string
        config_string_list = config_string.split()
        for i in range(0, len(config_string_list), 2):
            day = config_string_list[i].split(":")[0]
            time_range = config_string_list[i + 1]
            self.is_valid_time_range(time_range)
            self.is_valid_day(day)
            day = day.lower()[:3]
            if day not in day_ranges:
                day_ranges[day] = [self.parse_time_range(time_range)]
            else:
                day_ranges[day].append(self.parse_time_range(time_range))
        return day_ranges

    def can_get_free_drink(self) -> bool:
        """
        Check if the current time falls within a valid time range for the current day.

        Returns:
            bool: True if the current time falls within a valid time range for the current day

        Example:
            # Assuming the config_string is "Mon: 1200-1400 Tue: 0900-1100"
            >>> free_drinks = FreeDrinks(config_string)
            >>> free_drinks.can_get_free_drink()
            True # If the current day is Monday and the current time is 12:30 PM
            >>> free_drinks.can_get_free_drink()
            False # If the current day is Tuesday and the current time is 12:30 PM
        """
        day_ranges = self.parse_config_string()
        current_datetime = datetime.now()
        current_day = current_datetime.strftime("%a").lower()[:3]
        current_time = current_datetime.time()
        if current_day in day_ranges:
            for day_range in day_ranges[current_day]:
                start_time, end_time = day_range
                if end_time == time.max:
                    if start_time <= current_time <= end_time:
                        return True
                else:
                    if start_time <= current_time < end_time:
                        return True
        return False


if __name__ == "__main__":
    with open("free_drinks/config", "r") as f:
        config_string = f.read().strip()
    free_drinks = FreeDrinkEstimator(config_string)
    result = free_drinks.can_get_free_drink()
    if result:
        print("Free drink time!")
    else:
        print("Sorry, no free drinks for now but you can still buy one!")
