"""Module for managing users in a habit tracking application.
This module provides the User class which represents individual users in 
a habit tracking application.
It includes functionality for user management, habit tracking, and data 
persistence through dictionary conversion."""
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class User:
    """A class representing a user in a habit tracking application."""
    def __init__(self, username, household, points=0):
        """Initialize a new User instance.

        Args:
            username (str): The username of the user
            household (Household): The household the user belongs to
            points (int, optional): Initial points for the user. Defaults to 0
        """
        self.username = username
        self.household = household
        self.habits_completed = {}
        self.streaks = {}
        self.bonus_claimed = {}
        self.points = points

    def has_completed_today(self, habit_name):
        """Check if a habit has been completed today.

        Args:
            habit_name: The name of the habit to check.

        Returns:
            bool: True if the habit has been completed today, False otherwise.
        """
        today = datetime.now().date()
        return habit_name in self.habits_completed and self.habits_completed[habit_name][-1] == today

    def track_completion(self, habit_name, date, periodicity, points=None):
        """Track the completion of a habit on a specific date.

        Args:
            habit_name (str): The name of the habit completed
            date (datetime.date): The date of completion
            periodicity (str): The frequency of the habit ('daily' or 'weekly')
            points (int, optional): Points to award for completion. Defaults to None.
        """
        if habit_name not in self.habits_completed:
            self.habits_completed[habit_name] = []
            self.streaks[habit_name] = 0

        self.habits_completed[habit_name].append(date)
        self.update_streak(habit_name, periodicity)
        if points is not None:
            self.points += points

    def update_streak(self, habit_name, periodicity):
        """Update the streak count for a habit.

        Args:
            habit_name (str): The name of the habit
            periodicity (str): The frequency of the habit ('daily' or 'weekly')
        """
        completions = self.habits_completed[habit_name]
        if len(completions) < 2:
            self.streaks[habit_name] = 1
            return

        streak = 1
        for i in range(1, len(completions)):
            delta = (completions[i] - completions[i - 1]).days
            if (periodicity == 'daily' and delta == 1) or (periodicity == 'weekly' and delta == 7):
                streak += 1
            else:
                streak = 1

        self.streaks[habit_name] = streak
        if streak % 7 == 0:
            self.points += 5  # Add streak bonus

    def get_bonus_points(self, habit_name):
        """Calculate bonus points for a habit streak.

        Args:
            habit_name (str): The name of the habit

        Returns:
            int: 5 points if the streak is a multiple of 7, 0 otherwise
        """
        if habit_name not in self.streaks:
            return 0
        return 5 if self.streaks[habit_name] % 7 == 0 else 0

    def add_points(self, points):
        """Add points to the user's total.

        Args:
            points (int): Number of points to add
        """
        self.points += points

    def to_dict(self):
        """Convert the User object to a dictionary representation.

        Returns:
            dict: A dictionary containing the user's data
        """
        return {
            'username': self.username,
            'household': self.household.name if hasattr(self.household, 'name') else str(self.household),
            'habits_completed': {
                habit: [date.strftime("%Y-%m-%d") for date in dates]
                for habit, dates in self.habits_completed.items()
            },
            'streaks': self.streaks,
            'bonus_claimed': self.bonus_claimed,
            'points': self.points
        }

    @classmethod
    def from_dict(cls, data, household=None):
        """Create a User instance from a dictionary.

        Args:
            data (dict): Dictionary containing user data
            household (Household, optional): The household object. Required for new users.

        Returns:
            User: A new User instance with the data from the dictionary

        Raises:
            KeyError: If required data fields are missing from the dictionary
            ValueError: If data is not a dictionary or if points is negative
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        if "username" not in data:
            raise KeyError("Username is required")

        points = data.get("points", 0)
        if not isinstance(points, (int, float)) or points < 0:
            raise ValueError("Points must be a non-negative number")

        user = cls(data["username"], household, points)
        user.habits_completed = {
            habit: [datetime.strptime(date, "%Y-%m-%d").date() for date in dates]
            for habit, dates in data.get("habits_completed", {}).items()
        }
        user.streaks = data.get("streaks", {})
        user.bonus_claimed = data.get("bonus_claimed", {})
        user.points = points

        # Validate the created user object
        if not isinstance(user.streaks, dict):
            raise ValueError("Streaks must be a dictionary")
        if not isinstance(user.bonus_claimed, dict):
            raise ValueError("Bonus claimed must be a dictionary")
        if not isinstance(user.habits_completed, dict):
            raise ValueError("Habits completed must be a dictionary")

        return user