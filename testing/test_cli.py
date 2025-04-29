"""Test module for CLI commands.
This module provides comprehensive testing for all CLI commands in the habit tracker.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from click.testing import CliRunner
from cli import create_household, add_user, add_habit, add_bonus_habit
from cli import complete_habit, list_habits, view_leaderboard, reset_monthly_scores
from cli import view_top_performers, view_past_rankings, clear_data
from services.data_manager import DataManager

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

@pytest.fixture
def clean_data():
    """Ensure clean state before and after tests."""
    DataManager.clear_data()
    yield
    DataManager.clear_data()

def test_create_household(runner):
    """Test creating a new household."""
    result = runner.invoke(create_household, ["TestHouse"])
    assert result.exit_code == 0
    assert "Household 'TestHouse' created" in result.output

def test_add_user(runner):
    """Test adding a user to a household."""
    # First create a household
    runner.invoke(create_household, ["TestHouse"])
    # Then add a user
    result = runner.invoke(add_user, ["testuser", "TestHouse"])
    assert result.exit_code == 0
    assert "User 'testuser' added to household 'TestHouse'" in result.output

def test_add_habit(runner):
    """Test adding a regular habit."""
    result = runner.invoke(add_habit, ["Exercise", "daily", "5"])
    assert result.exit_code == 0
    assert "Habit 'Exercise' added as a daily habit worth 5 points" in result.output

def test_add_bonus_habit(runner):
    """Test adding a bonus habit."""
    result = runner.invoke(add_bonus_habit, ["WeeklyChallenge", "weekly", "10"])
    assert result.exit_code == 0
    assert "Bonus Habit 'WeeklyChallenge' added" in result.output

def test_complete_habit(runner):
    """Test completing a habit."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["testuser", "TestHouse"])
    runner.invoke(add_habit, ["Exercise", "daily", "5"])
    
    # Test completion
    result = runner.invoke(complete_habit, ["testuser", "Exercise"])
    assert result.exit_code == 0
    assert "completed by 'testuser'" in result.output

def test_list_habits(runner):
    """Test listing all habits."""
    # Add some habits first
    runner.invoke(add_habit, ["Exercise", "daily", "5"])
    runner.invoke(add_habit, ["Reading", "weekly", "10"])
    
    result = runner.invoke(list_habits)
    assert result.exit_code == 0
    assert "Exercise" in result.output
    assert "Reading" in result.output

def test_view_leaderboard(runner):
    """Test viewing the leaderboard."""
    # Setup
    runner.invoke(create_household, ["TestHouse"])
    runner.invoke(add_user, ["user1", "TestHouse"])
    runner.invoke(add_user, ["user2", "TestHouse"])
    
    result = runner.invoke(view_leaderboard, ["TestHouse"])
    assert result.exit_code == 0
    assert "Leaderboard for 'TestHouse'" in result.output

def test_reset_monthly_scores(runner):
    """Test resetting monthly scores."""
    result = runner.invoke(reset_monthly_scores)
    assert result.exit_code == 0
    assert "Monthly scores reset" in result.output

def test_view_top_performers(runner):
    """Test viewing top performers."""
    # Clear data first
    runner.invoke(clear_data)
    result = runner.invoke(view_top_performers)
    assert result.exit_code == 0
    # Initially there should be no top performers
    assert "No top performers recorded yet" in result.output

def test_view_past_rankings(runner):
    """Test viewing past rankings."""
    # Clear data first
    runner.invoke(clear_data)
    result = runner.invoke(view_past_rankings)
    assert result.exit_code == 0
    # Initially there should be no past rankings
    assert "No past rankings recorded" in result.output

def test_clear_data(runner):
    """Test clearing all data."""
    result = runner.invoke(clear_data)
    assert result.exit_code == 0
    assert "All data has been cleared" in result.output

def test_invalid_household(runner):
    """Test adding user to non-existent household."""
    result = runner.invoke(add_user, ["testuser", "NonExistentHouse"])
    assert result.exit_code == 0
    assert "Error" in result.output

def test_invalid_habit_completion(runner):
    """Test completing non-existent habit."""
    result = runner.invoke(complete_habit, ["testuser", "NonExistentHabit"])
    assert result.exit_code == 0
    assert "not found" in result.output

def test_bonus_habit_completion(runner):
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