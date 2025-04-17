"""Module for tracking users, habits, and households in a habit tracking application.
This module provides the Tracker class which manages user, habit, and household tracking.
"""
import json
import logging

logging.basicConfig(level=logging.INFO)

class Tracker:
    """A class for tracking users, habits, and households in a habit tracking application.
    This class provides methods for adding users, habits, and households to the database.
    """
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.data = self.get_data()

    def get_data(self):
        """Load data from JSON file or initialize default structure."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"Data file '{self.filename}' not found or corrupt.")
            return {"users": [], "habits": [], "households": []}

    def save_data(self):
        """Save data to JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def add_user(self, user):
        """Add a user to the database."""
        self.data['users'].append(user.to_dict())
        self.save_data()

    def add_habit(self, habit):
        """Add a habit to the database."""
        self.data['habits'].append(habit.to_dict())
        self.save_data()

    def add_household(self, household):
        """Add a household to the database."""
        self.data['households'].append(household.to_dict())
        self.save_data()
