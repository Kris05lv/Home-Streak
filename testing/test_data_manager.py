"""Test module for DataManager service.
This module provides comprehensive testing for the DataManager service
which handles data persistence and manipulation.
"""
import pytest
from services.data_manager import DataManager
from classes.habit import Habit
from classes.user import User

@pytest.fixture
def setup_and_cleanup():
    """Ensure clean state before and after tests."""
    DataManager.clear_data()
    yield
    DataManager.clear_data()

@pytest.fixture
def test_habit():
    """Create a test habit."""
    return Habit("TestHabit", "daily", 5)

@pytest.fixture
def test_bonus_habit():
    """Create a test bonus habit."""
    return Habit("BonusHabit", "weekly", 10, is_bonus=True)

@pytest.fixture
def test_user():
    """Create a test user."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    return user

def test_create_household(setup_and_cleanup):
    """Test household creation."""
    DataManager.create_household("TestHouse")
    data = DataManager.load_data()
    assert "TestHouse" in data["households"]
    assert "members" in data["households"]["TestHouse"]
    assert "points" in data["households"]["TestHouse"]

def test_save_user(setup_and_cleanup):
    """Test user creation and storage."""
    DataManager.create_household("TestHouse")
    user = User("testuser", "TestHouse")
    DataManager.save_user(user)
    
    data = DataManager.load_data()
    assert "testuser" in data["households"]["TestHouse"]["members"]
    assert "testuser" in data["households"]["TestHouse"]["points"]
    assert data["households"]["TestHouse"]["points"]["testuser"] == 0

def test_save_habit(setup_and_cleanup, test_habit):
    """Test saving regular habits."""
    DataManager.save_habit(test_habit)
    data = DataManager.load_data()
    saved_habit = next((h for h in data["habits"] if h["name"] == "TestHabit"), None)
    assert saved_habit is not None
    assert saved_habit["periodicity"] == "daily"
    assert saved_habit["points"] == 5

def test_save_bonus_habit(setup_and_cleanup, test_bonus_habit):
    """Test saving bonus habits."""
    DataManager.save_bonus_habit(test_bonus_habit)
    data = DataManager.load_data()
    saved_habit = next((h for h in data["bonus_habits"] if h["name"] == "BonusHabit"), None)
    assert saved_habit is not None
    assert saved_habit["is_bonus"] is True
    assert saved_habit["points"] == 10

def test_complete_habit(setup_and_cleanup, test_habit, test_user):
    """Test habit completion."""
    DataManager.save_habit(test_habit)
    result = DataManager.complete_habit("testuser", "TestHabit")
    assert result is True
    
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 5
    assert "TestHabit" in data["streaks"]["testuser"]
    assert data["streaks"]["testuser"]["TestHabit"] == 1

def test_claim_bonus_habit(setup_and_cleanup, test_bonus_habit, test_user):
    """Test claiming bonus habits."""
    DataManager.save_bonus_habit(test_bonus_habit)
    result = DataManager.claim_bonus_habit("testuser", "BonusHabit")
    assert result is True
    
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 10
    
    # Try claiming again in same period
    result = DataManager.claim_bonus_habit("testuser", "BonusHabit")
    assert result is False

def test_reset_monthly_scores(setup_and_cleanup, test_user, test_habit):
    """Test monthly score reset."""
    DataManager.save_habit(test_habit)
    DataManager.complete_habit("testuser", "TestHabit")
    
    DataManager.reset_monthly_scores()
    data = DataManager.load_data()
    assert data["households"]["TestHouse"]["points"]["testuser"] == 0

def test_load_habits(setup_and_cleanup, test_habit, test_bonus_habit):
    """Test loading all habits."""
    DataManager.save_habit(test_habit)
    DataManager.save_bonus_habit(test_bonus_habit)
    
    habits = DataManager.load_habits()
    assert len(habits) == 2
    assert any(h["name"] == "TestHabit" for h in habits)
    assert any(h["name"] == "BonusHabit" for h in habits)

def test_get_habit(setup_and_cleanup, test_habit):
    """Test retrieving specific habits."""
    DataManager.save_habit(test_habit)
    habit = DataManager.get_habit("TestHabit")
    assert habit is not None
    assert habit["name"] == "TestHabit"
    
    # Test non-existent habit
    assert DataManager.get_habit("NonExistentHabit") is None

def test_reset_habits(setup_and_cleanup, test_habit, test_user):
    """Test habit reset functionality."""
    DataManager.save_habit(test_habit)
    DataManager.complete_habit("testuser", "TestHabit")
    
    DataManager.reset_habits()
    data = DataManager.load_data()
    habit = next((h for h in data["habits"] if h["name"] == "TestHabit"), None)
    assert habit["last_completed_at"] is None

def test_clear_data(setup_and_cleanup):
    """Test data clearing functionality."""
    # Add some data first
    DataManager.create_household("TestHouse")
    DataManager.save_habit(Habit("TestHabit", "daily", 5))
    
    DataManager.clear_data()
    data = DataManager.load_data()
    assert len(data["households"]) == 0
    assert len(data["habits"]) == 0
    assert len(data["bonus_habits"]) == 0