"""Module for testing household functionality.
This module provides test cases for household functionality including member management
and leaderboard features.
"""
import pytest
from classes.household import Household
from classes.user import User

@pytest.fixture
def household():
    """Create a test household."""
    return Household("Test Household")

@pytest.fixture
def user(household):
    """Create a test user."""
    return User("test_user", household)

@pytest.fixture
def multiple_users(household):
    """Create multiple test users with different points."""
    users = [
        User("user1", household, points=100),
        User("user2", household, points=50),
        User("user3", household, points=75)
    ]
    return users

def test_household_initialization():
    """Test household initialization."""
    name = "Test Household"
    household = Household(name)
    assert household.name == name
    assert isinstance(household.members, list)
    assert len(household.members) == 0

def test_add_member(household, user):
    """Test adding a member to the household."""
    household.add_member(user)
    assert len(household.members) == 1
    assert user in household.members

def test_add_duplicate_member(household, user):
    """Test adding the same member twice."""
    household.add_member(user)
    household.add_member(user)  # Try to add the same user again
    assert len(household.members) == 1  # Should still only have one member

def test_get_leaderboard_empty(household):
    """Test getting leaderboard with no members."""
    leaderboard = household.get_leaderboard()
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == 0

def test_get_leaderboard_ordered(household, multiple_users):
    """Test leaderboard ordering by points."""
    # Add users in random order
    household.add_member(multiple_users[1])  # 50 points
    household.add_member(multiple_users[0])  # 100 points
    household.add_member(multiple_users[2])  # 75 points

    leaderboard = household.get_leaderboard()
    assert len(leaderboard) == 3
    # Check if ordered by points (descending)
    assert leaderboard[0].points == 100
    assert leaderboard[1].points == 75
    assert leaderboard[2].points == 50

def test_to_dict(household, user):
    """Test converting household to dictionary."""
    household.add_member(user)
    household_dict = household.to_dict()
    
    assert isinstance(household_dict, dict)
    assert household_dict["name"] == household.name
    assert isinstance(household_dict["members"], list)
    assert len(household_dict["members"]) == 1
    
    member_dict = household_dict["members"][0]
    assert member_dict["username"] == user.username
    assert member_dict["points"] == user.points
    assert member_dict["habits_completed"] == user.habits_completed
    assert member_dict["streaks"] == user.streaks
    assert member_dict["bonus_claimed"] == user.bonus_claimed