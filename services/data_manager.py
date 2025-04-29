"""Module for managing data in a habit tracking application.
This module provides the DataManager class which manages data persistence 
in a habit tracking application.
It includes functionality for loading and saving data, creating households, 
adding users, and managing habits."""
import logging
from datetime import datetime
from services.data_store import load_data, save_data
from services.leaderboard import Leaderboard
from classes.user import User

logging.basicConfig(level=logging.INFO)

class DataManager:
    """A class managing data persistence in a habit tracking application.
    This class provides methods for loading and saving data, creating households, 
    adding users, and managing habits.
    """
    @staticmethod
    def load_data():
        """Loads data from JSON file or initializes default structure."""
        return load_data()

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
        if household_name not in data["leaderboard"]["rankings"]:
            data["leaderboard"]["rankings"][household_name] = {}
        DataManager.save_data(data)

    @staticmethod
    def save_user(user):
        """Adds a user to an existing household."""
        data = DataManager.load_data()
        if user.household not in data["households"]:
            logging.error("Household '%s' does not exist. Please create it first.", user.household)
            raise ValueError(f"Household '{user.household}' does not exist")
        if user.username in data["households"][user.household]["members"]:
            logging.warning("User '%s' is already in household '%s'.", user.username, user.household)
            return
        data["households"][user.household]["members"].append(user.username)
        data["households"][user.household]["points"][user.username] = 0  

        if user.username not in data["streaks"]:
            data["streaks"][user.username] = {}  

        DataManager.save_data(data)
       
    @staticmethod
    def save_habit(habit):
        """Saves a new habit (regular or bonus) to the database."""
        data = DataManager.load_data()
        habit_dict = habit.to_dict()

        if any(h["name"] == habit.name for h in data["habits"]):
            logging.warning("Habit '%s' already exists.", habit.name)
            return

        if habit.is_bonus:
            data["bonus_habits"].append(habit_dict)
        else:
            data["habits"].append(habit_dict)

        DataManager.save_data(data)

    @staticmethod
    def save_bonus_habit(habit):
        """Saves a bonus habit to the database."""
        data = DataManager.load_data()
        habit_dict = habit.to_dict()  
        if any(h["name"] == habit.name for h in data["bonus_habits"]):
            logging.warning("Bonus habit '%s' already exists.", habit.name)
            return
        data["bonus_habits"].append(habit_dict)  
        DataManager.save_data(data)

    @staticmethod
    def complete_habit(username, habit_name):
        """Marks a habit as completed, tracks streaks, updates points, and leaderboard."""
        data = DataManager.load_data()

        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.warning("Habit '%s' not found.", habit_name)
            return False

        # Find user's household
        household_name = None
        for household, details in data["households"].items():
            if username in details["members"]:
                household_name = household
                break

        if not household_name:
            logging.warning("User '%s' not found.", username)
            return False

        # Initialize streak if not exists
        if username not in data["streaks"]:
            data["streaks"][username] = {}
        if habit_name not in data["streaks"][username]:
            data["streaks"][username][habit_name] = 0

        # Check if habit can be completed based on periodicity
        last_completed = habit.get("last_completed_at")
        if last_completed:
            last_completed = datetime.strptime(last_completed, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            if habit["periodicity"] == "daily":
                if now.date() <= last_completed.date():
                    logging.warning("Daily habit '%s' already completed today.", habit_name)
                    return False
            elif habit["periodicity"] == "weekly":
                if (now - last_completed).days < 7:
                    logging.warning("Weekly habit '%s' already completed this week.", habit_name)
                    return False

        # Update streak and points
        if last_completed:
            time_diff = datetime.now() - last_completed
            if (habit["periodicity"] == "daily" and time_diff.days <= 1) or \
               (habit["periodicity"] == "weekly" and time_diff.days <= 7):
                data["streaks"][username][habit_name] += 1
            else:
                data["streaks"][username][habit_name] = 1
        else:
            data["streaks"][username][habit_name] = 1

        # Calculate points with streak bonus
        streak = data["streaks"][username][habit_name]
        streak_bonus = max(0, streak - 1)  # No bonus for streak of 1
        points = habit["points"] + streak_bonus

        # Update user points
        data["households"][household_name]["points"][username] += points

        # Update habit completion time
        habit["last_completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        DataManager.save_data(data)

        # Update leaderboard
        user = User(username, household_name, data["households"][household_name]["points"][username])
        Leaderboard().update(user)

        logging.info("Habit '%s' completed by %s. Streak: %d. Points earned: %d.", 
                    habit_name, username, data['streaks'][username][habit_name], points)
        return True

    @staticmethod
    def claim_bonus_habit(username, habit_name):
        """Claim a bonus habit (only once per period)."""
        data = DataManager.load_data()

        household_name = None
        for household, details in data["households"].items():
            if username in details["members"]:
                household_name = household
                break

        if not household_name:
            logging.warning("User '%s' not found.", username)
            return False

        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        if not habit or not habit.get("is_bonus", False):
            logging.warning("Habit '%s' is not a bonus habit.", habit_name)
            return False

        current_period = datetime.now().strftime("%Y-%m-%d") if habit["periodicity"] == "daily" else datetime.now().strftime("%Y-%W")

        if "completed_habits" not in data:
            data["completed_habits"] = {}
        if current_period not in data["completed_habits"]:
            data["completed_habits"][current_period] = {}

        if habit_name in data["completed_habits"][current_period]:
            logging.warning("Bonus habit '%s' has already been claimed this period.", habit_name)
            return False

        user_data = data["households"][household_name]["points"]
        user_data[username] += habit["points"]
    
        data["completed_habits"][current_period][habit_name] = username  
        DataManager.save_data(data)

        user = User(username, household_name, user_data[username])
        Leaderboard().update(user)

        logging.info("Bonus Habit '%s' claimed by %s. Points: %d.", habit_name, username, habit['points'])
        return True

    @staticmethod
    def reset_monthly_scores():
        """Resets user scores at the beginning of each month."""
        data = DataManager.load_data()
        for household in data["households"].values():
            for user in household["points"]:
                household["points"][user] = 0
        DataManager.save_data(data)

    @staticmethod
    def load_habits():
        """Loads all habits (regular and bonus)."""
        data = DataManager.load_data()
        return data.get("habits", []) + data.get("bonus_habits", [])
    
    @staticmethod
    def get_habit(habit_name):
        """Fetch a single habit from stored data."""
        data = DataManager.load_data()
    
        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if habit:
            return habit
    
        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        return habit

    @staticmethod
    def reset_habits():
        """Reset habits based on their periodicity (daily/weekly)."""
        data = DataManager.load_data()
        for habit in data["habits"] + data["bonus_habits"]:
            # Reset last_completed_at regardless of periodicity
            habit["last_completed_at"] = None
        DataManager.save_data(data)
        logging.info("All habits have been reset.")

    @staticmethod
    def clear_data():
        """Clears the contents of the data.json file."""
        data = {
            "households": {},
            "habits": [],
            "bonus_habits": [],
            "leaderboard": {"rankings": {}, "past_rankings": []}
        }
        try:
            save_data(data)
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
                users.append({"username": username, "household": household_name, "points": points})
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
            if streak_data["current_streak"] > 0:
                streaks.append({
                    "habit_name": habit_name,
                    "streak_length": streak_data["current_streak"],
                    "start_date": streak_data.get("streak_start_date", datetime.now().strftime("%Y-%m-%d"))
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

# Create a singleton instance of DataManager
data_manager = DataManager()