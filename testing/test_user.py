"""Module for testing user functionality.
This module provides test cases for user functionality.
"""

from datetime import datetime, timedelta

import pytest

from classes.habit import Habit
from classes.household import Household
from classes.user import User

@pytest.fixture
def mock_household():
    """Create a test household."""
    return Household("Test Household")

@pytest.fixture
def mock_user(mock_household):
    """Create a test user."""
    return User("test_user", mock_household)

@pytest.fixture
def mock_habit():
    """Create a test habit."""
    return Habit("Exercise", "daily", 5)

def test_user_initialization():
    """Test user initialization with valid parameters."""
    test_household_name = "Test Household"
    test_username = "test_user"
    test_points = 10
    
    new_household = Household(test_household_name)
    initialized_user = User(test_username, new_household, points=test_points)
    assert initialized_user.username == test_username
    assert initialized_user.household == new_household
    assert initialized_user.points == test_points
    assert isinstance(initialized_user.habits_completed, dict)
    assert isinstance(initialized_user.streaks, dict)
    assert isinstance(initialized_user.bonus_claimed, dict)

def test_has_completed_today(mock_user, mock_habit):
    """Test checking if a habit has been completed today."""
    assert not mock_user.has_completed_today(mock_habit.name)
    
    # Add a completion for today
    today = datetime.now().date()
    mock_user.track_completion(mock_habit.name, today, mock_habit.periodicity, mock_habit.points)
    assert mock_user.has_completed_today(mock_habit.name)

def test_track_completion(mock_user, mock_habit):
    """Test tracking habit completion."""
    today = datetime.now().date()
    mock_user.track_completion(mock_habit.name, today, mock_habit.periodicity, mock_habit.points)
    
    assert mock_habit.name in mock_user.habits_completed
    assert len(mock_user.habits_completed[mock_habit.name]) == 1
    assert mock_user.habits_completed[mock_habit.name][0] == today
    assert mock_user.streaks[mock_habit.name] == 1
    assert mock_user.points == mock_habit.points

def test_update_streak_daily(mock_user, mock_habit):
    """Test updating streak for daily habit."""
    today = datetime.now().date()
    
    # Complete habit for 3 consecutive days
    for i in range(3):
        date = today - timedelta(days=2-i)
        mock_user.track_completion(mock_habit.name, date, "daily", mock_habit.points)
    
    assert mock_user.streaks[mock_habit.name] == 3
    assert mock_user.points == mock_habit.points * 3

def test_update_streak_weekly(mock_user):
    """Test updating streak for weekly habit."""
    weekly_habit = Habit("Weekly Exercise", "weekly", 10)
    today = datetime.now().date()
    
    # Complete habit for 3 consecutive weeks
    for i in range(3):
        date = today - timedelta(weeks=2-i)
        mock_user.track_completion(weekly_habit.name, date, "weekly", weekly_habit.points)
    
    assert mock_user.streaks[weekly_habit.name] == 3
    assert mock_user.points == weekly_habit.points * 3

def test_streak_reset(mock_user, mock_habit):
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
        mock_user.track_completion(mock_habit.name, date, "daily", mock_habit.points)
    
    assert mock_user.streaks[mock_habit.name] == 1  # Streak should reset after the gap
    assert mock_user.points == mock_habit.points * 4  # Points for 4 completions

def test_get_bonus_points(mock_user, mock_habit):
    """Test bonus points calculation for streaks."""
    today = datetime.now().date()
    
    # Complete habit for 7 consecutive days
    for i in range(7):
        date = today - timedelta(days=6-i)
        mock_user.track_completion(mock_habit.name, date, "daily", mock_habit.points)
    
    assert mock_user.get_bonus_points(mock_habit.name) == 5  # Should get bonus on 7th day
    assert mock_user.get_bonus_points("nonexistent_habit") == 0  # No bonus for non-existent habits
    assert mock_user.points == (mock_habit.points * 7) + 5  # Base points plus streak bonus

def test_to_dict(mock_user, mock_habit):
    """Test converting user to dictionary."""
    today = datetime.now().date()
    mock_user.track_completion(mock_habit.name, today, mock_habit.periodicity, mock_habit.points)
    
    user_dict = mock_user.to_dict()
    assert isinstance(user_dict, dict)
    assert user_dict["username"] == mock_user.username
    assert user_dict["household"] == mock_user.household.name
    assert isinstance(user_dict["habits_completed"], dict)
    assert isinstance(user_dict["streaks"], dict)
    assert isinstance(user_dict["bonus_claimed"], dict)
    assert user_dict["points"] == mock_user.points
    
    # Check habit completion date format
    habit_dates = user_dict["habits_completed"][mock_habit.name]
    assert isinstance(habit_dates[0], str)
    assert datetime.strptime(habit_dates[0], "%Y-%m-%d").date() == today

def test_from_dict_valid(mock_household):
    """Test creating user from valid dictionary."""
    user_data = {
        "username": "test_user",
        "points": 10,
        "habits_completed": {
            "Exercise": ["2025-04-15"]
        },
        "streaks": {"Exercise": 1},
        "bonus_claimed": {}
    }
    
    created_user = User.from_dict(user_data, mock_household)
    assert created_user.username == "test_user"
    assert created_user.points == 10
    assert len(created_user.habits_completed["Exercise"]) == 1
    assert created_user.streaks["Exercise"] == 1

def test_from_dict_invalid():
    """Test creating user from invalid dictionary."""
    with pytest.raises(ValueError, match="Data must be a dictionary"):
        User.from_dict("not a dict", None)
    
    with pytest.raises(ValueError, match="Username is required"):
        User.from_dict({}, None)
    
    with pytest.raises(ValueError, match="Points must be a non-negative number"):
        User.from_dict({"username": "test", "points": -1}, None)

def test_streak_bonus_points(mock_user, mock_habit):
    """Test that streak bonuses add points correctly."""
    today = datetime.now().date()
    initial_points = mock_user.points
    
    # Complete habit for 7 consecutive days
    for i in range(7):
        date = today - timedelta(days=6-i)
        mock_user.track_completion(mock_habit.name, date, "daily", mock_habit.points)
    
    # Should have base points for each completion plus streak bonus
    assert mock_user.points > initial_points + (7 * mock_habit.points)
    # Verify the bonus was added (5 points for 7-day streak)
    assert mock_user.points == initial_points + (7 * mock_habit.points) + 5

def test_add_points(mock_user):
    """Test adding points to user."""
    initial_points = mock_user.points
    mock_user.add_points(10)
    assert mock_user.points == initial_points + 10