"""Test module for DataManager service.
This module provides comprehensive testing for the DataManager service
which handles data persistence and manipulation.
"""
import pytest
from services.data_manager import DataManager
from classes.habit import Habit
from classes.user import User

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Ensure clean state before and after tests."""
    DataManager.clear_data()
    yield
    DataManager.clear_data()

def test_create_household():
    """Test household creation."""
    DataManager.create_household("TestHouse")
    data = DataManager.load_data()
    assert "TestHouse" in data["households"]
    assert "members" in data["households"]["TestHouse"]
    assert "points" in data["households"]["TestHouse"]

def test_save_user():
    """Test user creation and storage."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    data = DataManager.load_data()
    assert "testuser" in data["households"]["TestHouse"]["members"]
    assert "testuser" in data["households"]["TestHouse"]["points"]
    assert data["households"]["TestHouse"]["points"]["testuser"] == 0

def test_save_habit():
    """Test saving regular habits."""
    habit = Habit("TestHabit", "daily", 5)
    DataManager.save_habit(habit)
    data = DataManager.load_data()
    saved_habit = next((h for h in data["habits"] if h["name"] == "TestHabit"), None)
    assert saved_habit is not None
    assert saved_habit["periodicity"] == "daily"
    assert saved_habit["points"] == 5

def test_save_bonus_habit():
    """Test saving bonus habits."""
    bonus_habit = Habit("BonusHabit", "weekly", 10, is_bonus=True)
    DataManager.save_bonus_habit(bonus_habit)
    data = DataManager.load_data()
    saved_habit = next((h for h in data["bonus_habits"] if h["name"] == "BonusHabit"), None)
    assert saved_habit is not None
    assert saved_habit["is_bonus"] is True
    assert saved_habit["points"] == 10

def test_complete_habit():
    """Test habit completion."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    habit = Habit("TestHabit", "daily", 5)
    DataManager.save_habit(habit)

    result = DataManager.complete_habit("testuser", "TestHabit")
    assert result is True
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 5
    assert "TestHabit" in data["streaks"]["testuser"]
    assert data["streaks"]["testuser"]["TestHabit"] == 1

def test_claim_bonus_habit():
    """Test claiming bonus habits."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    bonus_habit = Habit("BonusHabit", "weekly", 10, is_bonus=True)
    DataManager.save_bonus_habit(bonus_habit)

    result = DataManager.claim_bonus_habit("testuser", "BonusHabit")
    assert result is True
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 10
    # Try claiming again in same period
    result = DataManager.claim_bonus_habit("testuser", "BonusHabit")
    assert result is False

def test_reset_monthly_scores():
    """Test monthly score reset."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    habit = Habit("TestHabit", "daily", 5)
    DataManager.save_habit(habit)
    DataManager.complete_habit("testuser", "TestHabit")
    DataManager.reset_monthly_scores()
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 0

def test_load_habits():
    """Test loading all habits."""
    habit = Habit("TestHabit", "daily", 5)
    bonus_habit = Habit("BonusHabit", "weekly", 10, is_bonus=True)
    DataManager.save_habit(habit)
    DataManager.save_bonus_habit(bonus_habit)
    habits = DataManager.load_habits()
    assert len(habits) == 2
    assert any(h["name"] == "TestHabit" for h in habits)
    assert any(h["name"] == "BonusHabit" for h in habits)

def test_get_habit():
    """Test retrieving specific habits."""
    habit = Habit("TestHabit", "daily", 5)
    DataManager.save_habit(habit)
    habit_data = DataManager.get_habit("TestHabit")
    assert habit_data is not None
    assert habit_data["name"] == "TestHabit"
    # Test non-existent habit
    assert DataManager.get_habit("NonExistentHabit") is None

def test_reset_habits():
    """Test habit reset functionality."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    habit = Habit("TestHabit", "daily", 5)
    DataManager.save_habit(habit)
    
    # Complete the habit and verify completion
    success = DataManager.complete_habit("testuser", "TestHabit")
    assert success is True
    
    # Verify the streak is set
    data = DataManager.load_data()
    assert data["streaks"]["testuser"]["TestHabit"] == 1
    
    # Reset habits and verify streak is reset
    DataManager.reset_habits()
    data = DataManager.load_data()
    assert data["streaks"]["testuser"]["TestHabit"] == 0

def test_clear_data():
    """Test data clearing functionality."""
    # Add some data first
    DataManager.create_household("TestHouse")
    DataManager.save_habit(Habit("TestHabit", "daily", 5))
    DataManager.clear_data()
    data = DataManager.load_data()
    assert len(data["households"]) == 0
    assert len(data["habits"]) == 0
    assert len(data["bonus_habits"]) == 0