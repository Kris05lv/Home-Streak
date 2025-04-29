"""Module for managing data in a habit tracking application.
This module provides the DataManager class which manages data persistence 
in a habit tracking application.
It includes functionality for loading and saving data, creating households, 
adding users, and managing habits."""
import logging
import json
from datetime import datetime, timedelta
from services.leaderboard import Leaderboard
from classes.user import User
import os

logging.basicConfig(level=logging.INFO)

leaderboard = Leaderboard()

class DataManager:
    """A class managing data persistence in a habit tracking application.
    This class provides methods for loading and saving data, creating households, 
    adding users, and managing habits.
    """
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")

    @staticmethod
    def load_data():
        """Load data from JSON file."""
        try:
            with open(DataManager.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "households": {},
                "habits": [],
                "bonus_habits": [],
                "user_data": {},
                "leaderboard": {
                    "rankings": {},
                    "past_rankings": [],
                    "top_performers": []
                }
            }
            DataManager.save_data(data)
        return data

    @staticmethod
    def save_data(data):
        """Save data to JSON file."""
        def date_handler(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        with open(DataManager.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=date_handler)

    @staticmethod
    def create_household(household_name):
        """Creates a new household if it doesn't already exist."""
        data = DataManager.load_data()
        if household_name in data["households"]:
            logging.warning("Household '%s' already exists.", household_name)
            return
        data["households"][household_name] = {"members": [], "points": {}}
        # Initialize leaderboard rankings for the new household
        data["leaderboard"]["rankings"][household_name] = {}
        DataManager.save_data(data)

    @staticmethod
    def save_user(user):
        """Adds a user to an existing household."""
        data = DataManager.load_data()
        
        # Convert household to string if it's not already
        household_name = str(user.household)
        
        if household_name not in data["households"]:
            msg = f"Household '{household_name}' does not exist"
            logging.error("Household '%s' does not exist. Please create it first.", household_name)
            raise ValueError(msg)

        # Initialize or update user data in household
        if user.username not in data["households"][household_name]["members"]:
            data["households"][household_name]["members"].append(user.username)
            data["households"][household_name]["points"][user.username] = user.points

        # Initialize or update user data
        if "user_data" not in data:
            data["user_data"] = {}

        data["user_data"][user.username] = {
            "household": household_name,
            "points": user.points,
            "habits_completed": user.habits_completed,
            "streaks": user.streaks,
            "bonus_claimed": user.bonus_claimed
        }

        # Initialize leaderboard data for the user
        if household_name not in data["leaderboard"]["rankings"]:
            data["leaderboard"]["rankings"][household_name] = {}
        data["leaderboard"]["rankings"][household_name][user.username] = user.points

        DataManager.save_data(data)

    @staticmethod
    def save_habit(habit):
        """Saves a new habit (regular or bonus) to the database."""
        data = DataManager.load_data()
        habit_list = data["bonus_habits"] if habit.is_bonus else data["habits"]
        if not any(h["name"] == habit.name for h in habit_list):
            habit_list.append(habit.to_dict())
            DataManager.save_data(data)

    @staticmethod
    def save_bonus_habit(habit):
        """Saves a bonus habit to the database."""
        data = DataManager.load_data()
        if not any(h["name"] == habit.name for h in data["bonus_habits"]):
            habit.is_bonus = True
            data["bonus_habits"].append(habit.to_dict())
            DataManager.save_data(data)

    @staticmethod
    def complete_habit(username, habit_name):
        """Complete a habit for a user."""
        data = DataManager.load_data()
        
        # Get user data
        user = DataManager.get_user(username)
        if not user:
            logging.error("User '%s' not found in any household.", username)
            return False

        # First check if it's a bonus habit
        bonus_habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        if bonus_habit:
            return DataManager.claim_bonus_habit(username, habit_name)

        # Get regular habit data
        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.error("Habit '%s' not found.", habit_name)
            return False

        # Get current date for tracking
        current_date = datetime.now().date()

        # Check if habit is already completed for today
        if user.has_completed_today(habit_name):
            logging.warning(
                "Habit '%s' already completed by user '%s' today.",
                habit_name,
                username
            )
            return False

        # Track habit completion
        user.track_completion(habit_name, current_date, habit["periodicity"], habit["points"])

        # Save user state
        DataManager.save_user(user)

        # Update leaderboard
        DataManager.update_leaderboard(user)

        return True

    @staticmethod
    def claim_bonus_habit(username, habit_name):
        """Claim a bonus habit (only once per period)."""
        data = DataManager.load_data()
        
        # Get user data
        user = DataManager.get_user(username)
        if not user:
            logging.error("User '%s' not found in any household.", username)
            return False

        # Get bonus habit data
        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.error("Bonus habit '%s' not found.", habit_name)
            return False

        # Get current date for tracking
        current_date = datetime.now().date()

        # Check if habit is already completed for today
        if user.has_completed_today(habit_name):
            logging.warning(
                "Bonus habit '%s' already claimed by user '%s' today.",
                habit_name,
                username
            )
            return False

        # Track bonus habit completion
        user.track_completion(habit_name, current_date, habit["periodicity"], habit["points"])

        # Save user state
        DataManager.save_user(user)

        # Update leaderboard
        DataManager.update_leaderboard(user)

        return True

    @staticmethod
    def reset_monthly_scores():
        """Resets user scores at the beginning of each month."""
        data = DataManager.load_data()
        for household in data["households"].values():
            for username in household["points"]:
                household["points"][username] = 0
        DataManager.save_data(data)

    @staticmethod
    def load_habits():
        """Loads all habits (regular and bonus)."""
        data = DataManager.load_data()
        return data["habits"] + data["bonus_habits"]

    @staticmethod
    def get_habit(habit_name):
        """Get a habit's data from the data store."""
        data = DataManager.load_data()
        return next((h for h in data["habits"] if h["name"] == habit_name), None)

    @staticmethod
    def reset_habits():
        """Reset all habits and streaks."""
        data = DataManager.load_data()
        data["completed_habits"] = {}
        data["streaks"] = {}
        DataManager.save_data(data)

    @staticmethod
    def clear_data():
        """Clear all data."""
        data = {
            "households": {},
            "habits": [],
            "bonus_habits": [],
            "leaderboard": {"rankings": {}, "past_rankings": []},
            "streaks": {},
            "completed_habits": {},
            "user_data": {}
        }
        DataManager.save_data(data)

    @staticmethod
    def get_user(username):
        """Get a user by username."""
        data = DataManager.load_data()
        
        # Check if user exists in user_data
        if "user_data" not in data or username not in data["user_data"]:
            logging.error("User '%s' not found in any household.", username)
            return None

        # Get user data
        user_data = data["user_data"][username]
        household = user_data["household"]

        # Create user object
        user = User(username, household, user_data["points"])
        user.habits_completed = user_data.get("habits_completed", {})
        user.streaks = user_data.get("streaks", {})
        user.bonus_claimed = user_data.get("bonus_claimed", {})

        return user

    @staticmethod
    def load_users():
        """Load all users from the data store."""
        data = DataManager.load_data()
        users = []
        for household_name, household_data in data["households"].items():
            for username in household_data["members"]:
                points = household_data["points"].get(username, 0)
                users.append({
                    "username": username, 
                    "household": household_name, 
                    "points": points
                })
        return users

    @staticmethod
    def get_user_completion_history(username):
        """Get the completion history for a specific user."""
        data = DataManager.load_data()
        if "completed_habits" not in data:
            return []

        history = []
        for date, completions in data["completed_habits"].items():
            completed_count = sum(1 for habit_name, user in completions.items() if user == username)
            if completed_count > 0:
                history.append({"date": date, "completed_habits": completed_count})
        return history

    @staticmethod
    def get_user_streaks(username):
        """Get the streak history for a specific user."""
        data = DataManager.load_data()
        if "streaks" not in data or username not in data["streaks"]:
            return []

        streaks = []
        for habit_name, streak_data in data["streaks"][username].items():
            if streak_data > 0:
                streaks.append({
                    "habit_name": habit_name,
                    "streak_length": streak_data,
                    "start_date": datetime.now().strftime("%Y-%m-%d")
                })
        return streaks

    @staticmethod
    def get_user_habit_bonus(username):
        """Get the bonus habit history for a specific user."""
        data = DataManager.load_data()
        if "completed_habits" not in data:
            return []

        bonus_history = []
        for date, completions in data["completed_habits"].items():
            bonus_points = 0
            for habit_name, user in completions.items():
                if user == username:
                    habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
                    if habit:
                        bonus_points += habit["points"]
            if bonus_points > 0:
                bonus_history.append({"date": date, "habit_bonus": bonus_points})
        return bonus_history

    @staticmethod
    def update_leaderboard(user):
        """Update the leaderboard with a user's points."""
        data = DataManager.load_data()
        if user.household not in data["households"]:
            logging.error("Household '%s' not found.", user.household)
            return

        if "points" not in data["households"][user.household]:
            data["households"][user.household]["points"] = {}

        data["households"][user.household]["points"][user.username] = user.points
        DataManager.save_data(data)

    @staticmethod
    def get_sorted_rankings(household_name):
        """Get sorted rankings for a household."""
        return leaderboard.get_sorted_rankings(household_name)

    @staticmethod
    def get_top_performers():
        """Get top performers from past months."""
        return leaderboard.get_top_performers()

    @staticmethod
    def get_past_rankings():
        """Get past leaderboard rankings."""
        return leaderboard.get_past_rankings()

    @staticmethod
    def reset_monthly():
        """Reset monthly scores and archive rankings."""
        leaderboard.reset_monthly()

# Create a singleton instance of DataManager
data_manager = DataManager()