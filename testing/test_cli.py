"""Test module for CLI commands.
This module provides comprehensive testing for all CLI commands in the habit tracker.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.data_manager import DataManager
import pytest
from click.testing import CliRunner
from cli import create_household, add_user, add_habit, add_bonus_habit
from cli import complete_habit, list_habits, view_leaderboard, reset_monthly_scores
from cli import view_top_performers, view_past_rankings, clear_data


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

@pytest.fixture
def clean_data():
    """Ensure clean state before and after tests."""
    if os.path.exists(DataManager.DATA_FILE):
        os.remove(DataManager.DATA_FILE)
    yield
    if os.path.exists(DataManager.DATA_FILE):
        os.remove(DataManager.DATA_FILE)

def test_create_household(runner, clean_data):
    """Test creating a new household."""
    result = runner.invoke(create_household, ["TestHouse"])
    assert result.exit_code == 0
    assert "Household 'TestHouse' created" in result.output

def test_add_user(runner, clean_data):
    """Test adding a user to a household."""
    # First create a household
    runner.invoke(create_household, ["TestHouse"])
    # Then add a user
    result = runner.invoke(add_user, ["testuser", "TestHouse"])
    assert result.exit_code == 0
    assert "User 'testuser' added to household 'TestHouse'" in result.output

def test_add_habit(runner, clean_data):
    """Test adding a regular habit."""
    result = runner.invoke(add_habit, ["Exercise", "daily", "5"])
    assert result.exit_code == 0
    assert "Habit 'Exercise' added as a daily habit worth 5 points" in result.output

def test_add_bonus_habit(runner, clean_data):
    """Test adding a bonus habit."""
    result = runner.invoke(add_bonus_habit, ["WeeklyChallenge", "weekly", "10"])
    assert result.exit_code == 0
    assert "Bonus Habit 'WeeklyChallenge' added" in result.output

def test_complete_habit(runner, clean_data):
    """Test habit completion."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["testuser", "TestHouse"])
    runner.invoke(add_habit, ["Exercise", "daily", "5"])
    
    # Test completion
    result = runner.invoke(complete_habit, ["testuser", "Exercise"])
    assert result.exit_code == 0
    assert "completed by 'testuser'" in result.output

def test_list_habits(runner, clean_data):
    """Test listing all habits."""
    # Add some habits first
    runner.invoke(add_habit, ["Exercise", "daily", "5"])
    runner.invoke(add_habit, ["Reading", "weekly", "10"])
    
    result = runner.invoke(list_habits)
    assert result.exit_code == 0
    assert "Exercise" in result.output
    assert "Reading" in result.output

def test_view_leaderboard(runner, clean_data):
    """Test viewing the leaderboard."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["user1", "TestHouse"])
    runner.invoke(add_user, ["user2", "TestHouse"])
    
    result = runner.invoke(view_leaderboard, ["TestHouse"])
    assert result.exit_code == 0
    assert "Leaderboard for 'TestHouse'" in result.output

def test_reset_monthly_scores(runner, clean_data):
    """Test resetting monthly scores."""
    result = runner.invoke(reset_monthly_scores)
    assert result.exit_code == 0
    assert "Monthly scores reset" in result.output

def test_view_top_performers(runner, clean_data):
    """Test viewing top performers."""
    result = runner.invoke(view_top_performers)
    assert result.exit_code == 0
    # Initially there should be no top performers
    assert "No top performers recorded yet" in result.output

def test_view_past_rankings(runner, clean_data):
    """Test viewing past rankings."""
    result = runner.invoke(view_past_rankings)
    assert result.exit_code == 0
    # Initially there should be no past rankings
    assert "No past rankings recorded" in result.output

def test_clear_data(runner, clean_data):
    """Test clearing all data."""
    result = runner.invoke(clear_data)
    assert result.exit_code == 0
    assert "All data has been cleared" in result.output

def test_invalid_household(runner, clean_data):
    """Test adding user to non-existent household."""
    result = runner.invoke(add_user, ["testuser", "NonExistentHouse"])
    assert result.exit_code == 0
    assert "Error" in result.output

def test_invalid_habit_completion(runner, clean_data):
    """Test completing non-existent habit."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["testuser", "TestHouse"])
    
    result = runner.invoke(complete_habit, ["testuser", "NonExistentHabit"])
    assert result.exit_code == 0
    assert "not found" in result.output

def test_bonus_habit_completion(runner, clean_data):
    """Test completing a bonus habit."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["testuser", "TestHouse"])
    runner.invoke(add_bonus_habit, ["BonusChallenge", "weekly", "20"])
    
    result = runner.invoke(complete_habit, ["testuser", "BonusChallenge"])
    assert result.exit_code == 0
    assert "Bonus Habit 'BonusChallenge' claimed" in result.output

    # Check points
    user = DataManager.get_user("testuser")
    assert user.points == 20