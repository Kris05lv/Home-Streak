"""Module for testing user functionality.
This module provides test cases for user functionality.
"""
import pytest
from datetime import datetime, timedelta
from classes.user import User
from classes.household import Household # noqa: F401
from classes.habit import Habit  # noqa: F401 - Used in pytest fixtures

@pytest.fixture
def household():
    """Create a test household."""
    return Household("Test Household")

@pytest.fixture
def user(household):
    """Create a test user."""
    return User("test_user", household)

@pytest.fixture
def habit():
    """Create a test habit."""
    return Habit("Exercise", "daily", 5)

def test_user_initialization():
    """Test user initialization with valid parameters."""
    test_household = Household("Test Household")
    user = User("test_user", test_household, points=10)
    assert user.username == "test_user"
    assert user.household == test_household
    assert user.points == 10
    assert isinstance(user.habits_completed, dict)
    assert isinstance(user.streaks, dict)
    assert isinstance(user.bonus_claimed, dict)

def test_has_completed_today(user, habit):
    """Test checking if a habit has been completed today."""
    assert not user.has_completed_today(habit.name)
    
    # Add a completion for today
    today = datetime.now().date()
    user.track_completion(habit.name, today, habit.periodicity, habit.points)
    assert user.has_completed_today(habit.name)

def test_track_completion(user, habit):
    """Test tracking habit completion."""
    today = datetime.now().date()
    user.track_completion(habit.name, today, habit.periodicity, habit.points)
    
    assert habit.name in user.habits_completed
    assert len(user.habits_completed[habit.name]) == 1
    assert user.habits_completed[habit.name][0] == today
    assert user.streaks[habit.name] == 1
    assert user.points == habit.points

def test_update_streak_daily(user, habit):
    """Test updating streak for daily habit."""
    today = datetime.now().date()
    
    # Complete habit for 3 consecutive days
    for i in range(3):
        date = today - timedelta(days=2-i)
        user.track_completion(habit.name, date, "daily", habit.points)
    
    assert user.streaks[habit.name] == 3
    assert user.points == habit.points * 3

def test_update_streak_weekly(user):
    """Test updating streak for weekly habit."""
    weekly_habit = Habit("Weekly Exercise", "weekly", 10)
    today = datetime.now().date()
    
    # Complete habit for 3 consecutive weeks
    for i in range(3):
        date = today - timedelta(weeks=2-i)
        user.track_completion(weekly_habit.name, date, "weekly", weekly_habit.points)
    
    assert user.streaks[weekly_habit.name] == 3
    assert user.points == weekly_habit.points * 3

def test_streak_reset(user, habit):
    """Test streak reset when completion chain breaks."""
    today = datetime.now().date()
    
    # Complete habit for 3 days, skip one, then complete again
    dates = [
        today - timedelta(days=4),
        today - timedelta(days=3),
        today - timedelta(days=2),
        today  # Skip day 1
    ]
    
    for date in dates:
        user.track_completion(habit.name, date, "daily", habit.points)
    
    assert user.streaks[habit.name] == 1  # Streak should reset after the gap
    assert user.points == habit.points * 4  # Points for 4 completions

def test_get_bonus_points(user, habit):
    """Test bonus points calculation for streaks."""
    today = datetime.now().date()
    
    # Complete habit for 7 consecutive days
    for i in range(7):
        date = today - timedelta(days=6-i)
        user.track_completion(habit.name, date, "daily", habit.points)
    
    assert user.get_bonus_points(habit.name) == 5  # Should get bonus on 7th day
    assert user.get_bonus_points("nonexistent_habit") == 0  # No bonus for non-existent habits
    assert user.points == (habit.points * 7) + 5  # Base points plus streak bonus

def test_to_dict(user, habit):
    """Test converting user to dictionary."""
    today = datetime.now().date()
    user.track_completion(habit.name, today, habit.periodicity, habit.points)
    
    user_dict = user.to_dict()
    assert isinstance(user_dict, dict)
    assert user_dict["username"] == user.username
    assert user_dict["household"] == user.household.name
    assert isinstance(user_dict["habits_completed"], dict)
    assert isinstance(user_dict["streaks"], dict)
    assert isinstance(user_dict["bonus_claimed"], dict)
    assert user_dict["points"] == user.points
    
    # Check habit completion date format
    habit_dates = user_dict["habits_completed"][habit.name]
    assert isinstance(habit_dates[0], str)
    assert datetime.strptime(habit_dates[0], "%Y-%m-%d").date() == today

def test_from_dict_valid():
    """Test creating user from valid dictionary."""
    household = Household("Test Household")
    user_data = {
        "username": "test_user",
        "points": 10,
        "habits_completed": {
            "Exercise": ["2025-04-15"]
        },
        "streaks": {"Exercise": 1},
        "bonus_claimed": {}
    }
    
    user = User.from_dict(user_data, household)
    assert user.username == "test_user"
    assert user.points == 10
    assert len(user.habits_completed["Exercise"]) == 1
    assert user.streaks["Exercise"] == 1

def test_from_dict_invalid():
    """Test creating user from invalid dictionary."""
    with pytest.raises(ValueError, match="Data must be a dictionary"):
        User.from_dict("not a dict", None)
    
    with pytest.raises(KeyError, match="Username is required"):
        User.from_dict({}, None)
    
    with pytest.raises(ValueError, match="Points must be a non-negative number"):
        User.from_dict({"username": "test", "points": -1}, None)

def test_streak_bonus_points(user, habit):
    """Test that streak bonuses add points correctly."""
    today = datetime.now().date()
    initial_points = user.points
    
    # Complete habit for 7 consecutive days
    for i in range(7):
        date = today - timedelta(days=6-i)
        user.track_completion(habit.name, date, "daily", habit.points)
    
    # Should have base points for each completion plus streak bonus
    assert user.points > initial_points + (7 * habit.points)
    # Verify the bonus was added (5 points for 7-day streak)
    assert user.points == initial_points + (7 * habit.points) + 5

def test_add_points(user):
    """Test adding points to user."""
    initial_points = user.points
    user.add_points(10)
    assert user.points == initial_points + 10
