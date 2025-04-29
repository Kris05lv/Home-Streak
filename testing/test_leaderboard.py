"""Test module for Leaderboard service.
This module provides comprehensive testing for the Leaderboard service
which handles user rankings and performance tracking.
"""
import pytest
from datetime import datetime
from services.leaderboard import Leaderboard
from services.data_manager import DataManager
from classes.user import User

@pytest.fixture
def clean_data():
    """Ensure clean state before and after tests."""
    DataManager.clear_data()
    yield
    DataManager.clear_data()

@pytest.fixture
def leaderboard_instance():
    """Create a leaderboard instance."""
    return Leaderboard()

@pytest.fixture
def test_household():
    """Create a test household with users."""
    DataManager.create_household("TestHouse")
    users = [
        User("user1", "TestHouse"),
        User("user2", "TestHouse"),
        User("user3", "TestHouse")
    ]
    for user in users:
        DataManager.save_user(user)
    return "TestHouse"

def test_initialization(leaderboard_instance):
    """Test leaderboard initialization."""
    assert isinstance(leaderboard_instance.rankings, dict)
    assert isinstance(leaderboard_instance.past_rankings, list)
    assert hasattr(leaderboard_instance, 'top_performers')

def test_update(clean_data, test_household):
    """Test updating the leaderboard."""
    leaderboard = Leaderboard()
    user = User("testuser", test_household, 5)
    leaderboard.update(user)
    
    rankings = leaderboard.get_sorted_rankings(test_household)
    assert rankings["testuser"] == 5

def test_multiple_updates(clean_data, test_household):
    """Test multiple updates to the leaderboard."""
    leaderboard = Leaderboard()
    user1 = User("user1", test_household, 10)
    user2 = User("user2", test_household, 15)
    
    leaderboard.update(user1)
    leaderboard.update(user2)
    
    rankings = leaderboard.get_sorted_rankings(test_household)
    assert rankings["user1"] == 10
    assert rankings["user2"] == 15

def test_reset_monthly(clean_data, test_household):
    """Test resetting monthly scores."""
    leaderboard = Leaderboard()
    user = User("testuser", test_household, 5)
    leaderboard.update(user)
    
    # Reset scores
    leaderboard.reset_monthly()
    
    # Check that rankings are empty
    rankings = leaderboard.get_sorted_rankings(test_household)
    assert not rankings

def test_get_sorted_rankings(clean_data, test_household):
    """Test getting sorted rankings."""
    leaderboard = Leaderboard()
    user1 = User("user1", test_household, 10)
    user2 = User("user2", test_household, 15)
    user3 = User("user3", test_household, 5)
    
    leaderboard.update(user1)
    leaderboard.update(user2)
    leaderboard.update(user3)
    
    rankings = leaderboard.get_sorted_rankings(test_household)
    assert list(rankings.keys()) == ["user2", "user1", "user3"]

def test_get_top_performers(clean_data, test_household):
    """Test getting top performers."""
    leaderboard = Leaderboard()
    user = User("testuser", test_household, 5)
    leaderboard.update(user)
    leaderboard.reset_monthly()  # This should save the top performer
    
    top_performers = leaderboard.get_top_performers()
    assert len(top_performers) > 0
    assert top_performers[0]["top_user"] == "testuser"
    assert top_performers[0]["points"] == 5

def test_get_past_rankings(clean_data, test_household):
    """Test getting past rankings."""
    leaderboard = Leaderboard()
    user = User("testuser", test_household, 5)
    leaderboard.update(user)
    leaderboard.reset_monthly()  # This should save the rankings
    
    past_rankings = leaderboard.get_past_rankings()
    assert len(past_rankings) > 0
    assert test_household in past_rankings[0]["rankings"]
    assert past_rankings[0]["rankings"][test_household]["testuser"] == 5

def test_nonexistent_household(clean_data, leaderboard_instance):
    """Test handling of non-existent household."""
    rankings = leaderboard_instance.get_sorted_rankings("NonExistentHouse")
    assert rankings == {}