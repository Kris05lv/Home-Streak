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
    """Test updating user scores."""
    user = User("user1", "TestHouse", points=10)
    Leaderboard.update(user)
    
    data = DataManager.load_data()
    assert "TestHouse" in data["leaderboard"]["rankings"]
    assert data["leaderboard"]["rankings"]["TestHouse"]["user1"] == 10

def test_multiple_updates(clean_data, test_household):
    """Test multiple score updates."""
    users = [
        User("user1", "TestHouse", points=10),
        User("user2", "TestHouse", points=20),
        User("user3", "TestHouse", points=15)
    ]
    
    for user in users:
        Leaderboard.update(user)
    
    data = DataManager.load_data()
    rankings = data["leaderboard"]["rankings"]["TestHouse"]
    
    # Check if rankings are sorted
    assert list(rankings.keys()) == ["user2", "user3", "user1"]
    assert list(rankings.values()) == [20, 15, 10]

def test_reset_monthly(clean_data, leaderboard_instance, test_household):
    """Test monthly reset functionality."""
    # Add some scores
    users = [
        User("user1", "TestHouse", points=10),
        User("user2", "TestHouse", points=20)
    ]
    for user in users:
        Leaderboard.update(user)
    
    # Reset monthly scores
    leaderboard_instance.reset_monthly()
    
    data = DataManager.load_data()
    assert len(data["leaderboard"]["rankings"]) == 0
    assert len(data["leaderboard"]["past_rankings"]) == 1
    
    past_ranking = data["leaderboard"]["past_rankings"][0]
    assert past_ranking["top_user"] == "user2"
    assert past_ranking["points"] == 20

def test_get_sorted_rankings(clean_data, leaderboard_instance, test_household):
    """Test retrieving sorted rankings."""
    users = [
        User("user1", "TestHouse", points=10),
        User("user2", "TestHouse", points=20),
        User("user3", "TestHouse", points=15)
    ]
    for user in users:
        Leaderboard.update(user)
    
    rankings = leaderboard_instance.get_sorted_rankings("TestHouse")
    assert list(rankings.keys()) == ["user2", "user3", "user1"]
    assert list(rankings.values()) == [20, 15, 10]

def test_get_top_performers(clean_data, leaderboard_instance, test_household):
    """Test retrieving top performers."""
    # Add scores and reset multiple times
    for i in range(2):
        users = [
            User("user1", "TestHouse", points=10 * (i + 1)),
            User("user2", "TestHouse", points=20 * (i + 1))
        ]
        for user in users:
            Leaderboard.update(user)
        leaderboard_instance.reset_monthly()
    
    top_performers = leaderboard_instance.get_top_performers()
    assert len(top_performers) == 2
    assert all(p["top_user"] == "user2" for p in top_performers)

def test_get_past_rankings(clean_data, leaderboard_instance, test_household):
    """Test retrieving past rankings."""
    # Add scores and reset
    users = [
        User("user1", "TestHouse", points=10),
        User("user2", "TestHouse", points=20)
    ]
    for user in users:
        Leaderboard.update(user)
    leaderboard_instance.reset_monthly()
    
    past_rankings = leaderboard_instance.get_past_rankings()
    assert len(past_rankings) == 1
    assert "TestHouse" in past_rankings[0]["rankings"]
    assert past_rankings[0]["rankings"]["TestHouse"]["user2"] == 20

def test_nonexistent_household(clean_data, leaderboard_instance):
    """Test handling of non-existent household."""
    rankings = leaderboard_instance.get_sorted_rankings("NonExistentHouse")
    assert rankings == {}