"""Module for managing habits in a habit tracking application.

This module provides the Habit class which represents individual habits that users can complete
    to earn points. It includes functionality for habit completion, point calculation, and data
    persistence through dictionary conversion."""
import logging
from datetime import datetime
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Habit:
    """A class representing a habit that users can complete to earn points.

    This class manages habits, their completion status, and associated point calculations."""

    def __init__(self, name: str, periodicity: str, points: int, is_bonus: bool = False) -> None:
        """Initialize a new Habit.

        Args:
            name (str): The name of the habit.
            periodicity (str): How often the habit can be completed (e.g., 'daily', 'weekly').
            points (int): Base points awarded for completing the habit.
            is_bonus (bool, optional): Whether this is a bonus habit. Defaults to False.

        Raises:
            ValueError: If name is empty, points is negative, or periodicity is invalid.
        """
        if not name or not name.strip():
            raise ValueError("Habit name cannot be empty")
        if points < 0:
            raise ValueError("Points cannot be negative")
        if periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be either 'daily' or 'weekly'")

        self.name = name.strip()
        self.periodicity = periodicity
        self.created_at = datetime.now().isoformat()
        self.points = points
        self.is_bonus = is_bonus

    def complete(self, user: 'User') -> str:
        """Complete a habit for the given user.

        Args:
            user: The user completing the habit.

        Returns:
            str: A message indicating the result of the completion attempt,
                including points earned or why the completion was not allowed.
        """
        today = datetime.now().date()

        if user.has_completed_today(self.name):
            return f"Oops! {self.name} has already been completed today."

        if self.is_bonus:
            current_week = today.strftime('%W-%Y')
            if user.bonus_claimed.get(self.name) == current_week:
                return f"Oops! {self.name} has already been claimed this week."
            user.bonus_claimed[self.name] = current_week

        user.track_completion(self.name, today, self.periodicity)
        points_earned = self.calculate_points(user)
        user.points += points_earned

        return f"Good job, {user.username}! You completed '{self.name}' and earned {points_earned} points."

    def calculate_points(self, user: 'User') -> int:
        """Calculate the total points to be awarded for completing this habit.

        Args:
            user: The user completing the habit.

        Returns:
            int: Total points to be awarded, including any bonus points.
        """
        total_points = self.points
        if user.streaks.get(self.name, 0) % 7 == 0:
            total_points += 5  # Add streak bonus
        return total_points

    def to_dict(self) -> Dict[str, Any]:
        """Convert the habit object to a dictionary representation.

        Returns:
            dict: Dictionary containing all habit attributes.
        """
        return {
            'name': self.name,
            'periodicity': self.periodicity,
            'created_at': self.created_at,
            'points': self.points,
            'is_bonus': self.is_bonus
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Habit':
        """Create a Habit instance from a dictionary.

        Args:
            data (dict): Dictionary containing habit attributes.

        Returns:
            Habit: A new Habit instance with the specified attributes.
        """
        return cls(data["name"], data["periodicity"], data["points"], data["is_bonus"])