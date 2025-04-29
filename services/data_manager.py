"""Module for managing data in a habit tracking application.
This module provides the DataManager class which manages data persistence 
in a habit tracking application.
It includes functionality for loading and saving data, creating households, 
adding users, and managing habits."""
import logging
from datetime import datetime, timedelta
from services.data_store import load_data, save_data
from services.leaderboard import Leaderboard
from classes.user import User

logging.basicConfig(level=logging.INFO)

leaderboard = Leaderboard()

class DataManager:
    """A class managing data persistence in a habit tracking application.
    This class provides methods for loading and saving data, creating households, 
    adding users, and managing habits.
    """
    @staticmethod
    def load_data():
        """Load data from the data.json file."""
        try:
            data = load_data()
            # Initialize data structure if empty
            if not data:
                data = {
                    "households": {},
                    "habits": [],
                    "bonus_habits": [],
                    "leaderboard": {"rankings": {}, "past_rankings": []},
                    "streaks": {},
                    "completed_habits": {}
                }
                save_data(data)
            # Ensure all required keys exist
            required_keys = [
                "households", "habits", "bonus_habits", 
                "leaderboard", "streaks", "completed_habits"
            ]
            for key in required_keys:
                if key not in data:
                    data[key] = [] if key in ["habits", "bonus_habits"] else {}
            if "leaderboard" in data and isinstance(data["leaderboard"], dict):
                if "rankings" not in data["leaderboard"]:
                    data["leaderboard"]["rankings"] = {}
                if "past_rankings" not in data["leaderboard"]:
                    data["leaderboard"]["past_rankings"] = []
            else:
                data["leaderboard"] = {"rankings": {}, "past_rankings": []}
            return data
        except FileNotFoundError:
            logging.info("No data.json found. Creating new data structure.")
            data = {
                "households": {},
                "habits": [],
                "bonus_habits": [],
                "leaderboard": {"rankings": {}, "past_rankings": []},
                "streaks": {},
                "completed_habits": {}
            }
            save_data(data)
            return data

    @staticmethod
    def save_data(data):
        """Saves data to JSON file."""
        save_data(data)

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
        if user.household not in data["households"]:
            msg = f"Household '{user.household}' does not exist"
            logging.error("Household '%s' does not exist. Please create it first.", user.household)
            raise ValueError(msg)
        if user.username in data["households"][user.household]["members"]:
            logging.warning("User '%s' is already in household '%s'.", user.username, user.household)
            return
        data["households"][user.household]["members"].append(user.username)
        data["households"][user.household]["points"][user.username] = user.points
        # Initialize user's streaks and completed habits
        data["streaks"][user.username] = {}
        if "completed_habits" not in data:
            data["completed_habits"] = {}
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
        """Marks a habit as completed, tracks streaks, updates points, and leaderboard."""
        data = DataManager.load_data()
        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.error("Habit '%s' not found.", habit_name)
            return False

        # Find user's household
        user_household = None
        for household, details in data["households"].items():
            if username in details["members"]:
                user_household = household
                break

        if not user_household:
            logging.error("User '%s' not found in any household.", username)
            return False

        # Initialize streak tracking for the user if needed
        if username not in data["streaks"]:
            data["streaks"][username] = {}
        if habit_name not in data["streaks"][username]:
            data["streaks"][username][habit_name] = 0

        # Update streak and points
        data["streaks"][username][habit_name] += 1
        data["households"][user_household]["points"][username] += habit["points"]

        # Record completion
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in data["completed_habits"]:
            data["completed_habits"][today] = {}
        data["completed_habits"][today][habit_name] = username

        # Update leaderboard
        user = User(username, user_household, points=data["households"][user_household]["points"][username])
        DataManager.update_leaderboard(user)

        DataManager.save_data(data)
        return True

    @staticmethod
    def claim_bonus_habit(username, habit_name):
        """Claim a bonus habit (only once per period)."""
        data = DataManager.load_data()
        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.error("Bonus habit '%s' not found.", habit_name)
            return False

        # Find user's household
        user_household = None
        for household, details in data["households"].items():
            if username in details["members"]:
                user_household = household
                break

        if not user_household:
            logging.error("User '%s' not found in any household.", username)
            return False

        # Check if the habit has already been claimed in the current period
        today = datetime.now()
        period_start = today - timedelta(days=today.weekday() if habit["periodicity"] == "weekly" else 0)
        period_start = period_start.strftime("%Y-%m-%d")

        # Check if already claimed in this period
        for date, completions in data["completed_habits"].items():
            if date >= period_start and habit_name in completions and completions[habit_name] == username:
                logging.warning("User '%s' has already claimed bonus habit '%s' this period.", 
                              username, habit_name)
                return False

        # Record completion and update points
        today_str = today.strftime("%Y-%m-%d")
        if today_str not in data["completed_habits"]:
            data["completed_habits"][today_str] = {}
        data["completed_habits"][today_str][habit_name] = username
        data["households"][user_household]["points"][username] += habit["points"]

        # Update leaderboard
        user = User(username, user_household, 
                   points=data["households"][user_household]["points"][username])
        DataManager.update_leaderboard(user)

        DataManager.save_data(data)
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
        """Fetch a single habit from stored data."""
        data = DataManager.load_data()
        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if habit:
            return habit
        return next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)

    @staticmethod
    def reset_habits():
        """Reset habits based on their periodicity (daily/weekly)."""
        data = DataManager.load_data()
        today = datetime.now()

        # Reset streaks for habits that haven't been completed in their period
        for username, user_streaks in data["streaks"].items():
            for habit_name, streak in user_streaks.items():
                habit = DataManager.get_habit(habit_name)
                if not habit:
                    continue

                # Determine period start based on habit periodicity
                days_to_subtract = today.weekday() if habit["periodicity"] == "weekly" else 0
                period_start = (today - timedelta(days=days_to_subtract)).strftime("%Y-%m-%d")

                # Check if habit was completed in current period
                completed_in_period = False
                for date, completions in data["completed_habits"].items():
                    if (date >= period_start and 
                            habit_name in completions and 
                            completions[habit_name] == username):
                        completed_in_period = True
                        break

                if not completed_in_period:
                    data["streaks"][username][habit_name] = 0

        DataManager.save_data(data)

    @staticmethod
    def clear_data():
        """Clears the contents of the data.json file."""
        data = {
            "households": {},
            "habits": [],
            "bonus_habits": [],
            "leaderboard": {"rankings": {}, "past_rankings": []},
            "streaks": {},
            "completed_habits": {}
        }
        try:
            save_data(data)
            # Reset leaderboard state
            leaderboard.reset_state()
            logging.info("data.json has been cleared successfully.")
        except IOError as e:
            logging.error("Failed to clear data.json: %s", str(e))
            raise

    @staticmethod
    def get_user(username):
        """Get a user's data from the data store."""
        data = DataManager.load_data()
        for household_name, household_data in data["households"].items():
            if username in household_data["members"]:
                points = household_data["points"].get(username, 0)
                return User(username, household_name, points=points)
        return None

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
        leaderboard.update(user)

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