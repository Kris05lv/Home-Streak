"""Module for analytics in a habit tracking application.
This module provides the Analytics class which provides methods for analytics in a habit tracking application.
It includes functionality for getting all users, all habits, filtering by periodicity, finding the habit with the longest streak, and getting detailed statistics for a given habit."""
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Analytics:
    """A class providing analytics for a habit tracking application.
    This class provides methods for getting all users, all habits, filtering by periodicity, 
    finding the habit with the longest streak, and getting detailed statistics for a given 
    habit.
    """
    @staticmethod
    def get_all_users(tracker):
        """
        Get a list of all users in the tracker.
        """
        return tracker.data.get('users', [])    
    @staticmethod
    def all_habits(tracker):
        """
        Get a list of all habits in the tracker.
        """
        return tracker.data.get('habits', [])   
    @staticmethod
    def filter_by_periodicity(tracker, periodicity):
        """
        Filter habits based on the periodicity (daily/weekly).
        """
        return [habit for habit in tracker.data.get('habits', []) if habit.get('periodicity') == periodicity]    
    @staticmethod
    def longest_streak(tracker):
        """
        Find the habit with the longest streak.
        """
        habits = tracker.data.get('habits', [])
        return max(habits, key=lambda h: h.get('streak', 0), default=None)

    @staticmethod
    def longest_streak_for_habit(tracker, habit_name):
        """
        Get the longest streak for a specific habit.
        """
        habit = next((habit for habit in tracker.data.get('habits', []) if habit.get('name') == habit_name), None)
        if habit:
            return habit.get('streak', 0)
        return 0
    
    @staticmethod
    def habits_completed_by_user(tracker, username):
        """
        Get a list of habits completed by a specific user.
        """
        completed_habits = []
        for habit in tracker.data.get('habits', []):
            if 'completions' in habit and username in habit['completions']:
                completed_habits.append(habit['name'])
        return completed_habits

    @staticmethod
    def habit_statistics(tracker, habit_name):
        """
        Get detailed statistics for a given habit.
        """
        habit = next((habit for habit in tracker.data.get('habits', []) if habit.get('name') == habit_name), None)
        if habit:
            return {
                'name': habit['name'],
                'periodicity': habit['periodicity'],
                'completions': habit.get('completions', []),
                'streak': habit.get('streak', 0),
                'bonus_points': habit.get('bonus_points', 0)
            }
        return None
