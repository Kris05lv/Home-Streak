"""Module for managing leaderboards in a habit tracking application."""
from datetime import datetime
import logging
import json
from services.data_store import load_data, save_data

DATA_FILE = "data.json"

class Leaderboard:
    """A class for managing user rankings and leaderboards."""

    def __init__(self):
        """Initialize a new Leaderboard instance."""
        self.data = self.load_data()
        if "leaderboard" not in self.data:
            self.data["leaderboard"] = {
                "rankings": {},
                "past_rankings": []
            }
        self.rankings = self.data["leaderboard"]["rankings"]
        self.past_rankings = self.data["leaderboard"]["past_rankings"]
        self.top_performers = {}  # Required by test_initialization

    @staticmethod
    def load_data():
        """Load data from the data store."""
        try:
            data = load_data()
            if "leaderboard" not in data:
                data["leaderboard"] = {
                    "rankings": {},
                    "past_rankings": []
                }
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning("Error loading data.json: %s", e)
            return {
                "households": {},
                "habits": [],
                "leaderboard": {
                    "rankings": {},
                    "past_rankings": [],
                    "streaks": {},
                }
            }

    def save_data(self):
        """Save the current state to the data store."""
        save_data(self.data)

    @staticmethod
    def update(user: 'User'):
        """Update the leaderboard with a user's points."""
        data = load_data()
        if "leaderboard" not in data:
            data["leaderboard"] = {"rankings": {}, "past_rankings": []}
        
        if user.household not in data["leaderboard"]["rankings"]:
            data["leaderboard"]["rankings"][user.household] = {}
        
        # Update user points
        data["leaderboard"]["rankings"][user.household][user.username] = user.points
        
        # Sort rankings immediately after update
        rankings = data["leaderboard"]["rankings"][user.household]
        sorted_rankings = dict(sorted(
            rankings.items(),
            key=lambda item: item[1],
            reverse=True
        ))
        data["leaderboard"]["rankings"][user.household] = sorted_rankings
        save_data(data)

    def get_sorted_rankings(self, household_name):
        """Returns sorted rankings for a household."""
        data = self.load_data()
        if household_name not in data["leaderboard"]["rankings"]:
            data["leaderboard"]["rankings"][household_name] = {}
        
        rankings = data["leaderboard"]["rankings"][household_name]
        if not rankings:
            logging.warning("No rankings found for household '%s'." % household_name)
            return {}
        
        sorted_rankings = dict(sorted(
            rankings.items(),
            key=lambda item: item[1],
            reverse=True
        ))
        return sorted_rankings

    def get_top_performers(self):
        """Returns the top user for each month with their score."""
        if not self.past_rankings:
            return []
        return [ranking for ranking in self.past_rankings if "top_user" in ranking]

    def get_past_rankings(self):
        """Returns the list of past monthly rankings."""
        if not self.past_rankings:
            return []
        return [ranking for ranking in self.past_rankings if "rankings" in ranking]

    def reset_monthly(self):
        """Resets rankings at the end of each month, storing past rankings."""
        now = datetime.now().strftime('%m-%Y')
        
        # Store current rankings in past_rankings
        current_rankings = {}
        data = self.load_data()
        
        for household, rankings in data["leaderboard"]["rankings"].items():
            if rankings:  # Only store households with actual rankings
                current_rankings[household] = dict(sorted(
                    rankings.items(),
                    key=lambda item: item[1],
                    reverse=True
                ))

        if current_rankings:  # Only append if there are actual rankings
            # Store rankings with top performer in a single entry
            top_user, top_points = None, 0
            for household, rankings in current_rankings.items():
                for username, points in rankings.items():
                    if points > top_points:
                        top_user = username
                        top_points = points

            ranking_entry = {
                "month": now,
                "rankings": current_rankings,
                "top_user": top_user,
                "points": top_points
            }
            
            data["leaderboard"]["past_rankings"].append(ranking_entry)
            self.past_rankings.append(ranking_entry)

        # Clear current rankings
        data["leaderboard"]["rankings"] = {}
        self.rankings = {}
        save_data(data)
