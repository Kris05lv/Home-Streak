"""Module for testing habit functionality.
This module provides test cases for habit functionality.
"""
import pytest
from datetime import datetime
from classes.habit import Habit
from classes.user import User
from classes.household import Household

@pytest.fixture
def habit():
    return Habit(name="Exercise", periodicity="daily", points=5)

@pytest.fixture
def bonus_habit():
    return Habit(name="Weekly Challenge", periodicity="weekly", points=10, is_bonus=True)

@pytest.fixture
def user():
    household = Household("Test Household")
    return User("test_user", household)

def test_habit_initialization():
    """Test habit initialization with valid parameters."""
    test_habit = Habit("Exercise", "daily", 5)
    assert test_habit.name == "Exercise"
    assert test_habit.periodicity == "daily"
    assert test_habit.points == 5
    assert not test_habit.is_bonus
    assert isinstance(test_habit.created_at, str)

def test_habit_initialization_with_whitespace():
    """Test habit initialization handles whitespace in name."""
    test_habit = Habit("  Exercise  ", "daily", 5)
    assert test_habit.name == "Exercise"

def test_habit_invalid_name():
    """Test habit initialization with invalid name."""
    with pytest.raises(ValueError, match="Habit name cannot be empty"):
        Habit("", "daily", 5)
    with pytest.raises(ValueError, match="Habit name cannot be empty"):
        Habit("   ", "daily", 5)

def test_habit_invalid_points():
    """Test habit initialization with invalid points."""
    with pytest.raises(ValueError, match="Points cannot be negative"):
        Habit("Exercise", "daily", -5)

def test_habit_invalid_periodicity():
    """Test habit initialization with invalid periodicity."""
    with pytest.raises(ValueError, match="Periodicity must be either 'daily' or 'weekly'"):
        Habit("Exercise", "monthly", 5)

def test_habit_completion(habit, user):
    """Test completing a habit for the first time."""
    result = habit.complete(user)
    assert "Good job" in result
    assert str(habit.points) in result
    assert user.points == habit.points
    assert habit.name in user.habits_completed

def test_habit_double_completion(habit, user):
    """Test completing the same habit twice in one day."""
    habit.complete(user)
    result = habit.complete(user)
    assert "Oops!" in result
    assert "already been completed today" in result
    assert user.points == habit.points  # Points should not increase

def test_bonus_habit_completion(bonus_habit, user):
    """Test completing a bonus habit."""
    result = bonus_habit.complete(user)
    assert "Good job" in result
    assert str(bonus_habit.points) in result
    assert user.points == bonus_habit.points
    
    # Try completing the bonus habit again in the same day
    result = bonus_habit.complete(user)
    assert "Oops!" in result
    assert "already been completed today" in result

def test_habit_point_calculation(habit, user):
    """Test point calculation including streaks."""
    points_before = user.points
    
    # Complete the habit 7 times
    for i in range(7):
        result = habit.complete(user)
        # Reset the last completion date to simulate next day
        if user.habits_completed[habit.name]:
            last_date = datetime.strptime(user.habits_completed[habit.name][-1].strftime("%Y-%m-%d"), "%Y-%m-%d")
            user.habits_completed[habit.name][-1] = last_date.replace(day=last_date.day + 1).date()
    
    points_after = user.points
    # Should have at least the base points for each completion
    assert points_after >= points_before + (7 * habit.points)
    # Verify at least one completion was recorded
    assert len(user.habits_completed[habit.name]) == 7

def test_habit_to_dict(habit):
    """Test converting habit to dictionary."""
    habit_dict = habit.to_dict()
    assert habit_dict["name"] == habit.name
    assert habit_dict["periodicity"] == habit.periodicity
    assert habit_dict["points"] == habit.points
    assert habit_dict["is_bonus"] == habit.is_bonus
    assert "created_at" in habit_dict

def test_habit_from_dict():
    """Test creating habit from dictionary."""
    habit_data = {
        "name": "Exercise",
        "periodicity": "daily",
        "points": 5,
        "is_bonus": False
    }
    habit = Habit.from_dict(habit_data)
    assert habit.name == habit_data["name"]
    assert habit.periodicity == habit_data["periodicity"]
    assert habit.points == habit_data["points"]
    assert habit.is_bonus == habit_data["is_bonus"]
